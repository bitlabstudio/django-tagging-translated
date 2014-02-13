# -*- coding: utf-8 -*-
"""Tests for the models of the ``tagging_translated`` app."""
from django.test import TestCase

from tagging.models import Tag

from .. import models
from . import factories


class TagTestCase(TestCase):
    """Tests for the ``Tag`` model class."""
    longMessage = True

    def test_instantiation_and_signal(self):
        """Test instantiation of the ``Tag`` model."""
        tag = factories.TagFactory()
        self.assertTrue(tag.pk)
        self.assertEqual(
            models.TagTranslated.objects.count(), 1, msg=(
                'There should be a translation created along with the tag.'))

        tag.save()
        self.assertEqual(
            models.TagTranslated.objects.count(), 1, msg=(
                'If we save the tag again, there should still be only one'
                ' translation.'))

        trans = models.TagTranslated.objects.get()
        trans.name = 'NewName'
        trans.save()
        tag = Tag.objects.get(pk=tag.pk)
        self.assertEqual(tag.name, trans.name, msg=(
            'The name of the tag should have been updated.'))
