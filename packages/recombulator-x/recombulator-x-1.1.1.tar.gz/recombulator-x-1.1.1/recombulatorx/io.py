import numpy
import pandas
from networkx import DiGraph 

def ped2graph(path):
    """
    This function takes a pedigree file as input and encodes it as graphs.
    
    The pedigree file can be a table in .ped format (headerless and space-separated),
    in .tsv format (with header and tab-separated) or in .xlsx format (experimental).
    The format is inferred by the extension.
    
    The graphs are DiGraphs objects from the networkx module, where each node is an
    individual and edges go from parent to child. The nodes include individual information
    (sex and genotypes) as attributes.
    
    IMPORTANT: markers must be sorted by genomic position, since we assume that recombination
    happens between adjacent markers.
    
    path: str
        path to the pedigree file
    
    Returns: tuple
        a list of tuples (family ID, DiGraphs) for each family ID in the pedigree file and 
        a list of marker names.
    """

    # read pedigree data
    if path.endswith('.tsv'):
        tab = pandas.read_csv(path, sep='\t', dtype=str, na_values=['0'], index_col=False)
    elif path.endswith('.xlsx'):
        tab = pandas.read_excel(path)
    else: # ped
        tab = pandas.read_csv(path, sep='\s+', dtype=str, na_values=['0'], index_col=False, header=None)
        assert tab.shape[1] > 6 and tab.shape[1] % 2 == 0
        n_markers = int((tab.shape[1] - 6)/2)
        tab.columns = [
                'FID', 'IID', 'PAT', 'MAT', 'SEX', 'PHENO'
            ] + [
                f'M{marker}-A{allele}' for marker in range(n_markers) for allele in range(2)
        ]

    # check even number of columns
    assert tab.shape[1] > 6 and tab.shape[1] % 2 == 0

    #tab.iloc[:, 6:] = tab.iloc[:, 6:].astype(float)

    hap1_markers = tab.columns[6::2]
    hap2_markers = tab.columns[7::2]
    marker_names = [col.split('-')[0] for col in hap1_markers] # FIXME: marker names
    
    # recode sex
    possible_sex_codings = [
        ['XY', 'XX'],
        ['1', '2'],
        ['M', 'F'],
        ['MALE', 'FEMALE'],
    ]
    orig_sex = tab['SEX'].str.upper()
    for sex_coding in possible_sex_codings:
        if orig_sex.isin(sex_coding).all():
            tab['SEX'] = orig_sex.replace(sex_coding, ['male', 'female'])
            break
    else:
        values = tab['SEX'].value_counts(sort=True).index.tolist()
        value_str = ', '.join(map(repr, values[:5]))
        if len(values) > 5:
            value_str += '...' 
        raise ValueError(f'Unknown values {value_str} in SEX column of "{path}"')

    marker_types = [None]*len(marker_names)
    nonstr_coding = {b: i for i, b in enumerate('ACGT', 1)}

    # get graph nodes and edges
    fams_list = []
    for fid, fam in tab.groupby('FID'):
        #fam_dict = {}
        G = DiGraph()
        family_iids = set(fam['IID'])

        for _, row in fam.iterrows():
            iid = row.at['IID']
            pat = row.at['PAT']
            mat = row.at['MAT']        
            
            # parse genotypes
            if row.at['SEX'] == 'female':
                haps = [
                    row.loc[hap1_markers],
                    row.loc[hap2_markers],
                ]
            else:
                haps = [row.loc[hap1_markers]]

            def parse_haplotype(hap, nonstr_coding):
                # parse alleles and detect STR or OTHER allele type
                parsed_haplotype = []
                for i, a in enumerate(hap):
                    try:
                        detected_marker_type = 'STR'
                        c = float(a)
                    except:
                        detected_marker_type = 'OTHER'
                        c = -nonstr_coding.setdefault(a, max(nonstr_coding.values()) + 1)
                    if marker_types[i] is None:
                        # infer marker type from the first observed haplotype
                        marker_types[i] = detected_marker_type
                    elif marker_types[i] != detected_marker_type:
                        # marker type cannot change between samples/haplotypes
                        raise ValueError(f"Inconsistent maker type for marker {marker_names[i]}, expected {marker_types[i]}, detected {detected_marker_type}")
                    parsed_haplotype.append(c)
                return parsed_haplotype
            geno = numpy.array([parse_haplotype(h, nonstr_coding) for h in haps]).T

            G.add_node(iid, sex=row.at['SEX'], geno=geno)
            if not pandas.isnull(pat):
                if pat not in family_iids:
                    raise IOError(f'The father "{pat}" of "{iid}" is not in family "{fid}"')
                G.add_edge(pat, iid)
            if not pandas.isnull(mat):
                if mat not in family_iids:
                    raise IOError(f'The mother "{mat}" of "{iid}" is not in family "{fid}"')
                G.add_edge(mat, iid)
    
        fam_tuple = (fid, G)
        fams_list.append(fam_tuple)

    return fams_list, (marker_names, marker_types, nonstr_coding)

