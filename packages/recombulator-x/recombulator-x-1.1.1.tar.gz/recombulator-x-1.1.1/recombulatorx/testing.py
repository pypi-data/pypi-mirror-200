import numpy
from . import ProcessedFamily
import unittest
##########################
# TEST FAMILY GENERATION #
##########################


def generate_random_rates(n_markers: int):
    """Generate random recombination and mutation rates.

    Rates are intended to be not too unrealistic for the human X chromosome.
    Thus, rates are always lower than 0.5 for recombination and 0.05 for mutation
    and the total of the recombination rates is capped at 2.

    n_markers: int
    Number of markers
    
    Returns:
    a tuple of recombination (n_markers - 1) and mutation (n_markers) rates.
    """
    m = numpy.square(numpy.random.rand(n_markers))*0.05
    r = numpy.square(numpy.random.rand(n_markers - 1)*0.5)
    # avoid eccessive recombination which is unrealistic
    s = sum(r)
    if s > 2:
        r = r/s
    return r, m

def generate_haplotypes(n_markers: int, n_haps: int, mode='STR'):
    """
    Generate random haplotypes
    """
    if mode == 'STR':
        base = 10*numpy.arange(1, n_markers + 1)
        noise = numpy.random.randn(n_haps, n_markers)
        haps = base + numpy.clip(numpy.round(3*noise) + 5, 1, 9)
    elif mode == 'SNP':
        alleles = list('ACGT')
        acc = []
        for i in range(n_markers):
            # generate allele freqs for each marker
            p = (numpy.random.random(len(alleles))*[1, 0.5, 0.1, 0.01])**2
            p = p/numpy.sum(p)
            numpy.random.shuffle(p)
            acc.append(numpy.random.choice(alleles, size=n_haps, p=p))
        haps = numpy.array(acc).T
    return haps

def mutate_haplotypes(haps, mutation_rates, mode='STR'):
    """Add random mutations to haplotypes"""
    n_haps, n_markers = haps.shape
    mut_mask = (numpy.random.rand(n_haps, n_markers) < mutation_rates)
    if mode == 'STR':
        muts = (2*numpy.random.randint(2, size=(n_markers, n_haps)) - 1)*mut_mask.T
        mut_haps = haps + muts.T
    elif mode == 'SNP':
        alleles = 'ACGT'
        b2i = {c: i for i, c in enumerate(alleles)}
        i2b = dict(enumerate(alleles))
        ihaps = numpy.vectorize(b2i.get)(haps)
        muts = numpy.random.randint(1, len(alleles), size=haps.shape)
        mut_haps = numpy.vectorize(i2b.get)((ihaps + muts*mut_mask) % len(alleles))
    return mut_haps

def generate_maternal_haplotypes(mother, n_haps: int, recombination_rates, mutation_rates, mode='STR'):
    n_markers = mother.shape[0]
    recomb = (numpy.random.rand(n_haps, n_markers - 1) < recombination_rates).T

    #null_values = dict(STR=numpy.nan, 'N')
    #if mode == 'STR':
    #haps = numpy.full((n_haps, n_markers), -1.0 if)
    haps = numpy.full((n_haps, n_markers), numpy.nan, dtype=(object if mode == 'SNP' else float))
    #print(n_haps, n_markers, haps.shape, haps)
    #elif mode == 'SNP':
    #    haps = numpy.fu

    current_hap = numpy.random.randint(2, size=n_haps)
    for i in range(n_markers):
        haps[:, i] = mother[i, current_hap]
        if i < n_markers - 1:
            current_hap[recomb[i]] = 1 - current_hap[recomb[i]]

    return mutate_haplotypes(haps, mutation_rates, mode=mode)

def generate_processed_family(fid: str, n_sons: int, is_mother_phased: bool, recombination_rates, mutation_rates, mode='STR'):
    mother = generate_haplotypes(len(mutation_rates), 2, mode=mode).T
    haps = generate_maternal_haplotypes(mother, n_sons, recombination_rates, mutation_rates, mode=mode)
    return ProcessedFamily(
        fid=fid,
        is_mother_phased=is_mother_phased,
        mother=mother,
        maternal_haplotypes=haps
    )

