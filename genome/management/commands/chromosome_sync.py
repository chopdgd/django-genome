import logging

from django.core.management import BaseCommand

from genomix.utils import retrieve_compressed_data, retrieve_data

from genome import app_settings, models, utils


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sync Chromosomes'

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
        description_url = resources.get('url', "")

        # Download external resources
        logger.info('Downloading resources...')
        chromosome_data = retrieve_data(resources.get('chromosomes'))
        cytoband_data = retrieve_compressed_data(resources.get('cytoband'))

        # Create Genome
        logger.info('Creating Genome...')
        genome_obj, created = models.Genome.objects.get_or_create(
            label=genome,
            defaults={'description_url': description_url}
        )

        # Create Chromosome
        logger.info('Creating Chromosomes...')
        for line in chromosome_data:
            (label, length) = line.strip().split('\t')

            # NOTE: This is to remove weird Chromosomes
            new_label = utils.reformat_chromosome(label)
            if new_label:
                chrom_obj, created = models.Chromosome.objects.get_or_create(
                    label=new_label,
                    genome=genome_obj,
                    defaults={'length': length, }
                )

        # Create CytoBand
        logger.info('Creating CytoBands...')
        for line in cytoband_data:
            (chromosome, start, end, label, stain) = line.strip().split('\t')

            # NOTE: This is to remove weird Chromosomes
            new_chromosome = utils.reformat_chromosome(chromosome)
            if new_chromosome:
                chrom_obj = models.Chromosome.objects.get(
                    label=new_chromosome,
                    genome=genome_obj,
                )

                cytoband_obj, created = models.CytoBand.objects.get_or_create(
                    label=label,
                    chromosome=chrom_obj,
                    defaults={
                        'start': start,
                        'end': end,
                        'stain': stain,
                    }
                )
