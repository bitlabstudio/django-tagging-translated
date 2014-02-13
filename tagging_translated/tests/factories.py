"""Factories for the `tagging_translated` app."""
import factory
from django_libs.tests.factories import HvadFactoryMixin
from tagging.models import Tag

from .. import models


class TagFactory(factory.DjangoModelFactory):
    """Factory for the ``Tag`` model."""
    FACTORY_FOR = Tag

    name = factory.Sequence(lambda n: 'name {0}'.format(n))


class TagTranslatedFactory(HvadFactoryMixin, factory.DjangoModelFactory):
    """Factory for the ``TagTranslated`` model."""
    FACTORY_FOR = models.TagTranslated

    tag = factory.SubFactory(TagFactory)
    name = factory.Sequence(lambda n: 'name {0}'.format(n))
