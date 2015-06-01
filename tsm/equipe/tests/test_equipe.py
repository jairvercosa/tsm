# -*- coding: ISO-8859-1 -*-
import json

from model_mommy import mommy

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from tsm.core.base.core_base_test import Testsbase
from tsm.core.models.filial import Filial

from tsm.equipe.models.membro import Membro
from tsm.equipe.models.membrohistorico import MembroHistorico

from tsm.cliente.models.carteira import Carteira

from tsm.acesso.models.usuario import Usuario

class TestsEquipe(Testsbase):
    funcao = None
    modelStandard = Membro
    modelMommy = 'equipe.Membro'
    urlBase = '/equipe/'
    fieldTestRender = 'usuario'
    dataInsert = {
        'usuario_id' : None,
        'lider_id' : '',
        'criado' :'2010-05-01',
    }

    def setUp(self):
        self.data = {
            'username' : 'testuser',
            'senha'       : 'testpass',
            'email'       : 'test@test.com'
        }
        self.funcao = mommy.make('acesso.Funcao')
        self.user = Usuario.objects.create_user(self.data['username'], self.data['email'], self.data['senha'])
        self.user.funcao = self.funcao
        self.user.save()
        self.client.login(username=self.data['username'], password=self.data['senha'])

    def test_permissions(self):
        """
        Testa se valida permissoes de acesso
        """
        if not self.urlBase is None:
            #Teste de insert
            response = self.client.post(self.urlBase+'addmembro/',{})
            self.assertEquals(response.status_code, 403)

            #Teste de delete
            response = self.client.post(self.urlBase+'delmembro/1/',{})
            self.assertEquals(response.status_code, 403)

            #Teste de permissão para visualizar staffs
            response = self.client.get(self.urlBase)
            self.assertTrue('panel-staff' not in response.content)

            #Teste de permissão para carregar staffs
            response = self.client.get(self.urlBase+'getstaff/')
            self.assertEquals(response.status_code, 200)

            #Teste de permissão para carregar membros
            response = self.client.get(self.urlBase+'getmembros/')
            self.assertEquals(response.status_code, 200)

            #Teste de permissão para carregar carteiras, retorna 404 porque nenhum membro foi add ainda
            response = self.client.get(self.urlBase+'carteira/1/')
            self.assertEquals(response.status_code, 404)

    def test_render_listpage(self):
        """
        Irá testar se adicionando a permissão que visualiza os staffs os mesmos irão aparecer
        """
        self.addPermissions()

        membro = Membro.objects.create(criador=self.user,usuario=self.user,criado='2014-01-01')
        membro.save()

        response = self.client.get(self.urlBase)
        self.assertTrue('panel-staff' in response.content)

    def test_return_data_to_list(self):
        """
        Verifica se retorna um usuário
        """
        membro = Membro.objects.create(criador=self.user,usuario=self.user,criado='2014-01-01')
        membro.save()

        response = self.client.get(self.urlBase+'getmembros/')
        self.assertEquals(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEquals(len(result),1)

    def test_insert(self):
        """
        Testa gravação dos dados no post de inclusão
        """
        self.addPermissions()
        # Faz chamada da pagina
        if not self.urlBase is None:
            self.prepare_to_post('test_insert')
            response = self.client.post(self.urlBase+'addmembro/', self.modelPost)
            self.assertContains(response, '"success": true', status_code=200)

            total = MembroHistorico.objects.count()
            self.assertTrue(total>0)


    def test_update(self):
        pass

    def test_delete(self):
        """
        Remove membro
        """
        self.addPermissions()
        # Faz chamada da pagina
        if not self.urlBase is None:
            self.prepare_to_post('test_delete')

            if not self.modelRow:
                self.assertTrue(False)

            totalBefore = self.modelStandard.objects.count()
            response = self.client.post(self.urlBase+'delmembro/'+str(self.modelRow.id)+'/',{})
            totalUpdated = self.modelStandard.objects.count()
        
            self.assertEquals(response.status_code, 200)
            self.assertTrue(totalBefore > totalUpdated)

    def test_carteira(self):
        """
        Retorna as carteiras de um membro
        """
        membro = Membro.objects.create(criador=self.user,usuario=self.user,criado='2014-01-01')
        membro.save()

        response = self.client.get(self.urlBase+'carteira/'+str(membro.id)+'/')
        self.assertEquals(response.status_code,200)

        filial = mommy.make(Filial)
        carteira = mommy.make('cliente.Carteira',filial=filial)

        data = {
            'carteiras' : [carteira.id]
        }

        response = self.client.post(self.urlBase+'carteira/'+str(membro.id)+'/',data)
        self.assertEquals(response.status_code,200)

    
    def prepare_to_post(self, fromDef):
        """
        Prepara dados para testar post
        """
        self.dataInsert['usuario_id'] = self.user.id

        if fromDef == 'test_insert':
            self.modelPost = self.dataInsert
        else:
            self.modelRow = mommy.make(
                self.modelStandard, 
                criador=self.user,
                usuario=self.user
            )
            self.modelPost = self.dataInsert