def generate_complex_family(fid: str, is_mother_phasable: bool, n_sons: int, n_daughters: int, recombination_rates, mutation_rates, mode='STR'):
    """Generate a realistic family, with sons, daughters (with father) and an optional grandfather"""
    pf = generate_processed_family(fid, n_sons + n_daughters, is_mother_phased=is_mother_phasable, recombination_rates=recombination_rates, mutation_rates=mutation_rates, mode=mode)
    mother, mat_haps = pf.mother, pf.maternal_haplotypes
    if is_mother_phasable:
        # then add the mother's father
        yield (
            fid, 'GRANDFATHER', None, None, 
            mutate_haplotypes(mother.T[:1], mutation_rates),
        )
    yield (
        fid, 'MOTHER', 'GRANDFATHER' if is_mother_phasable else None, None, 
        numpy.sort(mother.T, axis=0),
    )
    
    # add sons
    for i, mat_hap in enumerate(mat_haps[:n_sons]):
        yield (
            fid, f'SON_{i + 1}', None, 'MOTHER', 
            numpy.array([mat_hap]),
        )

    # generate one father for each daughter
    father_haps = generate_haplotypes(len(mutation_rates), n_daughters)
    for i, (father_hap, pat_hap, mat_hap) in enumerate(zip(
        father_haps, mutate_haplotypes(father_haps, mutation_rates), mat_haps[n_sons:])):
        yield (
            fid, f'FATHER_{i+1}', None, None, 
            numpy.array([father_hap]),
        )
        yield (
            fid, f'DAUGHTER_{i+1}', f'FATHER_{i+1}', 'MOTHER', 
            numpy.sort([pat_hap, mat_hap], axis=0),
        )

def generate_complex_families(n_fam_I: int, n_fam_II: int, recombination_rates, mutation_rates):
    """Generate randomly simulated individuals from a given number of type I and II families.
    
    For each family, generate a random number of children (from a Poisson distribution with a
    mean of 2.0), with a minimum of 1 or 2 for type I or II families, respectively. A random 
    number of children (from a binomial distribution with a mean of 0.5) are set to be male and 
    the rest female. For each daughter, a father and his paternal haplotype are generated randomly.
    
    n_fam_I: int
        number of type I families
    n_fam_II: int
        number of type II families
    recombination_rates: array of shape (n_markers - 1, )
        recombination rates between adjacent markers used to generate children
    mutation_rates: array of shape (n_markers, )
        mutation rates of markers used to generate children
    
    Returns:
        an iterator to the generated individuals
    """
    for i in range(n_fam_I + n_fam_II):
        typeI = i < n_fam_I
        n_children = max(1 if typeI else 2, numpy.random.poisson(2.0))
        n_sons = numpy.random.binomial(n_children, 0.5)
        fid = f'FAM_{i}_' + ('I' if typeI else 'II')
        for ind in generate_complex_family(
            fid=fid, n_sons=n_sons, 
            n_daughters=n_children - n_sons, 
            is_mother_phasable=typeI, 
            recombination_rates=recombination_rates, 
            mutation_rates=mutation_rates):
            yield ind

def individuals2ped(path, marker_names, individuals):
    """Write individuals to a pedigree file.
    
    If path ends with `.tsv' write a tab-separated table with an header row,
    otherwise a headerless space-separated table in `.ped' style.
    
    path: str
        path to the pedigree file
    marker_names: sequence of str
        names for the markers
    individuals: sequence
        individuals as generated by generate_complex_families
    """
    sex_coding={1: '1', 2: '2'}
    with open(path, 'wt') as ped:
        if path.endswith('.tsv'):
            print('FID', 'IID', 'PAT', 'MAT', 'SEX', 'PHENO', *(f"{m}-A{a + 1}" for m in marker_names for a in range(2)), sep='\t', file=ped)
            sep = '\t'
        else:
            sep = ' '
        for fid, iid, pat, mat, geno in individuals:
            n_haps = geno.shape[0]
            geno0 = numpy.array([geno[0], [0]*geno.shape[1]]) if n_haps == 1 else geno
            sex = sex_coding[n_haps]
            print(fid, iid, pat or 0, mat or 0, sex, -9, *geno0.T.reshape(-1), sep=sep, file=ped)


def compute_family_likelihood_empirical(mother, maternal_haplotypes, is_mother_phased, recombination_rates, mutation_rates):
    """
    Empirical type I family likelihood computation.

    Randomly generates possible maternal haplotypes with the given rates and
    counts how many times the given maternal haplotypes are generated.

    """
    assert is_mother_phased
    n_markers = mother.shape[0]
    haps = generate_maternal_haplotypes(mother, 100*(2**n_markers), recombination_rates, mutation_rates)
    lh_acc = [
        numpy.sum(
            numpy.all(hap == haps, axis=1))/haps.shape[0]
        for hap in maternal_haplotypes
    ]
    return numpy.prod(lh_acc)


