# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Cliente.cnpj'
        db.delete_column(u'cliente_cliente', 'cnpj')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Cliente.cnpj'
        raise RuntimeError("Cannot reverse this migration. 'Cliente.cnpj' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Cliente.cnpj'
        db.add_column(u'cliente_cliente', 'cnpj',
                      self.gf('django.db.models.fields.CharField')(max_length=18),
                      keep_default=False)


    models = {
        'cliente.carteira': {
            'Meta': {'object_name': 'Carteira'},
            'filial': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['core.Filial']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'cliente.cliente': {
            'Meta': {'object_name': 'Cliente'},
            'bairro': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'carteira': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cliente.Carteira']"}),
            'cep': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'cidade': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'cnpj_matriz': ('django.db.models.fields.CharField', [], {'max_length': '18', 'null': 'True', 'blank': 'True'}),
            'criado': ('django.db.models.fields.DateField', [], {'max_length': '60'}),
            'endereco': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'filial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Filial']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'produtos': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'produto_set'", 'blank': 'True', 'to': "orm['cliente.Produto']"}),
            'segmento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cliente.Segmento']", 'null': 'True', 'blank': 'True'}),
            'webpage': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'})
        },
        'cliente.contato': {
            'Meta': {'object_name': 'Contato'},
            'cargo': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'celular': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cliente.Cliente']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'telefone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'cliente.fabricante': {
            'Meta': {'object_name': 'Fabricante'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'cliente.produto': {
            'Meta': {'object_name': 'Produto'},
            'fabricante': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cliente.Fabricante']", 'null': 'True'}),
            'filial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Filial']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'segmento': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'cliente.segmento': {
            'Meta': {'object_name': 'Segmento'},
            'cnae': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'subsegmento': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'})
        },
        'core.filial': {
            'Meta': {'object_name': 'Filial'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matriz': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cliente']