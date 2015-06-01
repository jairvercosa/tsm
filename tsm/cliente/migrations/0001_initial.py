# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Carteira'
        db.create_table(u'cliente_carteira', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('filial', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Filial'])),
        ))
        db.send_create_signal('cliente', ['Carteira'])

        # Adding model 'Fabricante'
        db.create_table(u'cliente_fabricante', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('cliente', ['Fabricante'])

        # Adding model 'Produto'
        db.create_table(u'cliente_produto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('segmento', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('fabricante', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cliente.Fabricante'], null=True)),
            ('filial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Filial'], null=True, blank=True)),
        ))
        db.send_create_signal('cliente', ['Produto'])

        # Adding model 'Cliente'
        db.create_table(u'cliente_cliente', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('cnpj', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('cnpj_matriz', self.gf('django.db.models.fields.CharField')(max_length=18, null=True, blank=True)),
            ('endereco', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('bairro', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('cidade', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('estado', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('cep', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('webpage', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('criado', self.gf('django.db.models.fields.DateField')(max_length=60)),
            ('filial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Filial'])),
            ('carteira', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cliente.Carteira'])),
        ))
        db.send_create_signal('cliente', ['Cliente'])

        # Adding M2M table for field produtos on 'Cliente'
        m2m_table_name = db.shorten_name(u'cliente_cliente_produtos')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cliente', models.ForeignKey(orm['cliente.cliente'], null=False)),
            ('produto', models.ForeignKey(orm['cliente.produto'], null=False))
        ))
        db.create_unique(m2m_table_name, ['cliente_id', 'produto_id'])

        # Adding model 'Contato'
        db.create_table(u'cliente_contato', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('cargo', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('telefone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('celular', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100, null=True, blank=True)),
            ('cliente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cliente.Cliente'])),
        ))
        db.send_create_signal('cliente', ['Contato'])


    def backwards(self, orm):
        # Deleting model 'Carteira'
        db.delete_table(u'cliente_carteira')

        # Deleting model 'Fabricante'
        db.delete_table(u'cliente_fabricante')

        # Deleting model 'Produto'
        db.delete_table(u'cliente_produto')

        # Deleting model 'Cliente'
        db.delete_table(u'cliente_cliente')

        # Removing M2M table for field produtos on 'Cliente'
        db.delete_table(db.shorten_name(u'cliente_cliente_produtos'))

        # Deleting model 'Contato'
        db.delete_table(u'cliente_contato')


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
            'cnpj': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'cnpj_matriz': ('django.db.models.fields.CharField', [], {'max_length': '18', 'null': 'True', 'blank': 'True'}),
            'criado': ('django.db.models.fields.DateField', [], {'max_length': '60'}),
            'endereco': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'filial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Filial']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'produtos': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'produto_set'", 'blank': 'True', 'to': "orm['cliente.Produto']"}),
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
        'core.filial': {
            'Meta': {'object_name': 'Filial'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matriz': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cliente']