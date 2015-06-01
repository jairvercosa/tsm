# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Situacao'
        db.create_table(u'oportunidade_situacao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal('oportunidade', ['Situacao'])

        # Adding model 'TipoTemperatura'
        db.create_table(u'oportunidade_tipotemperatura', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('perc', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
        ))
        db.send_create_signal('oportunidade', ['TipoTemperatura'])

        # Adding model 'Receita'
        db.create_table(u'oportunidade_receita', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal('oportunidade', ['Receita'])

        # Adding model 'Questao'
        db.create_table(u'oportunidade_questao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ordem', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=10)),
            ('pergunta', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('sim', self.gf('django.db.models.fields.FloatField')()),
            ('nao', self.gf('django.db.models.fields.FloatField')()),
            ('filial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Filial'])),
        ))
        db.send_create_signal('oportunidade', ['Questao'])

        # Adding model 'Oportunidade'
        db.create_table(u'oportunidade_oportunidade', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Filial'], blank=True)),
            ('cliente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cliente.Cliente'], blank=True)),
            ('receita', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oportunidade.Receita'], blank=True)),
            ('situacao', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oportunidade.Situacao'])),
            ('valor', self.gf('django.db.models.fields.FloatField')()),
            ('ponderado', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('temperatura_auto', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('tipotemperatura', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oportunidade.TipoTemperatura'])),
            ('responsavel', self.gf('django.db.models.fields.related.ForeignKey')(related_name='responsavel_set', blank=True, to=orm['acesso.Usuario'])),
            ('lider', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lider_oportunidade_set', blank=True, to=orm['acesso.Usuario'])),
            ('criador', self.gf('django.db.models.fields.related.ForeignKey')(related_name='criado_oportunidade_set', blank=True, to=orm['acesso.Usuario'])),
            ('criado', self.gf('django.db.models.fields.DateField')()),
            ('dtFechamento', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('oportunidade', ['Oportunidade'])

        # Adding model 'Historico'
        db.create_table(u'oportunidade_historico', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('oportunidade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oportunidade.Oportunidade'])),
            ('criado', self.gf('django.db.models.fields.DateField')()),
            ('nome_usuario_add', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('nome_situacao', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('nome_tipotemperatura', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('nome_responsavel', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('nome_lider', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('valor', self.gf('django.db.models.fields.FloatField')()),
            ('ponderado', self.gf('django.db.models.fields.FloatField')()),
            ('temperatura_auto', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('dtFechamento', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('oportunidade', ['Historico'])

        # Adding model 'Resposta'
        db.create_table(u'oportunidade_resposta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('questao', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oportunidade.Questao'])),
            ('oportunidade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oportunidade.Oportunidade'])),
            ('resposta', self.gf('django.db.models.fields.BooleanField')()),
            ('criado', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('oportunidade', ['Resposta'])

        # Adding model 'HistoricoResposta'
        db.create_table(u'oportunidade_historicoresposta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('oportunidade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oportunidade.Oportunidade'])),
            ('nome_usuario_add', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('questao_txt', self.gf('django.db.models.fields.CharField')(max_length=180)),
            ('resposta_txt', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('criado', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('oportunidade', ['HistoricoResposta'])


    def backwards(self, orm):
        # Deleting model 'Situacao'
        db.delete_table(u'oportunidade_situacao')

        # Deleting model 'TipoTemperatura'
        db.delete_table(u'oportunidade_tipotemperatura')

        # Deleting model 'Receita'
        db.delete_table(u'oportunidade_receita')

        # Deleting model 'Questao'
        db.delete_table(u'oportunidade_questao')

        # Deleting model 'Oportunidade'
        db.delete_table(u'oportunidade_oportunidade')

        # Deleting model 'Historico'
        db.delete_table(u'oportunidade_historico')

        # Deleting model 'Resposta'
        db.delete_table(u'oportunidade_resposta')

        # Deleting model 'HistoricoResposta'
        db.delete_table(u'oportunidade_historicoresposta')


    models = {
        'acesso.funcao': {
            'Meta': {'object_name': 'Funcao'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'acesso.usuario': {
            'Meta': {'object_name': 'Usuario', '_ormbases': [u'auth.User']},
            'filiais': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'filial_set'", 'blank': 'True', 'to': "orm['core.Filial']"}),
            'funcao': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['acesso.Funcao']", 'null': 'True', 'blank': 'True'}),
            'multEquipe': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'oportunidade.historico': {
            'Meta': {'object_name': 'Historico'},
            'criado': ('django.db.models.fields.DateField', [], {}),
            'dtFechamento': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome_lider': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'nome_responsavel': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'nome_situacao': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'nome_tipotemperatura': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'nome_usuario_add': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'oportunidade': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oportunidade.Oportunidade']"}),
            'ponderado': ('django.db.models.fields.FloatField', [], {}),
            'temperatura_auto': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'valor': ('django.db.models.fields.FloatField', [], {})
        },
        'oportunidade.historicoresposta': {
            'Meta': {'object_name': 'HistoricoResposta'},
            'criado': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome_usuario_add': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'oportunidade': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oportunidade.Oportunidade']"}),
            'questao_txt': ('django.db.models.fields.CharField', [], {'max_length': '180'}),
            'resposta_txt': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'oportunidade.oportunidade': {
            'Meta': {'object_name': 'Oportunidade'},
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cliente.Cliente']", 'blank': 'True'}),
            'criado': ('django.db.models.fields.DateField', [], {}),
            'criador': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'criado_oportunidade_set'", 'blank': 'True', 'to': "orm['acesso.Usuario']"}),
            'dtFechamento': ('django.db.models.fields.DateField', [], {}),
            'filial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Filial']", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lider_oportunidade_set'", 'blank': 'True', 'to': "orm['acesso.Usuario']"}),
            'ponderado': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'receita': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oportunidade.Receita']", 'blank': 'True'}),
            'responsavel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responsavel_set'", 'blank': 'True', 'to': "orm['acesso.Usuario']"}),
            'situacao': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oportunidade.Situacao']"}),
            'temperatura_auto': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'tipotemperatura': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oportunidade.TipoTemperatura']"}),
            'valor': ('django.db.models.fields.FloatField', [], {})
        },
        'oportunidade.questao': {
            'Meta': {'object_name': 'Questao'},
            'filial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Filial']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nao': ('django.db.models.fields.FloatField', [], {}),
            'ordem': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '10'}),
            'pergunta': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'sim': ('django.db.models.fields.FloatField', [], {})
        },
        'oportunidade.receita': {
            'Meta': {'object_name': 'Receita'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'oportunidade.resposta': {
            'Meta': {'object_name': 'Resposta'},
            'criado': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oportunidade': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oportunidade.Oportunidade']"}),
            'questao': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oportunidade.Questao']"}),
            'resposta': ('django.db.models.fields.BooleanField', [], {})
        },
        'oportunidade.situacao': {
            'Meta': {'object_name': 'Situacao'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'oportunidade.tipotemperatura': {
            'Meta': {'object_name': 'TipoTemperatura'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'perc': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['oportunidade']