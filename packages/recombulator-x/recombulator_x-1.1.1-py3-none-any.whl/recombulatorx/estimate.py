import numpy
import scipy.optimize
from .likelihood import compute_family_likelihood


def compute_family_likelihood_star(args):
    pf = args[0]
    try:
        return pf.fid, compute_family_likelihood(*args)
    except Exception as e:
        print(f'Exception computing family likelihood in family {pf}: {e}')
        raise e


def compute_global_likelihood(families, recombination_rates, mutation_rates, implementation):
    """
    Compute the log-likelihood of multiple families given recombination and mutation rates.

    families: sequence of families
        the preprocessed genetic data of all the families
    recombination_rates: array of shape (n_markers - 1, )
        probability of recombination between adjacent markers
    mutation_rates: array of shape (n_markers, )
        probability of unit mutation (+1 or -1) for each marker
    implementation: string
        the name of the implementation to use for the likelihood computation
    Returns: scalar
        Combined log likelihood of all families
    """
    
    args = [(pf, recombination_rates, mutation_rates, implementation) for pf in families]
    likelihoods = dict(map(compute_family_likelihood_star, args))

    for fid, lh in likelihoods.items():
        assert 0 <= lh and lh <= 1, f"bad probability value {lh} for family {fid}"
        if lh == 0:
            raise ValueError(f"zero likelihood for family {fid}")

    # merge the independent log likelihoods
    return -numpy.sum(numpy.log(numpy.array(list(likelihoods.values()))))

def likelihood_objective_function(x, families, estimate_mutation_rates, starting_mutation_rates, implementation):
    if estimate_mutation_rates == 'no':
        rates = x, starting_mutation_rates
    elif estimate_mutation_rates == 'one':
        rates = x[:-1], x[-1]
    elif estimate_mutation_rates == 'all':
        n = int((len(x) + 1)/2)
        rates = numpy.split(x, [n - 1])
    return compute_global_likelihood(families, *rates, implementation)

def repeat_if_number(x, repeats):
    if numpy.ndim(x) == 0:
        return numpy.full(repeats, x)
    assert len(x) == repeats
    return x
  
def get_starting_params(
  starting_recombination_rates, 
  starting_mutation_rates, 
  estimate_mutation_rates, 
  n_markers,
):
    recomb_params = repeat_if_number(starting_recombination_rates, n_markers - 1)
        
    if estimate_mutation_rates == 'no':
        mut_params = []
    elif estimate_mutation_rates == 'one':
        if numpy.ndim(starting_mutation_rates) > 0:
            raise ValueError('starting_mutation_rates must be a scalar when estimate_mutation_rates is set to "one"')
        mut_params = [starting_mutation_rates]
    elif estimate_mutation_rates == 'all':
                mut_params = repeat_if_number(starting_mutation_rates, n_markers)
    else:
        raise ValueError(f'unknown value "{estimate_mutation_rates}" for estimate_mutation_rates')
    
    return numpy.concatenate([recomb_params, mut_params])

  
def estimate_rates(
  families, 
  starting_recombination_rates=0.05, 
  starting_mutation_rates=0.001, 
  estimate_mutation_rates='no', 
  implementation=None, 
  optimization_method='L-BFGS-B', # default from the original R code
  maxiter=1000,
):
    """Estimate recombination and optionally mutation rates from a set of families.
    
    Estimation is done by expectation maximization, that is by finding recombination 
    and mutation rates that maximize the likelihood of observing the given families.
    Implemented using scipy.optimize.minimize to find recombination and mutation rates 
    that minimize the negative log likelihood.
    
    families: sequence of families
        the preprocessed genetic data of all the families
    starting_recombination_rates: array of shape (n_markers - 1, )
        starting probability of recombination between adjacent markers as initial 
    starting_mutation_rates: array of shape (n_markers, )
        probability of unit mutation (+1 or -1) for each marker
    estimate_mutation_rates: string
        one of 'no', 'one', 'all'. If 'no' 
    implementation: string
        the name of the implementation to use for the likelihood computation
    optimization_method: string
        the name of the method to be passed to scipy.optimize.minimize
    maxiter: int
        the maximum number of optimizing iterations (passed to scipy.optimize.minimize)
      
    Returns: arrays
        an array of estimated recombination rates if estimate_mutation_rates is 'no',
        a tuple of an array of estimated recombination rates and a scalar mutation rate if estimate_mutation_rates is 'one',
        a tuple of an array of estimated recombination rates and an array of mutation rates if estimate_mutation_rates is 'all'
    """
    # parameter preprocessing
    #if estimate_mutation_rates:
    #    print("not fully implemented, add father-daughter likelihood!")

    n_markers = families[0].mother.shape[0]
    if numpy.ndim(starting_recombination_rates) == 0:
        starting_recombination_rates = numpy.full(n_markers - 1, starting_recombination_rates)

    if estimate_mutation_rates == 'no':
        x0_mut = []
    elif estimate_mutation_rates == 'one':
        if numpy.ndim(starting_mutation_rates) > 0:
            raise ValueError('expected scalar value for starting_mutation_rates')
        x0_mut = [starting_mutation_rates]
    elif estimate_mutation_rates == 'all':
        if numpy.ndim(starting_mutation_rates) == 0:
            x0_mut = [starting_mutation_rates]*n_markers
        else:
            x0_mut = starting_mutation_rates
    else:
        raise ValueError(f'unknown value "{estimate_mutation_rates}" for estimate_mutation_rates')
    
    x0=numpy.concatenate([
        starting_recombination_rates,
        x0_mut,
    ])

    r = scipy.optimize.minimize(
        fun=likelihood_objective_function, x0=x0,
        args=(families, estimate_mutation_rates, starting_mutation_rates, implementation),
        bounds=[(1e-8, 0.5)]*len(x0),
        method=optimization_method,
        options=dict(maxiter=maxiter),
    )

    if not r.success:
        raise ValueError(f"Minimization failed to converge: {r.message}")

    if estimate_mutation_rates == 'no':
        est = r.x
    elif estimate_mutation_rates == 'one':
        est = r.x[:-1], r.x[-1]
    elif estimate_mutation_rates == 'all':
        est = numpy.split(r.x, [n_markers - 1])

    return est
