# set environment

import numpy
import networkx
import logging
from .types import ProcessedFamily
from .likelihood import compute_family_likelihood

# Function for checking family graphs and raising eventual errors
def check_family_graph(fid, G):
    '''Check that a family graph is consistent.
    
    Checks that there are no unconnected individuals and that individuals have at most two parents with different sex.
    '''
    if not networkx.is_weakly_connected(G):
        logging.warning(f"found unrelated individuals in family {fid}")
    rG = G.reverse()
    for node in rG:
        parent_sex = [G.nodes[n]['sex'] for n in rG.neighbors(node)]
        #assert len(parent_sex) <= 2
        #assert len(set(parent_sex)) == len(parent_sex)
        if len(parent_sex) > 2:
            raise ValueError(f"more than two parents in family {fid}!")
        if len(set(parent_sex)) != len(parent_sex):
            raise ValueError(f"same sex parent in family {fid}!")

# Plotting function
def plot_family_graph(G, title=None):
    """Plot a family graph.
    
    Requires the matplotlib module.
    
    G: networkx.DiGraph
        family graph
    title: str
        plot title
    
    Returns: matplotlib.Figure
        the family plot
    """
    import matplotlib.pyplot as plt
    fig = plt.figure()
    plt.plot()
    plt.tight_layout()
    #x1,x2,y1,y2 = plt.axis()
    #plt.axis((x1-2,x2+2,y1-2,y2+2))
    #networkx.draw_shell(G, with_labels=True, font_weight='bold')
    color_map = []
    for node in G:
        if G.nodes[node]['sex'] == 'female':
            color_map.append('pink')
        else:
            color_map.append('cornflowerblue')
    #pos = graphviz_layout(G, prog='dot')
    networkx.draw(G, with_labels=True, arrows=True, node_color = color_map, node_size=1000, font_size=8)
    if title:
        plt.title(title)
    #plt.show()
    return fig

# Function for getting the father and (below) function for getting the parents of sample i
def get_father(i, G):
    #l = [item for item in G.predecessors(i) if 'XY' == item[1]]
    l = [item for item in G.predecessors(i) if 'male' == G.nodes[item]['sex']]
    assert len(l) <= 1
    return l[0] if l else None

#print(get_father('F2_FIGLIA 1', fams[1][1]))

def get_parents(i, G):
    mother, father = None, None
    for y in G.predecessors(i):
        if G.nodes[y]['sex'] == 'female':
            assert mother is None
            mother = y
        elif G.nodes[y]['sex'] == 'male':
            assert father is None
            father = y
        else:
            raise ValueError('bad sex: ' + y[1])
    return mother, father

## check if it's correct
# Function for counting Type I Type II families
def count_families(G):
    typeI = []
    typeII = []
    for f in G.nodes:
        if G.nodes[f]['sex'] == 'female':
            sons = [item for item in G.successors(f) if G.nodes[item]['sex'] == 'male']
            daughters_with_father = [item for item in G.successors(f) if G.nodes[item]['sex'] == 'female' and get_father(item, G)]
            children = sons + daughters_with_father
            if children:
                father = get_father(f, G)
                if father:
                    typeI.append('Type I: {} {} {}'.format(father, f, children))
                elif len(children) >= 2:
                    typeII.append('Type II: {} {}'.format(f, children))
    return typeI, typeII

# Function for retrieving genotypes? check the output in the chunk below
# We should decide how to code the marker names (A1 and A2?)
# è un problema che markers non viene definito nella funzione?

def get_father_geno(
        family: networkx.DiGraph, 
        iid: str,
    ):
    """
    Get iid's father genotype.

    family: networkx.DiGraph
        the family graph
    iid: str
        the name of the individual whose father we are retrieving
    
    Returns:
        the father genotype or None if the father is not in the family graph
    """
    for parent in family.predecessors(iid):
        if family.nodes[parent]['sex'] == 'male':
            return family.nodes[parent]['geno']
    return None

class AmbiguousPhasingError(Exception):
    pass
class FamilyNotInformativeError(Exception):
    pass

def extract_informative_subfamilies(families):
    """
    Extract informative subfamilies from a family graph.

    For recombination, informative subfamilies are either those with:
    - a phased mother and at least one son or phased daughter, called type I families
    - an unphased mother and at least two between sons and phased daughters, called type II families
    Females can be phased when their father is available. Note that these families are informative also for mutation.

    For mutation, informative families are composed by FIXME

    """
    recombination_subfams = []
    mutation_subfams = []
    for fid, G in families:
        for iid in G.nodes:
            sub_fid = fid, iid # sub family id
            if G.nodes[iid]['sex'] == 'female': # we start by finding a possible mother with children
                mother = iid
                # if available, the grandfather allows to phase the mother
                grandfather = get_father_geno(G, mother)

                # recombination can be observed from the maternal haplotypes in the male children
                # if the father is available, also the maternal halpotype can be recovered also from female children 
                sons = []
                daughters_with_father = []
                for child_name in G.successors(mother):
                    child = G.nodes[child_name]
                    if child['sex'] == 'male':
                        sons.append(child['geno'])
                    else:
                        assert child['sex'] == 'female'
                        father_name = get_father(child_name, G)
                        if father_name is not None:
                            daughter_father = G.nodes[father_name]['geno']
                            daughters_with_father.append((child['geno'], daughter_father))
                maternal_haplotype_num = len(sons) + len(daughters_with_father)
                if grandfather is not None and maternal_haplotype_num > 0:
                    ftype = 'typeI'
                elif maternal_haplotype_num > 1:
                    ftype = 'typeII'
                else: continue

                recombination_subfams.append(dict(
                        fid=sub_fid,
                        ftype=ftype,
                        mother=G.nodes[mother]['geno'],
                        grandfather=grandfather,
                        sons=sons,
                        daughters_with_father=daughters_with_father,
                    ))
            elif G.nodes[iid]['sex'] == 'male':
                daughters = []
                for child_name in G.successors(iid):
                    child = G.nodes[child_name]
                    if child['sex'] == 'female':
                        daughters.append(child['geno'])

                if len(daughters) == 0: continue

                mutation_subfams.append(dict(
                    fid=sub_fid,
                    ftype='typeIII',
                    father=G.nodes[iid]['geno'],
                    daughters=daughters,
                ))
    return recombination_subfams, mutation_subfams


