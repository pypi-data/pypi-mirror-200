import numpy
from .types import ProcessedFamily
import warnings
from heapq import heappush, heappop

def compute_phased_family_likelihood_dyn_loop(mother, maternal_haplotypes, recombination_rates, mutation_rates):
    """Simple dynamic programming implementation of phased (type I) family likelihood.
    
    The dynamic programming algorithm is implemented explicitly with nested loops.
    This function can be compiled with numba if available for a big speedup.
    """
    
    lh = 1.0
    m = numpy.zeros(shape=mother.shape)
    for hap in maternal_haplotypes:
        for pos in range(mother.shape[0]):
            for r in range(2):
                # compute mutation probability
                if hap[pos] > 0:
                    # STR marker
                    mut_step = abs(mother[pos, r] - hap[pos])
                    if mut_step == 0:
                        mutp = 1 - mutation_rates[pos]
                    elif mut_step == 1:
                        mutp = mutation_rates[pos]
                    else:
                        mutp = 0
                else:
                    # OTHER marker
                    if mother[pos, r] == hap[pos]:
                        mutp = 1 - mutation_rates[pos]
                    else:
                        mutp = mutation_rates[pos]

                # compute recombination probability
                m[pos, r] = 0.5*mutp if pos == 0 else mutp*(
                    m[pos - 1, r]*(1 - recombination_rates[pos - 1]) +
                    m[pos - 1, 1 - r]*recombination_rates[pos - 1]
                )
        lh *= numpy.sum(m[-1])
    return lh

#TODO this could work better with if the marker was the first index and not the last
def compute_family_mutation_probs(mother, maternal_haplotypes, mutation_rates, numpy=numpy):
    """Compute the mutation probability matrix for a family given the mutation rates
    
    Returns:
    a matrix of shape: 2 (mother ploidity), number of maternal haplotypes in the family, number of markers
    """
    assert mother.shape[0] == maternal_haplotypes.shape[1]
    
    mut_rate_m = numpy.stack([
        1 - mutation_rates,
        mutation_rates,
        numpy.zeros_like(mutation_rates)
    ])

    #assert numpy.all(mother > 0), 'only STR supported in this implementation!' # replace a_max=numpy.where(mother[:,0] < 0, 1.0, 2.0) in numpy.clip for non-STR ?
    mut_d = mother.T.reshape((2, 1, -1)) - maternal_haplotypes
    mut_max = numpy.where(mother[:,0] < 0, 1.0, 2.0)
    mut_i = numpy.clip(numpy.abs(mut_d), 0, mut_max)
    jj = numpy.arange(len(mutation_rates))
    ii = mut_i.astype(numpy.int32)
    # mutp_m.shape: ploidity, mat haps, n_markers
    mutp_m = mut_rate_m[ii, jj]
    return mutp_m

def compute_phased_family_likelihood_dyn_vec(mother, maternal_haplotypes, recombination_rates, mutation_rates, numpy=numpy):
    """Vectorial dynamic programming implementation of phased (type I) family likelihood.
    
    The dynamic programming algorithm is implemented mostly with vector operators and is faster than
    compute_phased_family_likelihood_dyn_loop if numba is not available. This function fails to compile with numba.
    
    numpy: module
        standard numpy or jax.numpy
    """
    mutation_probs = compute_family_mutation_probs(mother, maternal_haplotypes, mutation_rates, numpy=numpy) # FIXME change shape so that pos is the first index
    v = 0.5*mutation_probs[:,:,0]
    for pos in range(1, mother.shape[0]):
        mp = mutation_probs[:, :, pos]
        r = recombination_rates[pos - 1]
        v = mp*(v*(1 - r) + v[::-1]*r)
    return numpy.prod(numpy.sum(v, axis=0))

  
  