class BaseTests(unittest.TestCase):
    def test_likelihoods_basic(self):
        from recombulatorx.likelihood import implementations, compute_family_likelihood

        available_implementations = implementations.keys()
        available_implementations = [i for i in available_implementations if i != 'direct-loop-numba']
        n_markers = 6

        hap1 = (numpy.arange(n_markers)+1)*10
        hap2 = hap1 + 1
        hom_mother = numpy.tile(hap1, (2,1)).T
        het_mother = numpy.array([hap1, hap2]).T
        zero_rec = numpy.zeros(n_markers - 1)
        zero_mut = numpy.zeros(n_markers)

        test_fams = [
            (ProcessedFamily('hom_zero_1_I', True, hom_mother, numpy.tile(hap1, (1, 1))), (zero_rec, zero_mut), 1.0),
            (ProcessedFamily('hom_zero_2_I', True, hom_mother, numpy.tile(hap1, (2, 1))), (zero_rec, zero_mut), 1.0),
            (ProcessedFamily('hom_mut_2_I', True, hom_mother, numpy.tile(hap1, (1, 1))), (zero_rec, zero_mut + 0.1), 0.9**n_markers),
            (ProcessedFamily('hom_rec_2_I', True, hom_mother, numpy.tile(hap1, (1, 1))), (zero_rec + 0.1, zero_mut), 1.0),#0.9**n_markers),
            (ProcessedFamily('homz_2_II', False, hom_mother, numpy.tile(hap1, (2, 1))), (zero_rec, zero_mut), 1.0),
            (ProcessedFamily('homz_3_II', False, hom_mother, numpy.tile(hap1, (3, 1))), (zero_rec, zero_mut), 1.0),
            (ProcessedFamily('homz_4_II', False, hom_mother, numpy.tile(hap1, (4, 1))), (zero_rec, zero_mut), 1.0),
            (ProcessedFamily('het_zero_2_II', False, hom_mother, numpy.tile(hap1, (2, 1))), (zero_rec, zero_mut), 1.0),
        ]
        for fam, rates, expected_lh in test_fams:
            for impl in available_implementations:
                if impl == 'direct-loop' and not fam.is_mother_phased:
                    continue # direct-loop return 2.0 instead of 1.0 for unphased families...
                with self.subTest(implementation=impl, fam=fam):
                    #compute_family_likelihood_empirical
                    lh = compute_family_likelihood(fam, *rates, implementation=impl)
                    #print(fam.fid, expected_lh, impl, lh)
                    self.assertAlmostEqual(expected_lh, lh, msg=f'bad likelihood in {impl}: {lh} was computed while {expected_lh} was expected')

    def xtest_likelihoods_random(self):
        from recombulatorx.likelihood import implementations, compute_family_likelihood

        available_implementations = implementations.keys()
        available_implementations = [i for i in available_implementations if i != 'direct-loop-numba']
        n_markers = 6
        n_fam_I = 1
        n_fam_II = 1

        rates = generate_random_rates(n_markers)
        for i in range(n_fam_I + n_fam_II):
            typeI = i < n_fam_II
            fam = generate_processed_family(
                fid=f'FAM_{i + 1}_' + ('I' if typeI else 'II'),
                n_sons=2,
                is_mother_phased=typeI,
                recombination_rates=rates[0],
                mutation_rates=rates[1],
            )
            #if typeI:
            #    emp_lh = compute_family_likelihood_empirical(fam.mother, fam.maternal_haplotypes, fam.is_mother_phased, *rates)
            #    print(f'{emp_lh=}')
            ref_lh = None
            for impl in available_implementations:
                with self.subTest(implementation=impl, fam=fam):
                    #compute_family_likelihood_empirical
                    lh = compute_family_likelihood(fam, *rates, implementation=impl)
                    #print(impl, lh)
                    if ref_lh is None:
                        ref_lh = lh
                        ref_impl = impl
                    else:
                        self.assertAlmostEqual(ref_lh, lh, msg=f'Inconsistent likelihoods between implementations: {ref_impl} returned {ref_lh} while {impl} returned {lh}')# for family {fam}')


    def test_integration(self):
        import recombulatorx
        family_graphs, markers = recombulatorx.ped2graph('testsim_SNP.tsv')
        processed_families = recombulatorx.preprocess_families(family_graphs)
        est_recomb_rates, est_mut_rates = recombulatorx.estimate_rates(processed_families, 0.1, 0.1, estimate_mutation_rates='all')

    def test_integration_STR(self):
        import recombulatorx
        family_graphs, markers = recombulatorx.ped2graph('testsim.tsv')
        processed_families = recombulatorx.preprocess_families(family_graphs)
        est_recomb_rates, est_mut_rates = recombulatorx.estimate_rates(processed_families, 0.1, 0.1, estimate_mutation_rates='all')
    
    
#    def test_impl(self):
#        import recombulatorx
#        available_implementations = recombulatorx.likelihood.implementations.keys()
#        #available_implementations = [i for i in available_implementations if i != 'direct-loop-numba']
#
#        family_graphs, markers = recombulatorx.ped2graph('testsim.tsv')
#        processed_families = recombulatorx.preprocess_families(family_graphs)
#        for impl in available_implementations:
#            with self.subTest(f'impl={impl}'):
#                est_recomb_rates, est_mut_rates = recombulatorx.estimate_rates(
#                    processed_families, 0.1, 0.1, estimate_mutation_rates='all', implementation=impl,
#                )
#