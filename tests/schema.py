from graphene import Field, Node, ObjectType, Schema
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField

from genome import models, schema as genome_schema


# NOTE: We need to subclass Filter in combination with register above
from django.db.models import CharField

import django_filters
from genomix.filters import DisplayChoiceFilter


class GeneFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = models.Gene
        fields = '__all__'


class Query(ObjectType):

    gene = Node.Field(genome_schema.GeneNode)
    all_genes = DjangoFilterConnectionField(
        genome_schema.GeneNode,
        filterset_class=GeneFilter,
    )

    debug = Field(DjangoDebug, name='__debug')


schema = Schema(query=Query)
