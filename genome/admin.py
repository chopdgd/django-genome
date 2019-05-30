# -*- coding: utf-8
from django.contrib import admin

from . import models


class GenomeAdmin(admin.ModelAdmin):
    model = models.Genome
    list_display = ('label', 'active', 'created', 'modified')
    prepopulated_fields = {
        'slug': ('label', )
    }
    search_fields = ('label', 'description')
    list_filter = ('active', )
    save_as = True


class ChromosomeAdmin(admin.ModelAdmin):
    model = models.Chromosome
    list_display = (
        'label', 'genome', 'length',
        'active', 'created', 'modified',
    )
    raw_id_fields = ('genome', )
    search_fields = ('label', )
    list_filter = ('active', )
    save_as = True


class CytoBandAdmin(admin.ModelAdmin):
    model = models.CytoBand
    list_display = (
        'label', 'chromosome', 'start', 'end',
        'active', 'created', 'modified',
    )
    raw_id_fields = ('chromosome', )
    search_fields = ('label', 'stain')
    list_filter = ('active', )
    save_as = True


class GeneAdmin(admin.ModelAdmin):
    model = models.Gene
    list_display = (
        'symbol', 'hgnc_id', 'status', 'chromosome',
        'active', 'created', 'modified',
    )
    raw_id_fields = ('chromosome', 'synonyms')
    search_fields = ('symbol', 'name', 'previous_name', 'synonyms__label')
    list_filter = ('active', 'status')
    save_as = True


class GeneSynonymAdmin(admin.ModelAdmin):
    model = models.GeneSynonym
    list_display = ('label', 'active', 'created', 'modified')
    search_fields = ('label', 'genes__symbol')
    list_filter = ('active', )
    save_as = True


class TranscriptAdmin(admin.ModelAdmin):
    model = models.Transcript
    list_display = (
        'label', 'gene', 'strand',
        'transcription_start', 'transcription_end',
        'cds_start', 'cds_end',
        'active', 'created', 'modified',
    )
    raw_id_fields = ('gene', )
    search_fields = ('label', 'gene__symbol', 'gene__synonyms__label')
    list_filter = ('active', 'strand')
    save_as = True


class ExonAdmin(admin.ModelAdmin):
    model = models.Exon
    list_display = (
        'number', 'transcript', 'start', 'end', 'cds',
        'active', 'created', 'modified',
    )
    raw_id_fields = ('transcript', )
    search_fields = (
        'transcript__label',
        'transcript__gene__symbol',
        'transcript__gene__synonyms__label',
    )
    list_filter = ('active', )
    save_as = True


admin.site.register(models.Genome, GenomeAdmin)
admin.site.register(models.Chromosome, ChromosomeAdmin)
admin.site.register(models.CytoBand, CytoBandAdmin)
admin.site.register(models.Gene, GeneAdmin)
admin.site.register(models.GeneSynonym, GeneSynonymAdmin)
admin.site.register(models.Transcript, TranscriptAdmin)
admin.site.register(models.Exon, ExonAdmin)
