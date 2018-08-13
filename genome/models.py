# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from genomix.models import TimeStampedLabelModel
from model_utils.models import TimeStampedModel

from . import choices, managers


class Genome(TimeStampedLabelModel):
    """Genome Reference Build.

    Source: Downloaded from: https://www.ncbi.nlm.nih.gov/grc
    """
    description_url = models.URLField(blank=True)

    class Meta:
        verbose_name = _('Genome Build')
        verbose_name_plural = _('Genome Builds')


class Chromosome(TimeStampedModel):
    """Chromosome.

    Source: hg18 http://hgdownload.soe.ucsc.edu/goldenPath/hg18/bigZips/hg18.chrom.sizes
    Source: hg19 http://hgdownload.soe.ucsc.edu/goldenPath/hg19/bigZips/hg19.chrom.sizes
    Source: hg38 http://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.chrom.sizes
    """
    label = models.CharField(max_length=2)
    genome = models.ForeignKey(
        'genome.Genome',
        related_name='chromosomes',
        on_delete=models.CASCADE,
    )
    length = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Chromosome')
        verbose_name_plural = _('Chromosomes')
        unique_together = ('genome', 'label')

    def __str__(self):
        return self.label

    def save(self, **kwargs):
        self.label = self.label.upper()
        super(Chromosome, self).save(**kwargs)


class CytoBand(TimeStampedModel):
    """Cytogenetic Band.

    Source: hg18 http://hgdownload.soe.ucsc.edu/goldenPath/hg18/database/cytoBand.txt.gz
    Source: hg19 http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/cytoBand.txt.gz
    Source: hg38 http://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/cytoBand.txt.gz
    """
    label = models.CharField(max_length=20)
    chromosome = models.ForeignKey(
        'genome.Chromosome',
        related_name='cytobands',
        on_delete=models.CASCADE,
    )
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()
    stain = models.CharField(max_length=10)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Cytogenetic Band')
        verbose_name_plural = _('Cytogenetic Bands')

    def __str__(self):
        return self.label

    @property
    def locus(self):
        return 'chr{0}:{1}-{2}'.format(self.chromosome, self.start, self.end)


