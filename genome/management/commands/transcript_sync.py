import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand

from genomix.utils import retrieve_compressed_data

from genome import app_settings, choices, models


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sync Transcripts'

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
        refgene_data = retrieve_compressed_data(resources.get('refgene'))

        # Create Transcript
        logger.info('Creating Transcripts and Exons from refGene...')
        for line in refgene_data:
            line = line.strip().split('\t')
            label = line[1]
            strand = line[3]
            transcription_start = int(line[4])
            transcription_end = int(line[5])
            cds_start = int(line[6])
            cds_end = int(line[7])
            symbol = line[12].upper()

            try:
                gene_obj = models.Gene.objects.get(symbol__iexact=symbol)
            except ObjectDoesNotExist:
                # NOTE: We skip weird genes like LOC, etc...
                continue

            transcript_obj, created = models.Transcript.objects.get_or_create(
                label=label,
                gene=gene_obj,
                defaults={
                    'strand': getattr(choices.STRAND_TYPES, strand),
                    'transcription_start': transcription_start,
                    'transcription_end': transcription_end,
                    'cds_start': cds_start,
                    'cds_end': cds_end,
                }
            )

            # Create Exon
            exon_starts = [int(x) for x in line[9].strip().split(',') if x]
            exon_ends = [int(x) for x in line[10].strip().split(',') if x]
            number_of_exons = int(line[8])
            for index, exon in enumerate(exon_starts):

                if strand == '+':  # NOTE: Positive strand exons count forward
                    number = index + 1

                elif strand == '-':  # NOTE: Negative strand exons count reverse
                    number = number_of_exons - index
                else:
                    raise ValueError('strand: {0} is not supported!'.format(strand))

                exon_obj, created = models.Exon.objects.get_or_create(
                    number=number,
                    transcript=transcript_obj,
                    start=exon_starts[index],
                    end=exon_ends[index],
                )
