#!/usr/bin/env python
# coding: utf-8


import itertools
import numpy

########################################
# STRAIGHTFORWARD LOOP IMPLEMENTATIONS #
########################################

# This function is a numba compilable replacement for the standard itertools.product([0,1], repeat=n)
def inheritance_vectors(n: int):
    """Generate all possible inheritance vectors of length n
    """
    v = numpy.zeros(n, dtype=numpy.int8)
    for i in range(1 << n):
        for j in range(n):
            v[j] = 1 if i & (1 << j) else 0
        yield v # note that this is always the same vector, not a copy
    return v # this does nothing but is needed by numba

def compute_phased_family_likelihood_direct_loop(mother, maternal_haplotypes, recombination_rates, mutation_rates):
    """Faithful transcription of the original likelihood formula for a phased mother"""
    if numpy.any(mother < 0):
        raise ValueError('this likelihood function does not support non-STR markers')
    n = len(mother)
    family_lh = 1.0
    for son in maternal_haplotypes:
        son_lh = 0.0
        for v in inheritance_vectors(n):
            recomb_lh = 0.5 # choice of starting haplotype
            for i in range(n - 1):
                recomb_lh *= 1 - recombination_rates[i] if v[i] == v[i + 1] else recombination_rates[i]
            mut_lh = 1
            for i in range(n):
                if mother[i][v[i]] == son[i]:
                    mut_lh_i = 1 - mutation_rates[i]
                elif abs(mother[i][v[i]] - son[i]) == 1.0:
                    mut_lh_i = mutation_rates[i]
                else: # zero likelihood for non unit mutations
                    mut_lh = 0
                    break
                mut_lh *= mut_lh_i
            son_lh += recomb_lh*mut_lh
        family_lh *= son_lh
    return family_lh


def compute_unphased_family_likelihood_direct_loop(mother, maternal_haplotypes, recombination_rates, mutation_rates):
        n = len(mother)
        half = 2**(n - 1)
        phased_mother = numpy.zeros_like(mother)
        phase_lh = 0.0
        #for i, v in enumerate(inheritance_vectors(n)):
        i = 0
        for v in inheritance_vectors(n):
            # only use the first half of the inheritance vectors, 
            # otherwise we repeat the same phasings as in the first half 
            # with the mother's haplotypes inverted
            if i == half:
                break
            # phase mother as in the inheritance vector v
            for pos in range(n):
                phased_mother[pos, 0] = mother[pos, v[pos]]
                phased_mother[pos, 1] = mother[pos, 1 - v[pos]]
            phase_lh += compute_phased_family_likelihood_direct_loop(phased_mother, maternal_haplotypes, recombination_rates, mutation_rates)
        return phase_lh/half


# Compute all required arrays that only depends on the number of markers
def get_basic_arrays(n_marker):
    """
    n_marker: int
        The number of markers

    Returns:
    r: n
        The marker index vector [0, 1, ..., n - 1]



        Attributes:
        n: int
            Number of markers
        r: integer vector of length n
            Marker indexer, the vector [0, 1, ..., n - 1]
        inheritance_matrix: matrix of 2**n rows by n columns
            All possible recombinations of two n-marker haplotypes
        inheritance_probs: 
        mutations_probs:
     
    """
    r = numpy.array(list(range(n_marker)))
    inheritance_matrix = numpy.array(list(itertools.product([0,1], repeat=n_marker)))
    jump_matrix = numpy.abs(inheritance_matrix[:, 1:] - inheritance_matrix[:, :-1])
    return dict(r=r, inheritance_matrix=inheritance_matrix, jump_matrix=jump_matrix)


###########
# PHASING #
###########

def all_unique_phasings(mother, r, inheritance_matrix):
    """
    Compute all possible unique phasings given a diploid individual.
    
    Note that if the individual is homozygous for a marker we consider the two possible phasings of that marker to be indistinguishable and thus produce less than the 2**(n_markers - 1) maximum phasings.

    ------
    Parameters:
    mother: array of shape (n_markers, 2)
        maternal genotypes as columns, phased if possible (when grandfather is available)
    """
    homs = mother[:, 0] == mother[:, 1]
    uniq = numpy.all(inheritance_matrix[:, homs] == 0, axis=1)
    phasing_matrix = numpy.array_split(inheritance_matrix[uniq], 2)[0]
    mother_phases = numpy.dstack((mother[r, phasing_matrix], mother[r, 1 - phasing_matrix]))

    return mother_phases

# Daughter phasing
def phase_daughter_probs(daughter, father, r, inheritance_matrix, mutation_probs):
    if numpy.any(daughter < 0):
        raise ValueError('this function does not support non-STR markers')
    inherited_matrix = daughter[r, inheritance_matrix]
    mutation_matrix = numpy.abs(inherited_matrix - father).clip(0,2)
    mutation_llh = numpy.prod(mutation_probs[r, mutation_matrix], axis=-1)
    assert mutation_llh.max() > 0.5
    assert all(inherited_matrix[mutation_llh.argmax()] == father)
    father_phase = inheritance_matrix[mutation_llh.argmax()]
    return numpy.array([daughter[r, father_phase], daughter[r, 1 - father_phase]]).T


#####################################
# RECOMBINATION/MUTATION likelihood #
#####################################

