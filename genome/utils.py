# -*- coding: utf-8
def reformat_chromosome(chromosome):
    chromosome = chromosome.replace('chr', '').replace('unplaced', '').upper().strip()
    accepted = list(map(str, range(1, 23))) + ['X', 'Y', 'M', 'MT']

    if chromosome not in accepted:
        if all(x in chromosome for x in ['P']):
            return chromosome.split('P')[0]
        elif all(x in chromosome for x in ['Q']):
            return chromosome.split('Q')[0]
        else:
            new_chromosome = chromosome.lower() \
                .replace('alternate reference locus', '') \
                .replace('mitochondria', 'M') \
                .replace('not on reference assembly', '') \
                .upper() \
                .strip()

            if new_chromosome in accepted:
                return new_chromosome
    else:
        return chromosome


def chromosome_number(chromosome):
    if chromosome in list(map(str, range(1, 23))):
        return int(chromosome)
    elif chromosome.upper() == 'X':
        return 23
    elif chromosome.upper() == 'Y':
        return 24
    elif chromosome.upper() in ['M', 'MT']:
        return 25
