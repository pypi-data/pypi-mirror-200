from .families import preprocess_families
from .io import ped2graph
from .estimate import estimate_rates

def main(
    default_mutation_rate = 0.001,
):
    import argparse
    import logging

    parser = argparse.ArgumentParser(description='Estimate recombination and mutation rates.')
    parser.add_argument(
        'ped_path', metavar='PED', type=str, 
        help='path to ped file'
    )
    parser.add_argument(
        '--mutation-rates', metavar='MUT-RATE', default=[default_mutation_rate], type=float, nargs='+', 
        help=f'mutation rates used in the estimation, either as fixed or as starting point in the optimization depending on the value of the --estimate-mutation-rates option. If not given the rates are set to {default_mutation_rate} for all markers'
    )
    parser.add_argument(
        '--estimate-mutation-rates', default='no', choices=['no', 'one', 'all'],
        help='controls the estimation of the mutation rates. With "no" the mutation rates are not estimated, with "one" the same rate is estimated for all markers, with "all" a separate estimation rate is estimated for each marker. Defaults to  "no"'
    )


    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger('recombulator-x')
    #logging.basicConfig(filename='demo.log', level=logging.DEBUG)
    
    family_graphs, (marker_names, marker_types, marker_encoding) = ped2graph(args.ped_path)
    log.info(f'Read {len(family_graphs)} families with {len(marker_names)} markers from pedigree file.')

    if len(args.mutation_rates) == 1:
        starting_mutation_rates = args.mutation_rates[0]
    elif len(args.mutation_rates) == len(marker_names):
        starting_mutation_rates = args.mutation_rates
    else:
        parser.error(f'the number of mutation rates ({len(args.mutation_rates)}) must be one or equal to the number of markers ({len(marker_names)})')

    processed_families = preprocess_families(family_graphs)
    type_I = 0
    type_II = 0
    for fam in processed_families:
        if fam.is_mother_phased:
            type_I += 1
        else:
            type_II += 1

    log.info(f'Detected {len(processed_families)} informative families')
    log.info(f'Type I families (phased mother): {type_I}, type II families (unphased mother): {type_II}')
    log.info(f'Estimating rates...')
    estimated_rates = estimate_rates(processed_families, 0.1, starting_mutation_rates, estimate_mutation_rates=args.estimate_mutation_rates)
    
    print('TYPE', 'MARKER', 'RATE', sep='\t')

    if args.estimate_mutation_rates == 'no':
        est_recomb_rates = estimated_rates
    else:
        est_recomb_rates, est_mut_rates = estimated_rates
        if args.estimate_mutation_rates == 'one':
            print('MUTATION', '*', est_mut_rates, sep='\t')
        else:
            for m, r in zip(marker_names, est_mut_rates):
                print('MUTATION', m, r, sep='\t')

    for i, r in enumerate(est_recomb_rates):
        print('RECOMBINATION', marker_names[i] + '-' + marker_names[i + 1], r, sep='\t')
    log.info('DONE')

if __name__ == '__main__':
    main()
