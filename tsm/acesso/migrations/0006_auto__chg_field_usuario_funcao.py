# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field receitas on 'Usuario'
        m2m_table_name = db.shorten_name(u'acesso_usuario_receitas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('usuario', models.ForeignKey(orm['acesso.usuario'], null=False)),
            ('receita', models.ForeignKey(orm['oportunidade.receita'], null=False))
        ))
        db.create_unique(m2m_table_name, ['usuario_id', 'receita_id'])


        # Changing field 'Usuario.funcao'
        db.alter_column(u'acesso_usuario', 'funcao_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['acesso.Funcao'], null=True, on_delete=models.PROTECT))

    def backwards(self, orm):
        # Removing M2M table for field receitas on 'Usuario'
        db.delete_table(db.shorten_name(u'acesso_usuario_receitas'))


        # Changing field 'Usuario.funcao'
        db.alter_column(u'acesso_usuario', 'funcao_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['acesso.Funcao'], null=True))

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
            'funcao': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['acesso.Funcao']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'receitas': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'usuario_receitas_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['oportunidade.Receita']"}),
            'showToTeam': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'telefone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
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