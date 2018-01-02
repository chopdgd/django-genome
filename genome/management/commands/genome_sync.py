import logging

from django.core.management import BaseCommand, call_command


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sync Genome Database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--genome-build',
            choices=['hg18', 'hg19', 'hg38'],
            default='hg19',
            help='Genome build to load',
        )

    def handle(self, *args, **options):
        logger.info('Syncing {0}'.format(options['genome_build']))
        call_command('chromosome_sync', *args, **options)
        call_command('gene_sync', *args, **options)
        call_command('transcript_sync', *args, **options)