def compute_unphased_family_likelihood_dyn_queue_inner(mother, recombination_rates, mutation_probs, cum_lh, early_stop=0.0, fast_stop=0.0):
    """
    Use a priority queue to explore the tree of all possible mother phasings starting from those with highest probability.

    """
    verb = False
    lh_acc = 0
    #lh_accl = []
    lh_count = 0
    possible_phasings = 2**(mother.shape[0] - 1)

    
    # probability for the first marker
    v = 0.5*mutation_probs[:,:,0]
    lh = numpy.prod(numpy.sum(v, axis=0))
    # use a priority queue with tuples with the following format:
    # 0 - minus the maximum reachable likelihood for the branch leaves
    # 1 - marker position/branch length
    # 2 - unique key (int) to retrieve the dyn prog results for the children computation
    # 3 - the likelihood of the partial branch
    # 4 - the molteplicity of this branch
    
    # 2 is needed to store the partial dynamic programming results since 
    # we cannot directly put a numpy array in the tuple using numba, 
    # since numba requires an ordering to be defined for all types 
    # in the tuple (even if it is never used)

    # 4 is needed since when the mother is homozigous we merge
    # the two possible branches into one (since they will give the same likelihood in the end)
    # so we need to keep track of how many possible branches and leaves are
    # represented by this branch to weight the likelihood when summing all the leaves
    array_store = {}
    vkey = 0
    phase_queue = [(-lh*cum_lh[0], 0, vkey, lh, 1)] # negative likelihood of partial phasing, , partial phasing tuple, number of branchings up to now
    array_store[vkey] = v

    max_size = 0
    last_neglh = -lh*cum_lh[0]
    last_lh = 1
    while phase_queue:
        max_size = max(max_size, len(phase_queue))

        # retrieve branch with the highest possibile probability
        neglh, last_pos, vkey0, lh, m = heappop(phase_queue)
        v0 = array_store.pop(vkey0)

        if False:
            if (last_neglh - neglh)/neglh < 0:
                print("branch monotonicity failure", max_size, last_neglh, neglh, (last_neglh - neglh)/neglh)
            assert (last_neglh - neglh)/neglh > -1e-14, "branch monotonicity failure soft"
            #assert last_neglh <= neglh, "branch monotonicity failure hard"
            last_neglh = neglh

        pos = last_pos + 1
        if pos == mother.shape[0]:
            # this is a full phasing (a leaf)
            lh_count += possible_phasings/m
            lh_acc += lh
            #lh_accl.append(lh)
            if verb:
                print('full phasing:', -neglh, lh, lh_count, m)

            # each leaf should have a lower (or equal) likelihood than than the previous, 
            # however there may be very small increases probably due to rounding errors, 
            # so allow very small increases
            #if last_lh < lh:
            #if (last_lh - lh)/lh < -1e-15:
            #    print("leaf monotonicity failure", last_lh, lh, last_lh - lh, (last_lh - lh)/lh)
            assert (last_lh - lh)/lh >= -1e-12, "leaf monotonicity failure"
            last_lh = lh

            # early stopping critieria, give approximate results
            if lh/lh_acc < fast_stop:
                if verb:
                    print('fast stop:', -neglh, lh, fast_stop, possible_phasings, lh_count, possible_phasings - lh_count)
                return lh_acc, max_size
            if lh*(possible_phasings - lh_count)/lh_acc < early_stop:
                if verb:
                    print('early stop:', -neglh, lh, early_stop, possible_phasings, lh_count, possible_phasings - lh_count)
                return lh_acc, max_size
        else:
            # this is a partial phasing
            
            # if the mother is homozygous there is no need to consider the two possible phasings since they yield the same mother's haplotypes
            cases = 1 if mother[pos, 0] == mother[pos, 1] else 2
            next_m = m*cases
            for p in range(cases):
                # compute likelihood for the child node
                mp = mutation_probs[:, :, pos]
                r = recombination_rates[pos - 1] if p else 1 - recombination_rates[pos - 1] 
                v = mp*(v0*(1 - r) + v0[::-1]*r)
                lh = numpy.prod(numpy.sum(v, axis=0))/next_m

                # add key
                if lh > 0:
                    vkey += 1
                    array_store[vkey] = v
                    heappush(phase_queue, (-lh*cum_lh[pos], pos, vkey, lh, next_m))
    
    #assert 2**(mother.shape[0] - 1) == lh_count, f"{2**(mother.shape[0] - 1)} != {lh_count}"
    #print('lh sum test', lh_acc, lh_acc - sum(lh_accl), lh_acc - sum(lh_accl[::-1]))
    return lh_acc, max_size

def compute_unphased_family_likelihood_dyn_queue(mother, maternal_haplotypes, recombination_rates, mutation_rates, early_stop=0.0, fast_stop=0.0, inner_func=compute_unphased_family_likelihood_dyn_queue_inner):
    # compute the maximum likelihood possible 
    mut_max_lh = numpy.cumprod(numpy.max([mutation_rates[1:], 1 - mutation_rates[1:]], axis=0)[::-1])[::-1] # FIXME check mut and 1 - mut
    rec_max_lh = numpy.cumprod(numpy.max([recombination_rates, 1 - recombination_rates], axis=0)[::-1])[::-1]
    cum_lh = numpy.concatenate([mut_max_lh*rec_max_lh, [1.0]])
    mutation_probs = compute_family_mutation_probs(mother, maternal_haplotypes, mutation_rates)
    return inner_func(mother, recombination_rates, mutation_probs, cum_lh, early_stop=early_stop, fast_stop=fast_stop)[0]


from .likelihood_direct import (
    compute_phased_family_likelihood_direct_loop, compute_unphased_family_likelihood_direct_loop,
    compute_phased_family_likelihood_direct_numpy, compute_unphased_family_likelihood_direct_numpy, 
)