def phase_daughter(daughter, father, r, inheritance_matrix):
    """
    Phase a daughter using the father haplotype.

    Returns the phased daughter with the paternal haplotype first and the number of differences (mutations) with the father haplotype
    """
    inherited_matrix = daughter[r, inheritance_matrix]
    mutation_count = numpy.sum(numpy.abs(inherited_matrix - father.T), axis=-1)
    #if mutation_count.min() > 0:
    #    print('mutation in phasing: {} {} {}'.format(mutation_count.min(), inherited_matrix[mutation_count.argmin()], father))
    ambiguous = numpy.unique(inherited_matrix[mutation_count == mutation_count.min()], axis=0)
    if ambiguous.shape[0] > 1:
        raise AmbiguousPhasingError('ambiguous phasing:'.format(ambiguous))
    father_phase = inheritance_matrix[mutation_count.argmin()]
    return numpy.array([daughter[r, father_phase], daughter[r, 1 - father_phase]]).T, mutation_count.min()


def preprocess_family(fam, r, inheritance_matrix, max_phasing_muts=0):
    fid = fam['fid']
    mother = fam['mother']
    is_mother_phased = False
    try:
        if fam['grandfather'] is not None:
            mother, muts = phase_daughter(mother, fam['grandfather'], r, inheritance_matrix)
            is_mother_phased = True
        #if muts > 0:
        #    logging.warning('muts!') #FIXME
    except AmbiguousPhasingError: 
        logging.warning(f'family {fid} demoted from type I to type II since the mother '\
            'cannot be unambiguously phased from the grandfather because of mutations') 
            # here we could instead produce an intermediate type II family with only the possible phasings (in pratice this should happen very little)

    maternal_haps = [s[:, 0] for s in fam['sons']]
    for daughter, father in fam['daughters_with_father']:
        try:
            daughter, muts = phase_daughter(daughter, father, r, inheritance_matrix)
            maternal_haps.append(daughter[:, 1])
        #    if muts > 0:
        #        logging.warning('muts!') #FIXME
        except AmbiguousPhasingError:
            logging.warning(f'discarded one daughter in family {fid} who cannot be unambiguously phased from the father because of mutations')

    # drop children with incompatible genotypes
    n = mother.shape[0]
    rates = numpy.full(n - 1, 0.5), numpy.full(n, 0.1)
    maternal_haps_ok = []
    for hap in maternal_haps:
        hapfam = ProcessedFamily(
            fid=fid,
            mother=mother,
            is_mother_phased=True, 
            maternal_haplotypes=numpy.stack([hap]),
        )
        lh = compute_family_likelihood(hapfam, *rates)
        if lh == 0:
            logging.warning(f'discarded one child with incompatible genotypes in family {fid}')
        else:
            maternal_haps_ok.append(hap)

    if len(maternal_haps_ok) < (1 if is_mother_phased else 2):
        raise FamilyNotInformativeError()

    processed = ProcessedFamily(
        fid=fam['fid'],
        mother=mother,
        is_mother_phased=is_mother_phased,
        maternal_haplotypes=numpy.stack(maternal_haps_ok),
    )

    return processed

from .likelihood_direct import get_basic_arrays # maybe remove all dependecies from likelyhood_direct?
def preprocess_families(family_graphs):
    """Preprocess family graphs for rates estimation.
    
    Does the following preprocessing steps:
    - checks the consistency of the parsed family graphs,
    - finds all the informative subfamilies from each family,
    - phases all females using their father when available,
    - packs the inherited maternal haplotypes into a matrix
    
    family_graphs: sequence of tuples (str, networkx.DiGraph)
        sequence of tuples of family IDs and family graphs
    
    Returns: list of ProcessedFamily
        the preprocessed families
    """
    for fid, G in family_graphs:
        check_family_graph(fid, G)
    recomb_fams, mut_fams = extract_informative_subfamilies(family_graphs) # we are ignoring mut_fams!
    from collections import Counter
    c = Counter(f['ftype'] for f in recomb_fams)

    logging.info(f'detected potential {c["typeI"]} type I families and {c["typeII"]} type II families')

    p = get_basic_arrays(recomb_fams[0]['mother'].shape[0])
    processed_families = []
    for fam in recomb_fams:
        try:
            processed_families.append(preprocess_family(fam, p['r'], p['inheritance_matrix']))
        except FamilyNotInformativeError: # recoverable errors have already been handled, here we discard the family
            fid = fam['fid']
            logging.warning(f'family {fid} was discarded since it is not informative!')
    return processed_families