class Gene(TimeStampedModel):
    """Gene.

    Source: http://www.genenames.org/cgi-bin/download
    Custom Query: http://tinyurl.com/mqot6vl
    """
    symbol = models.CharField(max_length=255, db_index=True)
    name = models.TextField(blank=True)
    hgnc_id = models.PositiveIntegerField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=choices.HGNC_GENE_STATUS)
    active = models.BooleanField(default=True)
    chromosome = models.ForeignKey(
        'genome.Chromosome',
        related_name='genes',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    previous_name = models.TextField(blank=True)
    synonyms = models.ManyToManyField(
        'genome.GeneSynonym',
        blank=True,
        related_name='genes',
    )

    locus_type = models.CharField(max_length=100, blank=True)
    locus_group = models.CharField(max_length=100, blank=True)

    ensembl = models.TextField(blank=True)
    refseq = models.TextField(blank=True)

    # Not curated by HGNC staff.  These are provided by exeternal resources
    not_curated_ensembl = models.TextField(
        verbose_name='Ensembl ID (supplied by Ensembl)',
        blank=True,
    )
    not_curated_refseq = models.TextField(
        verbose_name='RefSeq (supplied by NCBI)',
        blank=True,
    )
    not_curated_ucsc = models.TextField(
        verbose_name='UCSC ID (supplied by UCSC)',
        blank=True,
    )
    not_curated_omim = models.TextField(
        verbose_name='OMIM ID (supplied by OMIM)',
        blank=True,
    )
    not_curated_uniprot = models.TextField(
        verbose_name='UniProt ID (supplied by UniProt)',
        blank=True,
    )
    not_curated_mouse_genome_database = models.TextField(
        verbose_name='Mouse Genome Database ID (supplied by MGI)',
        blank=True,
    )
    not_curated_rat_genome_database = models.TextField(
        verbose_name='Rat Genome Database ID (supplied by RGD)',
        blank=True,
    )

    objects = managers.GeneQuerySet.as_manager()

    class Meta:
        verbose_name = _('Gene')
        verbose_name_plural = _('Genes')
        unique_together = ('chromosome', 'symbol')

    def __str__(self):
        return self.symbol

    def save(self, **kwargs):
        self.symbol = self.symbol.upper()
        super(Gene, self).save(**kwargs)

    @staticmethod
    def build_urls(url, field):
        if field:
            return [
                '{0}{1}'.format(url, value.strip())
                for value in field.strip().split(',')
            ]

    @property
    def ensembl_urls(self):
        return self.build_urls(
            'http://www.ensembl.org/Homo_sapiens/Gene/Summary?g=',
            self.not_curated_ensembl,
        )

    @property
    def refseq_urls(self):
        return self.build_urls(
            'https://www.ncbi.nlm.nih.gov/gene/?term=',
            self.not_curated_refseq,
        )

    @property
    def omim_urls(self):
        return self.build_urls(
            'https://www.omim.org/entry/',
            self.not_curated_omim,
        )

    @property
    def uniprot_urls(self):
        return self.build_urls(
            'http://www.uniprot.org/uniprot/',
            self.not_curated_uniprot,
        )

    @property
    def mgi_urls(self):
        return self.build_urls(
            'http://www.informatics.jax.org/marker/MGI:',
            self.not_curated_mouse_genome_database,
        )

    @property
    def rgd_urls(self):
        return self.build_urls(
            'http://rgd.mcw.edu/rgdweb/report/gene/main.html?id=',
            self.not_curated_rat_genome_database,
        )

    @property
    def ensembl_gene_id(self):
        ids = []

        if self.ensembl:
            ids.append(self.ensembl)

        if self.not_curated_ensembl:
            ids.extend(self.not_curated_ensembl.split(','))

        if len(ids) > 0:
            return ids[0]


class GeneSynonym(TimeStampedModel):
    """Other symbols used to refer to a Gene."""
    label = models.CharField(max_length=255, unique=True, db_index=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Gene Synonym')
        verbose_name_plural = _('Gene Synonyms')

    def __str__(self):
        return self.label


class Transcript(TimeStampedModel):
    """"Gene Transcript.

    Source: hg18 http://hgdownload.soe.ucsc.edu/goldenPath/hg18/database/refGene.txt.gz
    Source: hg19 http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz
    Source: hg38 http://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/refGene.txt.gz
    """
    label = models.CharField(max_length=255, unique=True, db_index=True)
    active = models.BooleanField(default=True)
    gene = models.ForeignKey(
        'genome.Gene',
        on_delete=models.CASCADE,
        related_name='transcripts',
    )
    strand = models.PositiveSmallIntegerField(choices=choices.STRAND_TYPES)

    transcription_start = models.PositiveIntegerField()
    transcription_end = models.PositiveIntegerField()

    cds_start = models.PositiveIntegerField()
    cds_end = models.PositiveIntegerField()

    preferred_transcript = models.BooleanField(default=False)

    objects = managers.TranscriptQuerySet.as_manager()

    class Meta:
        verbose_name = _('Transcript')
        verbose_name_plural = _('Transcripts')

    def __str__(self):
        return self.label


class Exon(TimeStampedModel):
    """Exon in RefSeq Transcript.

    Source: hg18 http://hgdownload.soe.ucsc.edu/goldenPath/hg18/database/refGene.txt.gz
    Source: hg19 http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz
    Source: hg38 http://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/refGene.txt.gz
    """
    number = models.PositiveSmallIntegerField()
    active = models.BooleanField(default=True)
    transcript = models.ForeignKey(
        'genome.Transcript',
        on_delete=models.CASCADE,
        related_name='exons',
    )
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()
    cds = models.BooleanField(default=False)

    objects = managers.ExonQuerySet.as_manager()

    class Meta:
        verbose_name = _('Exon')
        verbose_name_plural = _('Exons')

    def __str__(self):
        return str(self.number)


class GeneList(TimeStampedModel):
    """Collection of genes to use a gene list for analysis, etc."""
    label = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True)
    version = models.CharField(max_length=25)
    active = models.BooleanField(default=True)
    genes = models.ManyToManyField(
        'genome.Gene',
        related_name='gene_lists',
        blank=True,
    )

    class Meta:
        verbose_name = _('Gene List')
        verbose_name_plural = _('Gene Lists')
        unique_together = ('label', 'version')

    def __str__(self):
        return self.label
