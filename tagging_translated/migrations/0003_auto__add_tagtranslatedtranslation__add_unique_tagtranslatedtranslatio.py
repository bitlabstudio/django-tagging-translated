# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TagTranslatedTranslation'
        db.create_table('tagging_translated_tagtranslated_translation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['tagging_translated.TagTranslated'])),
        ))
        db.send_create_signal('tagging_translated', ['TagTranslatedTranslation'])

        # Adding unique constraint on 'TagTranslatedTranslation', fields ['language_code', 'master']
        db.create_unique('tagging_translated_tagtranslated_translation', ['language_code', 'master_id'])

        # Adding model 'TagTranslated'
        db.create_table('tagging_translated_tagtranslated', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.OneToOneField')(related_name='translated', unique=True, to=orm['tagging.Tag'])),
        ))
        db.send_create_signal('tagging_translated', ['TagTranslated'])


    def backwards(self, orm):
        # Removing unique constraint on 'TagTranslatedTranslation', fields ['language_code', 'master']
        db.delete_unique('tagging_translated_tagtranslated_translation', ['language_code', 'master_id'])

        # Deleting model 'TagTranslatedTranslation'
        db.delete_table('tagging_translated_tagtranslated_translation')

        # Deleting model 'TagTranslated'
        db.delete_table('tagging_translated_tagtranslated')


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