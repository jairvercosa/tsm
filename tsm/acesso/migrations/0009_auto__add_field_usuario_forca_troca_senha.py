# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Usuario.forca_troca_senha'
        db.add_column(u'acesso_usuario', 'forca_troca_senha',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Usuario.forca_troca_senha'
        db.delete_column(u'acesso_usuario', 'forca_troca_senha')


    models = {
        'acesso.funcao': {
            'Meta': {'object_name': 'Funcao'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'acesso.usuario': {
            'Meta': {'object_name': 'Usuario', '_ormbases': [u'auth.User']},
            'assistentes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'assistentes_rel_+'", 'null': 'True', 'to': "orm['acesso.Usuario']"}),
            'filiais': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'filial_set'", 'blank': 'True', 'to': "orm['core.Filial']"}),
            'forca_troca_senha': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'funcao': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['acesso.Funcao']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'receitas': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'usuario_receitas_set'", 'to': "orm['oportunidade.Receita']", 'through': "orm['acesso.UsuarioReceitas']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'segmentos': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'usuario_segmentos_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['cliente.Segmento']"}),
            'showToTeam': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'telefone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'acesso.usuarioreceitas': {
            'Meta': {'object_name': 'UsuarioReceitas'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receita': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oportunidade.Receita']", 'null': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['acesso.Usuario']", 'null': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cliente.segmento': {
            'Meta': {'object_name': 'Segmento'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.filial': {
            'Meta': {'object_name': 'Filial'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matriz': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'responsavel': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'diretor'", 'on_delete': 'models.PROTECT', 'to': "orm['acesso.Usuario']"})
        },
        'oportunidade.receita': {
            'Meta': {'object_name': 'Receita'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        }
    }

    complete_apps = ['acesso']