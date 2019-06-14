import logging

from django.core.management import BaseCommand
from django.db import IntegrityError

from genome import app_settings, choices, models, utils
from genomix.utils import retrieve_data

from tqdm import tqdm


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sync Genome Database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--build',
            choices=['hg18', 'hg19', 'hg38'],
            default='hg19',
            help='Genome build to load',
        )
        parser.add_argument(
            '--sync-exons',
            action='store_true',
            help='Sync Exons. By default they are not synced.',
        )

    def handle(self, *args, **options):
        build = options['build']
        resources = app_settings.RESOURCES.get(build, {})
        description_url = resources.get('url', "")

        logger.info('Syncing {0}...'.format(build))
        genome, created = models.Genome.objects.update_or_create(
            label=build,
            defaults={'description_url': description_url}
        )
        self.sync_chromosomes(genome)

        chromosomes = self.get_chromosomes(genome)
        self.sync_cytobands(genome, chromosomes)
        self.sync_genes(genome, chromosomes)
        self.sync_transcripts(genome, chromosomes, sync_exons=options['sync_exons'])
        logger.info('Syncing {0} complete!'.format(build))

    @staticmethod
    def get_chromosomes(genome):
        chromosomes = {}
        for item in models.Chromosome.objects.filter(genome=genome):
            chromosomes[item.label] = item
        return chromosomes

    @staticmethod
    def get_chromosome(genome, chromosomes, value):
        if value:
            label = utils.reformat_chromosome(value)
            try:
                return chromosomes[label]
            except KeyError:
                logger.warning('Chromosome: {0} does not exist!'.format(value))

    def sync_chromosomes(self, genome):
        logger.info('Syncing chromosomes...')
        for row in tqdm(self.run_ucsc_query(genome, self.ucsc_chromosome_sql())):
            chromosome = utils.reformat_chromosome(row[0])
            models.Chromosome.objects.update_or_create(
                genome=genome,
                label=chromosome,
                defaults={'length': row[1]}
            )
        logger.info('Syncing chromosomes complete!')

    def sync_cytobands(self, genome, chromosomes):
        logger.info('Syncing cytobands...')
        for row in tqdm(self.run_ucsc_query(genome, self.ucsc_cytoband_sql())):
            chromosome = self.get_chromosome(genome, chromosomes, row[0])
            models.CytoBand.objects.update_or_create(
                label=row[3],
                chromosome=chromosome,
                defaults={
                    'start': row[1],
                    'end': row[2],
                    'stain': row[4],
                }
            )
        logger.info('Syncing cytobands complete!')

    def sync_genes(self, genome, chromosomes):
        logger.info('Syncing HGNC genes...')
        logger.info('Downloading from HGNC...')
        hgnc_data = retrieve_data(getattr(app_settings, 'HGNC_GENES'))
        logger.info('Downloading complete!')
        header = [text.upper() for text in hgnc_data.pop(0).strip().split('\t')]

        for line in tqdm(hgnc_data):
            columns = line.split('\t')
            symbol = columns[header.index('APPROVED SYMBOL')]
            name = columns[header.index('APPROVED NAME')]
            hgnc_id = columns[header.index('HGNC ID')]
            status = columns[header.index('STATUS')]
            chromosome = columns[header.index('CHROMOSOME')]
            previous_name = columns[header.index('PREVIOUS NAME')]
            locus_type = columns[header.index('LOCUS TYPE')]
            locus_group = columns[header.index('LOCUS GROUP')]
            ensembl = columns[header.index('ENSEMBL GENE ID')]
            refseq = columns[header.index('REFSEQ IDS')]
            not_curated_ensembl = columns[header.index('ENSEMBL ID(SUPPLIED BY ENSEMBL)')]
            not_curated_refseq = columns[header.index('REFSEQ(SUPPLIED BY NCBI)')]
            not_curated_ucsc = columns[header.index('UCSC ID(SUPPLIED BY UCSC)')]
            not_curated_omim = columns[header.index('OMIM ID(SUPPLIED BY OMIM)')]
            not_curated_uniprot = columns[header.index('UNIPROT ID(SUPPLIED BY UNIPROT)')]
            not_curated_mouse_genome_database = columns[
                header.index('MOUSE GENOME DATABASE ID(SUPPLIED BY MGI)')]
            not_curated_rat_genome_database = columns[
                header.index('RAT GENOME DATABASE ID(SUPPLIED BY RGD)')]

            chromosome = self.get_chromosome(genome, chromosomes, chromosome)
            gene, created = models.Gene.objects.update_or_create(
                symbol=symbol.upper(),
                chromosome=chromosome,
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

            synonyms = columns[header.index('SYNONYMS')].strip().split(',')
            previous_symbols = columns[header.index('PREVIOUS SYMBOLS')].strip().split(',')

            for synonym in synonyms + previous_symbols:
                label = synonym.strip()
                if label:
                    synonym, created = models.GeneSynonym.objects.update_or_create(label=label.upper())
                    gene.synonyms.add(synonym)

            gene.save()
        logger.info('Syncing HGNC genes complete!')

    def sync_transcripts(self, genome, chromosomes, sync_exons=False):
        message = 'Syncing RefSeq transcripts'
        if sync_exons:
            message += ' and exons'
        logger.info('{0}...'.format(message))

        for row in tqdm(self.run_ucsc_query(genome, self.ucsc_refgene_sql())):
            chromosome = self.get_chromosome(genome, chromosomes, row[10])
            gene, created = models.Gene.objects.get_or_create(
                chromosome__genome=genome,
                symbol=row[0].upper(),
                defaults={
                    'status': getattr(choices.HGNC_GENE_STATUS, 'ucsc_gene'),
                    'chromosome': chromosome,
                }
            )

            try:
                transcript, created = models.Transcript.objects.update_or_create(
                    label=row[1],
                    gene=gene,
                    defaults={
                        'strand': getattr(choices.STRAND_TYPES, row[2]),
                        'transcription_start': row[3],
                        'transcription_end': row[4],
                        'cds_start': row[5],
                        'cds_end': row[6],
                    }
                )
            except IntegrityError:
                logger.warning('Transcript: {0} was skipped!'.format(row[1]))
                continue

            if sync_exons:
                strand = row[2]
                number_of_exons = row[7]
                starts = [int(x) for x in row[8].strip().split(',') if x]
                ends = [int(x) for x in row[9].strip().split(',') if x]

                for index, exon in enumerate(starts):
                    if strand == '+':  # NOTE: Positive strand exons count forward
                        number = index + 1
                    elif strand == '-':  # NOTE: Negative strand exons count reverse
                        number = number_of_exons - index
                    else:
                        raise ValueError('strand: {0} is not supported!'.format(strand))

                    models.Exon.objects.update_or_create(
                        number=number,
                        transcript=transcript,
                        defaults={
                            'start': starts[index],
                            'end': ends[index],
                        }
                    )
        logger.info('{0} complete!'.format(message))

    def run_ucsc_query(self, genome, query):
        logger.info('Querying UCSC...')
        build = genome.label
        conn = self.ucsc_connection(build)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        logger.info('Querying UCSC complete!')
        return rows

    @staticmethod
    def ucsc_connection(genome):
        import MySQLdb
        from MySQLdb.constants import FIELD_TYPE
        conv = {FIELD_TYPE.LONG: int}
        return MySQLdb.connect(
            host='genome-mysql.cse.ucsc.edu',
            user='genome',
            passwd='',
            db=genome,
            conv=conv
        )

    @staticmethod
    def ucsc_chromosome_sql():
        sql = """SELECT chrom, size FROM chromInfo WHERE LENGTH(chrom) < 6;"""
        logger.debug(sql)
        return sql

    @staticmethod
    def ucsc_cytoband_sql():
        sql = """SELECT chrom, chromStart, chromEnd, name, gieStain FROM cytoBand;"""
        logger.debug(sql)
        return sql

    @staticmethod
    def ucsc_refgene_sql():
        sql = """SELECT
            rg.name2,
            CONCAT(rg.name,'.',gi.version) as 'name',
            rg.strand,
            rg.txStart,
            rg.txEnd,
            rg.cdsStart,
            rg.cdsEnd,
            rg.exonCount,
            rg.exonStarts,
            rg.exonEnds,
            rg.chrom
        FROM hg19.refGene rg
        INNER JOIN hgFixed.gbCdnaInfo gi ON rg.name=gi.acc;
        """
        logger.debug(sql)
        return sql
