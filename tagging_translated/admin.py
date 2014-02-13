"""Admin classes for the ``tagging_translated`` app."""
from urllib import urlencode
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.template import TemplateDoesNotExist
from django.template.loader import find_template
from django.utils.encoding import iri_to_uri
from django.utils.translation import get_language

from hvad.admin import TranslatableAdmin, TranslatableTabularInline
from tagging.admin import TagAdmin
from tagging.models import Tag

from .models import TagTranslated


def get_language_name(language_code):
    return dict(settings.LANGUAGES).get(language_code, language_code)


class TagTranslatedAdmin(TranslatableAdmin):
    """Admin for the `TagTranslated` model."""
    pass


class TagTranslatedInline(TranslatableTabularInline):
    model = TagTranslated


class TagAdmin(TagAdmin):
    exclude = ['name', ]
    inlines = TagAdmin.inlines + [TagTranslatedInline]
    query_language_key = 'language'

    def get_available_languages(self, obj):
        if obj:
            return obj.translated.get_available_languages()
        else:
            return []

    def get_language_tabs(self, request, available_languages):
        tabs = []
        get = dict(request.GET)
        language = self._language(request)
        for key, name in settings.LANGUAGES:
            get.update({'language': key})
            url = '%s://%s%s?%s' % (request.is_secure() and 'https' or 'http',
                                    request.get_host(), request.path,
                                    urlencode(get))
            if language == key:
                status = 'current'
            elif key in available_languages:
                status = 'available'
            else:
                status = 'empty'
            tabs.append((url, name, key, status))
        return tabs

    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        lang_code = self._language(request)
        lang = get_language_name(lang_code)
        available_languages = self.get_available_languages(obj)
        context['title'] = '%s (%s)' % (context['title'], lang)
        context['current_is_translated'] = lang_code in available_languages
        context['allow_deletion'] = len(available_languages) > 1
        context['language_tabs'] = self.get_language_tabs(
            request, available_languages)
        context['base_template'] = self.get_change_form_base_template()
        return super(TagAdmin, self).render_change_form(request, context,
                                                        add, change, form_url,
                                                        obj)

    def get_change_form_base_template(self):
        opts = self.model._meta
        app_label = opts.app_label
        search_templates = [
            "admin/%s/%s/change_form.html" % (app_label,
                                              opts.object_name.lower()),
            "admin/%s/change_form.html" % app_label,
            "admin/change_form.html"
        ]
        for template in search_templates:
            try:
                find_template(template)
                return template
            except TemplateDoesNotExist:
                pass
        else:  # pragma: no cover
            pass

    def response_change(self, request, obj):
        redirect = super(TagAdmin, self).response_change(request, obj)
        uri = iri_to_uri(request.path)
        app_label, model_name = self.model._meta.app_label, \
            self.model._meta.module_name
        if redirect['Location'] in (uri, "../add/", reverse(
                'admin:%s_%s_add' % (app_label, model_name))):
            if self.query_language_key in request.GET:
                redirect['Location'] = '%s?%s=%s' % (
                    redirect['Location'],
                    self.query_language_key, request.GET[
                        self.query_language_key])
        return redirect

    def _language(self, request):
        return request.GET.get(self.query_language_key, get_language())


admin.site.unregister(Tag)
admin.site.register(Tag, TagAdmin)
admin.site.register(TagTranslated, TagTranslatedAdmin)
