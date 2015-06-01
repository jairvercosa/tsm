# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Oportunidade.origem'
        db.delete_column(u'oportunidade_oportunidade', 'origem_id')


    def backwards(self, orm):
        # Adding field 'Oportunidade.origem'
        db.add_column(u'oportunidade_oportunidade', 'origem',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='origem_oportunidade_set', to=orm['oportunidade.Origem']),
                      keep_default=False)


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
        'cliente.carteira': {
            'Meta': {'object_name': 'Carteira'},
            'filial': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['core.Filial']", 'on_delete': 'models.PROTECT'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'cliente.cliente': {
            'Meta': {'object_name': 'Cliente'},
            'bairro': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'carteira': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cliente.Carteira']", 'on_delete': 'models.PROTECT'}),
            'cep': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'cidade': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'cnpj': ('django.db.models.fields.CharField', [], {'max_length': '18', 'null': 'True'}),
            'cnpj_matriz': ('django.db.models.fields.CharField', [], {'max_length': '18', 'null': 'True', 'blank': 'True'}),
            'criado': ('django.db.models.fields.DateField', [], {'max_length': '60'}),
            'endereco': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'executivo': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['acesso.Usuario']", 'on_delete': 'models.PROTECT'}),
            'filial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Filial']", 'on_delete': 'models.PROTECT'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'produtos': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'produto_set'", 'blank': 'True', 'to': "orm['cliente.Produto']"}),
            'segmento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cliente.Segmento']", 'null': 'True', 'on_delete': 'models.PROTECT'}),
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
            'filial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Filial']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '80'})
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
        'oportunidade.historico': {
            'Meta': {'object_name': 'Historico'},
            'criado': ('django.db.models.fields.DateField', [], {}),
            'dtFechado': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dtFechamento': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome_arquitetos': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'nome_gpp': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'nome_lider': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'nome_produto': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'nome_responsavel': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'nome_situacao': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'nome_tipotemperatura': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'nome_usuario_add': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'obs': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'arquitetos': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'arquitetos_set'", 'blank': 'True', 'to': "orm['acesso.Usuario']"}),
            'bc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cliente.Cliente']", 'on_delete': 'models.PROTECT'}),
            'codcrm': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'criado': ('django.db.models.fields.DateField', [], {}),
            'criador': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'criado_oportunidade_set'", 'blank': 'True', 'on_delete': 'models.PROTECT', 'to': "orm['acesso.Usuario']"}),
            'dtFechado': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dtFechamento': ('django.db.models.fields.DateField', [], {}),
            'filial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Filial']", 'on_delete': 'models.PROTECT'}),
            'gpp': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'gpp_set'", 'null': 'True', 'on_delete': 'models.PROTECT', 'to': "orm['acesso.Usuario']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lider_oportunidade_set'", 'on_delete': 'models.PROTECT', 'to': "orm['acesso.Usuario']"}),
            'mw': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'obs': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ponderado': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'produto': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'produto_oportunidade_set'", 'null': 'True', 'on_delete': 'models.PROTECT', 'to': "orm['cliente.Produto']"}),
            'receita': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oportunidade.Receita']", 'on_delete': 'models.PROTECT'}),
            'responsavel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responsavel_set'", 'on_delete': 'models.PROTECT', 'to': "orm['acesso.Usuario']"}),
            'rtc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'situacao': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oportunidade.Situacao']", 'on_delete': 'models.PROTECT'}),
            'temperatura_auto': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'tipotemperatura': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tipotemperatura_set'", 'on_delete': 'models.PROTECT', 'to': "orm['oportunidade.TipoTemperatura']"}),
            'valor': ('django.db.models.fields.FloatField', [], {})
        },
        'oportunidade.origem': {
            'Meta': {'object_name': 'Origem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '60'})
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
            'questao': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oportunidade.Questao']", 'on_delete': 'models.PROTECT'}),
            'resposta': ('django.db.models.fields.BooleanField', [], {})
        },
        'oportunidade.rtc': {
            'Meta': {'object_name': 'Rtc'},
            'criado': ('django.db.models.fields.DateField', [], {}),
            'data': ('django.db.models.fields.DateField', [], {}),
            'descricao': ('django.db.models.fields.TextField', [], {}),
            'hora': ('django.db.models.fields.TimeField', [], {'default': "'00:00'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oportunidade': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'oportunidade_rtc_set'", 'to': "orm['oportunidade.Oportunidade']"}),
            'recursos': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'recursos_set'", 'blank': 'True', 'to': "orm['acesso.Usuario']"})
        },
        'oportunidade.situacao': {
            'Meta': {'object_name': 'Situacao'},
            'fator': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'operador': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '1'}),
            'perc': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        'oportunidade.tipotemperatura': {
            'Meta': {'object_name': 'TipoTemperatura'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'perc': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['oportunidade']