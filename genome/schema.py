from graphene import List, Node, String
from graphene_django import DjangoObjectType

from . import choices, models


class GenomeNode(DjangoObjectType):

    class Meta:
        model = models.Genome
        interfaces = (Node, )


class ChromosomeNode(DjangoObjectType):

    class Meta:
        model = models.Chromosome
        interfaces = (Node, )


class CytoBandNode(DjangoObjectType):

    class Meta:
        model = models.CytoBand
        interfaces = (Node, )


class GeneNode(DjangoObjectType):

    status = String()
    ensembl_urls = List(String)
    refseq_urls = List(String)
    omim_urls = List(String)
    uniprot_urls = List(String)
    mgi_urls = List(String)
    rgd_urls = List(String)

    class Meta:
        model = models.Gene
        interfaces = (Node, )

    def resolve_status(self, info):
        return choices.HGNC_GENE_STATUS[self.status]

    def resolve_ensembl_urls(self, info):
        return self.ensembl_urls

    def resolve_refseq_urls(self, info):
        return self.refseq_urls

    def resolve_omim_urls(self, info):
        return self.omim_urls

    def resolve_uniprot_urls(self, info):
        return self.uniprot_urls

    def resolve_mgi_urls(self, info):
        return self.mgi_urls

    def resolve_rgd_urls(self, info):
        return self.rgd_urls


class GeneSynonymNode(DjangoObjectType):

    class Meta:
        model = models.GeneSynonym
        interfaces = (Node, )


class TranscriptNode(DjangoObjectType):

    strand = String()

    class Meta:
        model = models.Transcript
        interfaces = (Node, )

    def resolve_strand(self, info):
        return choices.STRAND_TYPES[self.strand]


class ExonNode(DjangoObjectType):

    class Meta:
        model = models.Exon
        interfaces = (Node, )
