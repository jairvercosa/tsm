# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Filial'
        db.create_table(u'core_filial', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('matriz', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Filial'])

        # Adding model 'Parametro'
        db.create_table(u'core_parametro', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('valor', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('filial', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Filial'], null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Parametro'])


    def backwards(self, orm):
        # Deleting model 'Filial'
        db.delete_table(u'core_filial')

        # Deleting model 'Parametro'
        db.delete_table(u'core_parametro')


    models = {
        'core.filial': {
            'Meta': {'object_name': 'Filial'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matriz': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.parametro': {
            'Meta': {'object_name': 'Parametro'},
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'filial': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['core.Filial']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'valor': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['core']