# -*- coding: utf-8
def reformat_chromosome(chromosome):
    if 'p' in chromosome:
        new_chrom = chromosome.split('p')[0].upper()
    elif 'q' in chromosome:
        new_chrom = chromosome.split('q')[0].upper()
    else:
        new_chrom = chromosome.replace('chr', '').upper()

    if new_chrom in list(map(str, range(1, 23))) or new_chrom in ['X', 'Y', 'M', 'MT']:
        return new_chrom


def chromosome_number(chromosome):
    if chromosome in list(map(str, range(1, 23))):
        return int(chromosome)
    elif chromosome.upper() == 'X':
        return 23
    elif chromosome.upper() == 'Y':
        return 24
    elif chromosome.upper() in ['M', 'MT']:
        return 25
