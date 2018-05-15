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
        parser.add_argument(
            '--sync-exons',
            action='store_true',
            help='Sync Exons',
        )

    def handle(self, *args, **options):
        logger.info('Syncing {0}'.format(options['genome_build']))
        sync_exons = options.pop('sync_exons')
        call_command('chromosome_sync', *args, **options)
        call_command('gene_sync', *args, **options)
        options.update({"sync_exons": sync_exons})
        call_command('transcript_sync', *args, **options)
