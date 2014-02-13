# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        for tag in orm['tagging.Tag'].objects.all():
            master = orm['tagging_translated.TagTranslated'].objects.create(
                tag=tag)
            for title in orm['tagging_translated.TagTitle'].objects.filter(
                    tag=tag):
                orm['tagging_translated.TagTranslatedTranslation'].objects.create(
                    master=master, language_code=title.language,
                    name=title.trans_name,
                )

    def backwards(self, orm):
        pass

    models = {
        'tagging.tag': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'tagging_translated.tagtitle': {
            'Meta': {'object_name': 'TagTitle'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tagging.Tag']"}),
            'trans_name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'tagging_translated.tagtranslated': {
            'Meta': {'object_name': 'TagTranslated'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'translated'", 'unique': 'True', 'to': "orm['tagging.Tag']"})
        },
        'tagging_translated.tagtranslatedtranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'TagTranslatedTranslation', 'db_table': "'tagging_translated_tagtranslated_translation'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['tagging_translated.TagTranslated']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['tagging_translated']
    symmetrical = True
