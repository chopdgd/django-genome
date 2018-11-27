import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand

from genomix.utils import retrieve_compressed_data, retrieve_data

from genome import app_settings, choices, models, utils


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sync Genes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--genome-build',
            choices=['hg18', 'hg19', 'hg38'],
            default='hg19',
            help='Genome build to load',
        )

    def handle(self, *args, **options):
        genome = options['genome_build']
        resources = app_settings.RESOURCES.get(genome, {})

        # Download external resources
        logger.info('Downloading resources...')
        hgnc_data = retrieve_data(getattr(app_settings, 'HGNC_GENES'))
        kgXref_data = retrieve_compressed_data(resources.get('kgXref'))

        # Create Genome
        logger.info('Prepping Genome...')
        genome_obj, created = models.Genome.objects.get_or_create(label=genome)

        # Create Gene
        logger.info('Creating Genes from HGNC...')
        hgnc_header = [text.upper() for text in hgnc_data.pop(0).strip().split('\t')]

        for line in hgnc_data:
            hgnc_gene_data = line.split('\t')
            symbol = hgnc_gene_data[hgnc_header.index('APPROVED SYMBOL')]
            name = hgnc_gene_data[hgnc_header.index('APPROVED NAME')]
            hgnc_id = hgnc_gene_data[hgnc_header.index('HGNC ID')]
            status = hgnc_gene_data[hgnc_header.index('STATUS')]
            chromosome = hgnc_gene_data[hgnc_header.index('CHROMOSOME')]
            previous_name = hgnc_gene_data[hgnc_header.index('PREVIOUS NAME')]
            locus_type = hgnc_gene_data[hgnc_header.index('LOCUS TYPE')]
            locus_group = hgnc_gene_data[hgnc_header.index('LOCUS GROUP')]
            ensembl = hgnc_gene_data[hgnc_header.index('ENSEMBL GENE ID')]
            refseq = hgnc_gene_data[hgnc_header.index('REFSEQ IDS')]
            not_curated_ensembl = hgnc_gene_data[hgnc_header.index('ENSEMBL ID(SUPPLIED BY ENSEMBL)')]
            not_curated_refseq = hgnc_gene_data[hgnc_header.index('REFSEQ(SUPPLIED BY NCBI)')]
            not_curated_ucsc = hgnc_gene_data[hgnc_header.index('UCSC ID(SUPPLIED BY UCSC)')]
            not_curated_omim = hgnc_gene_data[hgnc_header.index('OMIM ID(SUPPLIED BY OMIM)')]
            not_curated_uniprot = hgnc_gene_data[hgnc_header.index('UNIPROT ID(SUPPLIED BY UNIPROT)')]
            not_curated_mouse_genome_database = hgnc_gene_data[
                hgnc_header.index('MOUSE GENOME DATABASE ID(SUPPLIED BY MGI)')]
            not_curated_rat_genome_database = hgnc_gene_data[
                hgnc_header.index('RAT GENOME DATABASE ID(SUPPLIED BY RGD)')]

            # normalize chromosome
            chromosome = utils.reformat_chromosome(chromosome)
            try:
                chromosome_obj = models.Chromosome.objects.get(
                    genome=genome_obj,
                    label=chromosome,
                )
            except ObjectDoesNotExist:
                chromosome_obj = None
            gene_obj, created = models.Gene.objects.update_or_create(
                symbol=symbol.upper(),
                chromosome=chromosome_obj,
                defaults={
                    'name': name,
                    'hgnc_id': hgnc_id.strip().split(':')[1],
                    'status': getattr(choices.HGNC_GENE_STATUS, status.lower().replace(' ', '_')),
                    'previous_name': previous_name,
                    'locus_type': locus_type,
                    'locus_group': locus_group,
                    'ensembl': ensembl,
                    'refseq': refseq,
                    'not_curated_ensembl': not_curated_ensembl,
                    'not_curated_refseq': not_curated_refseq,
                    'not_curated_ucsc': not_curated_ucsc,
                    'not_curated_omim': not_curated_omim,
                    'not_curated_uniprot': not_curated_uniprot,
                    'not_curated_mouse_genome_database': not_curated_mouse_genome_database,
                    'not_curated_rat_genome_database': not_curated_rat_genome_database,
                }
            )

            # Create GeneSynonym
            synonyms = hgnc_gene_data[
                hgnc_header.index('SYNONYMS')
            ].strip().split(',')
            previous_symbols = hgnc_gene_data[
                hgnc_header.index('PREVIOUS SYMBOLS')
            ].strip().split(',')

            for synonym in synonyms + previous_symbols:
                label = synonym.strip()
                if label:
                    synonym_obj, created = models.GeneSynonym.objects.update_or_create(label=label)
                    gene_obj.synonyms.add(synonym_obj)

            gene_obj.save()

        # Add missing genes from kgXref
        logger.info('Creating Genes from kgXref...')
        for line in kgXref_data:
            line = line.strip().split('\t')
            symbol = line[4]
            refseq = line[5]
            name = line[7]

            gene_obj, created = models.Gene.objects.update_or_create(
                symbol=symbol.upper(),
                defaults={
                    'refseq': refseq,
                    'name': name,
                    'status': getattr(choices.HGNC_GENE_STATUS, 'ucsc_gene')
                }
            )
