import logging

from django.apps import apps
from django.core.management import BaseCommand
from django.db.models import Q


logger = logging.getLogger(__name__)

Transcript = apps.get_model(app_label='genome', model_name='Transcript')
Genome = apps.get_model(app_label='genome', model_name='Genome')


class Command(BaseCommand):
    help = 'Sync Preferred Transcripts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--genome-build',
            choices=['hg18', 'hg19', 'hg38'],
            default='hg19',
            help='Genome build to load',
        )
        parser.add_argument(
            'preferred_transcript_mapping',
            help='Preferred Transcript TSV file'
        )

    def handle(self, *args, **options):
        genome = Genome.objects.get(label=options['genome_build'])
        preferred_transcript_mapping = open(options['preferred_transcript_mapping'], 'r')

        for mapping in preferred_transcript_mapping:
            columns = mapping.strip().split('.')
            preferred_transcript = columns[0]

            Transcript.objects.filter(
                Q(gene__chromosome__genome=genome) & Q(label__iexact=preferred_transcript)
            ).update(preferred_transcript=True)
