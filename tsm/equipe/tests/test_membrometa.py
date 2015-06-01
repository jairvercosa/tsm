# -*- coding: ISO-8859-1 -*-
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from model_mommy import mommy

from tsm.core.base.core_base_test import Testsbase
from tsm.equipe.models.membrometa import MembroMeta


class TestsMembro(Testsbase):
    modelStandard = MembroMeta
    modelMommy = 'equipe.MembroMeta'
    urlBase = '/equipe/membro/metas/'
    fieldTestRender = 'valor'
    dataInsert = {
        'criador' : None,
        'criado' :'2010-05-01',
        'tipometa' : None,
        'membro' : None,
        'valor': 2500000,
        'mesVigencia'  : '01',
        'anoVigencia'  : 2014,
        'isVisible'   : True,
    }

    def setUp(self):
        contentItem = ContentType.objects.get(app_label='equipe',model='membrometa')
        #busca permissoes do model
        if contentItem:
            permissao = Permission.objects.create(content_type=contentItem, name='add_self_membrometa', codename='add_self_membrometa')
            permissao.save()

        return super(TestsMembro,self).setUp()

    def test_permissions(self):
        """
        Testa se valida permissoes de acesso
        """
        if not self.urlBase is None:
            #Teste de insert
            response = self.client.get(self.urlBase+'formulario/')
            self.assertEquals(response.status_code, 403)

            #Cria dados
            self.prepare_to_post('test_permissions')

            #Teste de delete
            response = self.client.post(self.urlBase+'remove/'+str(self.modelRow.id)+'/',{})
            self.assertEquals(response.status_code, 403)

    def test_render_listpage(self):
        pass

    def test_return_data_to_list(self):
        """
        Testa do retorno de json dos niveis com os membros
        """
        # Faz chamada da pagina
        membro = mommy.make('equipe.Membro', usuario=self.user)

        response = self.client.get('/equipe/membro/metas/'+str(membro.id)+'/')
        self.assertEquals(response.status_code, 200)

    def prepare_to_post(self, fromDef):
        """
        Prepara dados para testar post
        """
        filial = mommy.make('core.Filial',responsavel=self.user)
        tipometa = mommy.make('equipe.TipoMeta',filial=filial)
        membro = mommy.make('equipe.Membro', usuario=self.user)

        self.dataInsert['membro'] = membro.id
        self.dataInsert['tipometa'] = tipometa.id
        self.dataInsert['criador'] = self.user.id
        if fromDef == 'test_insert':
            self.modelPost = self.dataInsert
        else:
            self.modelRow = mommy.make(self.modelMommy, membro=membro, tipometa=tipometa, criador=self.user)
            self.modelPost = self.dataInsert

    def test_insert_self(self):
        """
        Testa se pode inserir meta para si
        """
        contentItem = ContentType.objects.get(app_label='equipe',model='membrometa')
        #busca permissoes do model
        if not contentItem:
            self.assertTrue(False)

        #permissao de inclusao de meta, mas nao tem a permissao de incluir meta para ele mesmo
        permission = Permission.objects.get(content_type=contentItem.id, codename='add_membrometa')
        if permission:
            self.user.user_permissions.add(permission)
        else:
            self.assertTrue(False)

        # Faz chamada da pagina
        if not self.urlBase is None:
            self.prepare_to_post('test_insert')
            response = self.client.post(self.urlBase+'formulario/', self.modelPost)
            self.assertEquals(response.status_code, 400)

    def test_insert(self):
        """
        Testa gravação dos dados no post de inclusão
        """
        self.addPermissions()
        # Faz chamada da pagina
        if not self.urlBase is None:
            self.prepare_to_post('test_insert')
            response = self.client.post(self.urlBase+'formulario/', self.modelPost)
            self.assertEquals(response.status_code, 200)

            #testa se permite inclusao duplicada
            response = self.client.post(self.urlBase+'formulario/', self.modelPost)
            self.assertEquals(response.status_code, 400)

    def test_update(self):
        self.addPermissions()
        self.prepare_to_post('test_update')
        response = self.client.post(self.urlBase+'visivel/'+str(self.modelRow.id)+'/', {'isVisible': True})
        self.assertEquals(response.status_code, 200)