def compute_probs(recombination_rates, mutation_rates, jump_matrix):
    """
    Compute probability matrices that depend on the recombination and mutation rates
    
    inheritance_probs: 2**n
    mutation_probs: 
    """
    assert len(recombination_rates) == len(mutation_rates) - 1
    probs = dict(
        inheritance_probs=numpy.prod( # the original R code sums to 2, not 1
            jump_matrix*recombination_rates +
            (1 - jump_matrix)*(1 - recombination_rates),
            axis=1)/2,
        mutation_probs=numpy.stack([
            1 - mutation_rates, 
            mutation_rates, 
            numpy.zeros_like(mutation_rates), # only allow one step mutations
            ]).T,
    )
    #assert numpy.abs(numpy.sum(probs['inheritance_probs']) - 1) < 0.0000001
    return probs

import functools

@functools.lru_cache(maxsize=1)
def precompute_probs_inner(recombination_rates, mutation_rates):
    """combine the previous two functions"""
    arrays = get_basic_arrays(len(recombination_rates) + 1)
    probs = compute_probs(numpy.array(recombination_rates), numpy.array(mutation_rates), arrays['jump_matrix'])
    arrays.update(probs)
    del arrays['jump_matrix']
    return arrays
def precompute_probs(recombination_rates, mutation_rates):
    return precompute_probs_inner(*map(tuple, [recombination_rates, mutation_rates]))


def compute_father_daughter_likelihood(father, daughters, r, inheritance_matrix, mutation_probs):
    # preprocessing
    daughters = numpy.array(daughters)
    
    # static computation
    # here we can allow a different number of phasings for each daughter because of homozigosity
    daughter_phasings = daughters[:, r, inheritance_matrix] # n daughters, 2**n_markers, n_markers
    mutation_matrix_f = numpy.abs(daughter_phasings - father.T[0]).clip(0, 2)
    mutation_matrix_i = mutation_matrix_f.astype(numpy.int8)
    
    assert numpy.all(mutation_matrix_f - mutation_matrix_i == 0), "non integer mutation found"


    # likelihood computation
    mutation_lh = numpy.prod(mutation_probs[r, mutation_matrix_i], axis=-1)
    
    family_lh = numpy.prod(numpy.sum(mutation_lh, axis=-1))
    assert family_lh <= 1, "compute_father_daughter_likelihood greater than 1!"

    return family_lh
 
def compute_family_likelihood_direct_numpy_inner(mother, maternal_haplotypes, is_mother_phased, r, inheritance_matrix, inheritance_probs, mutation_probs):
    """
    Compute likelihood of sons/phased daughters given the mother, accounting for both recombination and mutation.

    ------
    Parameters:
    mother: array of shape (n_markers, 2)
        maternal genotypes as columns, phased if possible (when grandfather is available)
    maternal_haplotypes: array of shape (n_haps, n_markers)
        maternal haplotypes of the mother's children as rows, from all sons and from those daughters whose father is genotyped and can thus be phased
    is_mother_phased: bool
        true when the mother genotypes have been phased
    r: array of shape (n_markers,)
    inheritance_matrix: array of shape (2**n_markers, n_markers)
    inheritance_probs: array of shape (2**n_markers,)
    mutation_probs: array of shape (n_markers, 3)

    Returns: scalar
        the likelihood of the children maternal halpotypes occurring from recombination and mutation for the given recombination and mutation probability matrices
    """
    if numpy.any(mother < 0):
        raise ValueError('this likelihood function does not support non-STR markers')
    # preprocessing part, only depends on genotype data

    # possible unique mother phasings, n markers, ploidity=2
    if is_mother_phased:
        # only one possible phasing of the mother
        mother_phases = mother[numpy.newaxis]
    else:
        # take all phasing of the mother (up to the order of the two haplotypes)
        mother_phases = all_unique_phasings(mother, r, inheritance_matrix)
    
    # possible unique mother phasings, possible recombinations, n markers
    inherited_matrix = mother_phases[:, r, inheritance_matrix]

    # mutation count capped at 2: possible unique mother phasings, possible recombinations, n maternal haplotypes, n markers
    mutation_matrix_f = numpy.abs(inherited_matrix[:, :, numpy.newaxis, :] - maternal_haplotypes).clip(0, 2)
    mutation_matrix_i = mutation_matrix_f.astype(numpy.int8)
    assert numpy.all(mutation_matrix_f - mutation_matrix_i == 0), "non integer mutation found"
    
    # mutation_matrix max shape: 2**(n-1), 2**n, n_sons, n
       
    
    # here we start using mutation and recombination probs

    # mutation likelihood: possible unique mother phasings, possible recombinations, n maternal haplotypes
    mutation_lh = numpy.prod(mutation_probs[r, mutation_matrix_i], axis=-1)
    # combined mutation and recombination likelihood: possible unique mother phasings, n maternal haplotypes
    combined_lh = numpy.sum(mutation_lh*inheritance_probs[:, numpy.newaxis], axis=1)
    # total family likelihood, product of independent maternal haplotypes and mean across possible mother phasings (mean since we assume an uniform prior on mother phasings): scalar
    family_lh = numpy.mean(numpy.prod(combined_lh, axis=1))

    #assert family_lh > 0, "zero likelihood for family"

    return family_lh

# since other methods have different functions for phased and unphased families we define two wrappers for uniformity
def compute_phased_family_likelihood_direct_numpy(mother, maternal_haplotypes, recombination_rates, mutation_rates):
    probs = precompute_probs(recombination_rates, mutation_rates)
    return compute_family_likelihood_direct_numpy_inner(mother, maternal_haplotypes, is_mother_phased=True, **probs)
def compute_unphased_family_likelihood_direct_numpy(mother, maternal_haplotypes, recombination_rates, mutation_rates):
    probs = precompute_probs(recombination_rates, mutation_rates)
    return compute_family_likelihood_direct_numpy_inner(mother, maternal_haplotypes, is_mother_phased=False, **probs)