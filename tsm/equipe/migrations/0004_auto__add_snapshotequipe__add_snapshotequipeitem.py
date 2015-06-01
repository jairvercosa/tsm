# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SnapshotEquipe'
        db.create_table(u'equipe_snapshotequipe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('equipe', ['SnapshotEquipe'])

        # Adding model 'SnapshotEquipeItem'
        db.create_table(u'equipe_snapshotequipeitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('snapshot', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snapshot_equipe_set', to=orm['equipe.SnapshotEquipe'])),
            ('criador', self.gf('django.db.models.fields.related.ForeignKey')(related_name='criador_snapshot_equipe_set', to=orm['auth.User'])),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(related_name='usuario_snapshot_equipe_set', on_delete=models.PROTECT, to=orm['acesso.Usuario'])),
            ('lider', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='master_snapshot_equipe_set', null=True, to=orm['equipe.SnapshotEquipeItem'])),
            ('criado', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('equipe', ['SnapshotEquipeItem'])

        # Adding M2M table for field carteiras on 'SnapshotEquipeItem'
        m2m_table_name = db.shorten_name(u'equipe_snapshotequipeitem_carteiras')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('snapshotequipeitem', models.ForeignKey(orm['equipe.snapshotequipeitem'], null=False)),
            ('carteira', models.ForeignKey(orm['cliente.carteira'], null=False))
        ))
        db.create_unique(m2m_table_name, ['snapshotequipeitem_id', 'carteira_id'])


    def backwards(self, orm):
        # Deleting model 'SnapshotEquipe'
        db.delete_table(u'equipe_snapshotequipe')

        # Deleting model 'SnapshotEquipeItem'
        db.delete_table(u'equipe_snapshotequipeitem')

        # Removing M2M table for field carteiras on 'SnapshotEquipeItem'
        db.delete_table(db.shorten_name(u'equipe_snapshotequipeitem_carteiras'))


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
        'equipe.membro': {
            'Meta': {'object_name': 'Membro'},
            'carteiras': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'carteiras_set'", 'blank': 'True', 'to': "orm['cliente.Carteira']"}),
            'criado': ('django.db.models.fields.DateField', [], {}),
            'criador': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'criador'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lider': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'master'", 'null': 'True', 'to': "orm['equipe.Membro']"}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'usuario'", 'on_delete': 'models.PROTECT', 'to': "orm['acesso.Usuario']"})
        },
        'equipe.membrohistorico': {
            'Meta': {'object_name': 'MembroHistorico'},
            'criado': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome_lider': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'nome_membro': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'nome_usuario_add': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'equipe.membrometa': {
            'Meta': {'unique_together': "(('membro', 'tipometa', 'receita', 'mesVigencia', 'anoVigencia'),)", 'object_name': 'MembroMeta'},
            'anoVigencia': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '4'}),
            'criado': ('django.db.models.fields.DateField', [], {}),
            'criador': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['acesso.Usuario']", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_Visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'membro': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipe.Membro']"}),
            'mesVigencia': ('django.db.models.fields.CharField', [], {'default': "'08'", 'max_length': '2'}),
            'receita': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['oportunidade.Receita']"}),
            'tipometa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipe.TipoMeta']"}),
            'valor': ('django.db.models.fields.FloatField', [], {})
        },
        'equipe.membrometahistorico': {
            'Meta': {'object_name': 'MembroMetaHistorico'},
            'criado': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome_lider': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'nome_membro': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'nome_tipometa': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'nome_usuario_add': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'valor': ('django.db.models.fields.FloatField', [], {})
        },
        'equipe.snapshotequipe': {
            'Meta': {'object_name': 'SnapshotEquipe'},
            'data': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'equipe.snapshotequipeitem': {
            'Meta': {'object_name': 'SnapshotEquipeItem'},
            'carteiras': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'carteiras_snapshot_equipe_set'", 'blank': 'True', 'to': "orm['cliente.Carteira']"}),
            'criado': ('django.db.models.fields.DateField', [], {}),
            'criador': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'criador_snapshot_equipe_set'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lider': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'master_snapshot_equipe_set'", 'null': 'True', 'to': "orm['equipe.SnapshotEquipeItem']"}),
            'snapshot': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snapshot_equipe_set'", 'to': "orm['equipe.SnapshotEquipe']"}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'usuario_snapshot_equipe_set'", 'on_delete': 'models.PROTECT', 'to': "orm['acesso.Usuario']"})
        },
        'equipe.tipometa': {
            'Meta': {'object_name': 'TipoMeta'},
            'filial': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['core.Filial']", 'on_delete': 'models.PROTECT'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'oportunidade.receita': {
            'Meta': {'object_name': 'Receita'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        }
    }

    complete_apps = ['equipe']