implementations = {
    'dynamic': (
        compute_phased_family_likelihood_dyn_vec, 
        compute_unphased_family_likelihood_dyn_queue,
    ),
    'direct-loop': (
        compute_phased_family_likelihood_direct_loop, 
        compute_unphased_family_likelihood_direct_loop,
    ),
    'direct-numpy': (
        compute_phased_family_likelihood_direct_numpy, 
        compute_unphased_family_likelihood_direct_numpy,
    ),
}

try: # if numba is available add jit compiled version of loop based likelihood implementations
    import numba
    from functools import partial
    
    #compute_phased_family_likelihood_dyn_loop_numba = numba.njit(compute_phased_family_likelihood_dyn_loop)
    #compute_unphased_family_likelihood_dyn_queue_numba = partial(
    #    compute_unphased_family_likelihood_dyn_queue, 
    #    inner_func=numba.njit(compute_unphased_family_likelihood_dyn_queue_inner),
    #)
    implementations['dynamic-numba'] = (
        numba.njit(compute_phased_family_likelihood_dyn_loop),
        partial(
            compute_unphased_family_likelihood_dyn_queue, 
            inner_func=numba.njit(compute_unphased_family_likelihood_dyn_queue_inner),
        ),
    )
    implementations['direct-loop-numba'] = (
        numba.njit(compute_phased_family_likelihood_direct_loop),
        numba.njit(compute_unphased_family_likelihood_direct_loop),
    )

except ModuleNotFoundError:
    # numba is not available
    #compute_phased_family_likelihood_dyn_loop_numba = None
    #compute_unphased_family_likelihood_dyn_queue_numba = None
    pass


try:
  import jax
  from functools import partial

  implementations['dynamic-jax'] = (
      jax.jit(partial(compute_phased_family_likelihood_dyn_vec, numpy=jax.numpy)), 
      None,
      #partial(
      #      compute_unphased_family_likelihood_dyn_queue, 
      #      inner_func=jax.jit(compute_unphased_family_likelihood_dyn_queue_inner),
      #),
  )
except ModuleNotFoundError:
  pass

#if 'dynamic-numba' not in implementations and 'dynamic-jax' not in implementations:
#    print('No available accelerated version since') # FIXME 
def get_likelihood_implementation(phased: bool, implementation=None):
    """Select the best available implementation for likelihood computation
    """
    if implementation is None:
        implementation_list = [
          'dynamic-numba',
          'dynamic-jax',
          'dynamic',
          'direct_numpy',
          'direct_loop_numba',
          'direct_loop',
        ]
    elif isinstance(implementation, str):
        implementation_list = [implementation]
    else:
        implementation_list = implementation

    for impl in implementation_list:
        if impl in implementations:
            phased_func, unphased_func = implementations[impl]
            func = phased_func if phased else unphased_func
            if func is not None:
                if implementation is None and impl == 'dynamic':
                    warnings.warn('install numba for faster estimation!')
                return func
    raise ValueError(f"Could not find an available implementation for '{implementation}'")
        
def compute_family_likelihood(fam: ProcessedFamily, recombination_rates, mutation_rates, implementation=None):
    """Compute the likelihood of observing a family given the recombination and mutation rates.
    Dispatches the computation to one of the available implementations.

    fam: ProcessedFamily
        the processed family to compute the likelihood of
    recombination_rates: array of shape (n_markers - 1, )
        the recombination rates
    mutation_rates: array of shape (n_markers, )
        the mutation rates
    implementation: None | str | list of str
        one or more names of the likelihood implementation to use, None for automatic selection
    
    Returns: float
        family likelyhood
    """
    n = len(fam.mother)
    
    if numpy.ndim(mutation_rates) == 0:
        mutation_rates = numpy.full(n, mutation_rates)

    assert fam.maternal_haplotypes.shape[1] == n, f'bad maternal haplotypes length {fam.maternal_haplotypes.shape[1]} while mother is {n}'
    assert len(mutation_rates) == n, f'bad mutation rates length {len(mutation_rates)} while mother is {n}'
    assert len(recombination_rates) == n - 1, f'bad recombination rates length {len(recombination_rates)} while mother is {n}'
    assert fam.is_mother_phased or fam.maternal_haplotypes.shape[0] > 1, 'unphased mother needs at least two children to be informative'
    
    likelihood_func = get_likelihood_implementation(fam.is_mother_phased, implementation=implementation)

    if not isinstance(recombination_rates, numpy.ndarray):
        recombination_rates = numpy.array(recombination_rates)
    if not isinstance(mutation_rates, numpy.ndarray):
        mutation_rates = numpy.array(mutation_rates)

    return likelihood_func(fam.mother, fam.maternal_haplotypes, recombination_rates, mutation_rates)
