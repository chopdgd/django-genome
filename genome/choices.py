# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices


HGNC_GENE_STATUS = Choices(
    (1, 'approved', _('approved')),
    (2, 'entry_withdrawn', _('entry_withdrawn')),
    (3, 'symbol_withdrawn', _('symbol_withdrawn')),
    (4, 'ucsc_gene', _('ucsc_gene')),
)

STRAND_TYPES = Choices(
    (1, '+', _('+')),
    (2, '-', _('-')),
)
