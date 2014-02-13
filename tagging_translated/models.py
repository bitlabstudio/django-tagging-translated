"""Models for the ``tagging_translated`` app."""
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from hvad.models import TranslatedFields, TranslatableModel
from tagging.models import Tag


class TagTranslated(TranslatableModel):
    """Translatable model attached to a Tag."""
    translations = TranslatedFields(
        name=models.CharField(
            verbose_name=_('Name'),
            max_length=256,
        )
    )

    tag = models.OneToOneField(
        Tag,
        verbose_name=_('Tag'),
        related_name='translated',
    )

    def __unicode__(self):
        return self.safe_translation_getter('name', self.tag.name)


@receiver(post_save, sender=Tag)
def tag_post_save_handler(sender, **kwargs):
    """
    Makes sure that a translation is created when a tag is saved.


    """
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    # if we save the admin form, that excludes the name field, we won't have
    # instance.name and therefore know, that we are saving from the admin.
    # In that case, we don't create a translation, because it should be done by
    # the admin form.
    try:
        instance.translated
    except TagTranslated.DoesNotExist:
        if instance.name and created:
            TagTranslated.objects.create(
                name=instance.name, tag=instance, language_code='en')


@receiver(post_save, sender=TagTranslated)
def tagtranslated_post_save_handler(sender, **kwargs):
    """
    Ensure that the original tag name gets updated when the english
    translation is updated.

    """
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if instance.name != instance.tag.name and not created and \
            instance.language_code == 'en':
        instance.tag.name = instance.name
        instance.tag.save_base(raw=True)
