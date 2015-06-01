# -*- coding: ISO-8859-1 -*-
"""
Testes de oportunidades
"""
import json

from django.test import TestCase, Client
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from tsm.core.models.filial import Filial

from tsm.acesso.models.usuario import Usuario
from tsm.acesso.models.funcao import Funcao

from tsm.cliente.models.cliente import Cliente
from tsm.cliente.models.carteira import Carteira

from tsm.equipe.models.membro import Membro

from tsm.oportunidade.models.oportunidade import Oportunidade
from tsm.oportunidade.models.receita import Receita
from tsm.oportunidade.models.situacao import Situacao
from tsm.oportunidade.models.tipotemperatura import TipoTemperatura
from tsm.oportunidade.models.questao import Questao
from tsm.oportunidade.models.historico import Historico
from tsm.oportunidade.models.historicoresposta import HistoricoResposta

from model_mommy import mommy

class TestsOportundade(TestCase):
    funcao = None
    filial = None

    def setUp(self):
        self.data = {
            'username' : 'testuser',
            'senha'       : 'testpass',
            'email'       : 'test@test.com',
            'funcao'   : None
        }
        self.user = Usuario.objects.create_user(self.data['username'], self.data['email'], self.data['senha'])
        
        self.funcao = mommy.make(Funcao)
        self.filial = mommy.make('core.Filial',responsavel=self.user)
        self.tipotemperatura = mommy.make('oportunidade.TipoTemperatura',perc=10.00)
        self.carteira = mommy.make('cliente.Carteira', filial=self.filial)
        self.cliente = mommy.make(
            'cliente.Cliente',
            carteira=self.carteira,
            filial=self.filial,
            cnpj='44356778000103', 
            cep='99999-999', 
            estado='RJ'
        )
        self.receita = mommy.make(Receita)
        self.situacao = mommy.make(Situacao)
        
        self.user.funcao = self.funcao
        self.user.filiais.add(self.filial)
        self.user.save()

        self.client.login(username=self.data['username'], password=self.data['senha'])

    def addPermissions(self):
        """
        Adiciona permissoes ao usuario
        """
        #busca tabela de models
        contentItem = ContentType.objects.get(app_label='oportunidade',model='oportunidade')
        #busca permissoes do model
        if not contentItem:
            self.assertTrue(False)

        permissions = Permission.objects.all().filter(content_type=contentItem.id)
    
        for permission in permissions:
            self.user.user_permissions.add(permission)

    def test_grid(self):
        """
        Testes referente ao grid de oportunidades
        """
        #Acesso a tela
        response = self.client.get('/oportunidade/lista/')
        self.assertEqual(response.status_code, 200)

        #Retorno de dados no grid
        response = self.client.get('/oportunidade/lista/data/')
        self.assertContains(response, '"result": "ok"', status_code=200)

        """
        Verifica se só pode ver oportunidades pertinentes
        """
        #Cria dados para teste
        usuario1 = Usuario.objects.create_user('usuario1', 'usuario1@teste.com', 'usuario1')
        usuario2 = Usuario.objects.create_user('usuario2', 'usuario2@teste.com', 'usuario2')

        membro1 = Membro.objects.create(usuario=self.user,criador=self.user)
        membro2 = Membro.objects.create(usuario=usuario1, lider=membro1, criador=self.user)
        membro3 = Membro.objects.create(usuario=usuario2,criador=self.user)

        oportunidade1 = mommy.make(
            'oportunidade.Oportunidade',
            filial=self.filial,
            cliente=self.cliente,
            receita=self.receita,
            situacao=self.situacao,
            tipotemperatura=self.tipotemperatura,
            responsavel=usuario1,
            lider=self.user,
            criador=self.user
        )

        oportunidade2 = mommy.make(
            'oportunidade.Oportunidade',
            filial=self.filial,
            cliente=self.cliente,
            receita=self.receita,
            situacao=self.situacao,
            tipotemperatura=self.tipotemperatura,
            responsavel=usuario2,
            lider=usuario2,
            criador=self.user
        )

        #Testa retorno dos dados
        response = self.client.get('/oportunidade/lista/data/')
        self.assertEqual(response.status_code, 200)

        #Testa se a quantidade está correta
        result = json.loads(response.content)
        self.assertEquals(result['iTotalDisplayRecords'],1)

    def test_render_form(self):
        """
        Verifica renderização do formulário
        """
        #Verifica permissão
        response = self.client.get('/oportunidade/formulario/')
        self.assertEqual(response.status_code, 403)

        self.addPermissions()
        #Testa renderização do form
        response = self.client.get('/oportunidade/formulario/')
        self.assertEqual(response.status_code, 200)        

    def test_load_combo_cliente(self):
        """
        Testa o carregamento da combo de clientes apenas com os dados pertinentes
        à carteira do usuário
        """
        #Cria dados para teste
        usuario1 = Usuario.objects.create_user('usuario1', 'usuario1@teste.com', 'usuario1')
        usuario2 = Usuario.objects.create_user('usuario2', 'usuario2@teste.com', 'usuario2')

        membro1 = Membro.objects.create(usuario=self.user,criador=self.user)
        membro2 = Membro.objects.create(usuario=usuario1, lider=membro1, criador=self.user)
        membro3 = Membro.objects.create(usuario=usuario2,criador=self.user)

        #adiciona carteiras aos membros
        membro1.carteiras.add(self.carteira)
        membro2.carteiras.add(self.carteira)

        carteira1 = mommy.make('cliente.Carteira', filial=self.filial)
        cliente1 = mommy.make(
            'cliente.Cliente',
            nome='teste123',
            carteira=carteira1,
            filial=self.filial,
            cnpj='15260391000150', 
            cep='99999-999', 
            estado='RJ'
        )

        membro3.carteiras.add(carteira1)

        self.addPermissions()
        response = self.client.get('/oportunidade/formulario/')
        self.assertEqual(response.status_code, 200) #Testa se retorno está ok
        self.assertTrue(cliente1.nome not in response.content) #Testa se conteúdo está correto

    def test_load_combo_responsavel(self):
        """
        Testa o carregamento da combo de responsável apenas com os dados pertinentes
        ao usuário
        """
        #Cria dados para teste
        usuario1 = Usuario.objects.create_user('usuario1', 'usuario1@teste.com', 'usuario1')
        usuario2 = Usuario.objects.create_user('usuario2', 'usuario2@teste.com', 'usuario2')

        usuario1.first_name = 'usuario1'
        usuario1.last_name = 'usuario1teste'
        usuario1.save()

        usuario2.first_name = 'usuario2'
        usuario2.last_name = 'usuario2teste'
        usuario2.save()

        membro1 = Membro.objects.create(usuario=self.user,criador=self.user)
        membro2 = Membro.objects.create(usuario=usuario1, lider=membro1, criador=self.user)
        membro3 = Membro.objects.create(usuario=usuario2,criador=self.user)

        #adiciona carteiras aos membros
        membro1.carteiras.add(self.carteira)
        membro2.carteiras.add(self.carteira)

        self.addPermissions()
        response = self.client.get('/oportunidade/formulario/')
        self.assertEqual(response.status_code, 200) #Testa retorno do formulário

        #Testa se o conteúdo está correto
        self.assertTrue(membro3.usuario.first_name not in response.content)
        self.assertTrue(membro3.usuario.last_name not in response.content)

    def test_load_combo_lider(self):
        """
        Testa o carregamento da combo de líderes com retorno em json com os líderes
        possíveis para seleção
        """
        #Cria dados para teste
        usuario1 = Usuario.objects.create_user('usuario1', 'usuario1@teste.com', 'usuario1')
        usuario2 = Usuario.objects.create_user('usuario2', 'usuario2@teste.com', 'usuario2')

        membro1 = Membro.objects.create(usuario=self.user,criador=self.user)
        membro2 = Membro.objects.create(usuario=usuario1, lider=membro1, criador=self.user)

        response = self.client.get('/oportunidade/formulario/getlider/'+str(membro2.usuario.id)+'/')
        self.assertEqual(response.status_code, 200) #Testa retorno da requisição
        
        result = json.loads(response.content)
        self.assertTrue(len(result)) #Testa se retornou com dados

    def test_inset(self):
        """
        Teste de inclusão de oportunidades
        """
        usuario1 = Usuario.objects.create_user('usuario1', 'usuario1@teste.com', 'usuario1')
        usuario2 = Usuario.objects.create_user('usuario2', 'usuario2@teste.com', 'usuario2')

        usuario1.first_name = 'usuario1'
        usuario1.last_name = 'usuario1teste'
        usuario1.save()

        usuario2.first_name = 'usuario2'
        usuario2.last_name = 'usuario2teste'
        usuario2.save()

        membro1 = Membro.objects.create(usuario=self.user,criador=self.user)
        membro2 = Membro.objects.create(usuario=usuario1, lider=membro1, criador=self.user)
        membro3 = Membro.objects.create(usuario=usuario2,criador=self.user)

        #adiciona carteiras aos membros
        membro1.carteiras.add(self.carteira)
        membro2.carteiras.add(self.carteira)

        questao1 = mommy.make(
            'oportunidade.Questao',
            filial=self.filial
        )

        self.addPermissions()
        dataPost = {
            'filial':self.filial.id,
            'cliente':self.cliente.id,
            'receita':self.receita.id,
            'situacao':self.situacao.id,
            'tipotemperatura':self.tipotemperatura.id,
            'temperatura_auto':'Baixa',
            'responsavel':usuario1.id,
            'lider':self.user.id,
            'dtFechamento':'2014-05-01',
            'valor':9000,
            'respostas':[],
            'criador':self.user.id,
        }

        response = self.client.post('/oportunidade/formulario/',dataPost)
        self.assertEqual(response.status_code, 400) #Testa se bloqueou inclusão por não ter respostas

        dataPost = {
            'filial':self.filial.id,
            'cliente':self.cliente.id,
            'receita':self.receita.id,
            'situacao':self.situacao.id,
            'tipotemperatura':self.tipotemperatura.id,
            'temperatura_auto':'Média',
            'responsavel':usuario1.id,
            'lider':self.user.id,
            'dtFechamento':'2014-05-01',
            'valor':9000,
            'respostas[]': [{
                "questao":questao1.id,
                "resposta":True
            }],
            'criador':self.user.id,
        }

        response = self.client.post('/oportunidade/formulario/',dataPost)
        self.assertEqual(response.status_code, 200) #Testa se o retorno do post está ok

        oportunidades = Oportunidade.objects.count()
        self.assertTrue(oportunidades) #Testa se incluiu oportunidade

        historicos = Historico.objects.count()
        self.assertTrue(historicos) #Testa se gravou histórico

    def test_acesso_bloqueado(self):
        """
        Testa se bloqueia acesso a acesso via get de oportunidades
        que não pertencem ao usuário
        """
        usuario1 = Usuario.objects.create_user('usuario1', 'usuario1@teste.com', 'usuario1')
        usuario2 = Usuario.objects.create_user('usuario2', 'usuario2@teste.com', 'usuario2')

        usuario1.first_name = 'usuario1'
        usuario1.last_name = 'usuario1teste'
        usuario1.save()

        usuario2.first_name = 'usuario2'
        usuario2.last_name = 'usuario2teste'
        usuario2.save()

        membro1 = Membro.objects.create(usuario=self.user,criador=self.user)
        membro2 = Membro.objects.create(usuario=usuario1, lider=membro1, criador=self.user)
        membro3 = Membro.objects.create(usuario=usuario2,criador=self.user)

        #adiciona carteiras aos membros
        membro1.carteiras.add(self.carteira)
        membro2.carteiras.add(self.carteira)

        questao1 = mommy.make(
            'oportunidade.Questao',
            filial=self.filial
        )

        self.addPermissions()
        oportunidade = Oportunidade.objects.create(
            filial=self.filial,
            cliente=self.cliente,
            receita=self.receita,
            situacao=self.situacao,
            tipotemperatura=self.tipotemperatura,
            temperatura_auto='Média',
            responsavel=membro3.usuario,
            lider=membro3.usuario,
            dtFechamento='2014-05-01',
            valor=9000.00,
            criador=membro3.usuario,
        )
        oportunidade.save()

        response = self.client.get('/oportunidade/editar/'+str(oportunidade.id)+'/')
        self.assertEqual(response.status_code, 404) #Testa se retorna acesso negado

        oportunidade2 = Oportunidade.objects.create(
            filial=self.filial,
            cliente=self.cliente,
            receita=self.receita,
            situacao=self.situacao,
            tipotemperatura=self.tipotemperatura,
            temperatura_auto='Média',
            responsavel=membro2.usuario,
            lider=membro1.usuario,
            dtFechamento='2014-05-01',
            valor=9000,
            criador=membro1.usuario,
        )
        oportunidade.save()

        response = self.client.get('/oportunidade/editar/'+str(oportunidade2.id)+'/')
        self.assertEqual(response.status_code, 200) #Testa se retorna o que é de direito

    def test_fields_bloq(self):
        """
        Testa se os campos estão bloqueados como deveriam estar na edição
        """
        usuario1 = Usuario.objects.create_user('usuario1', 'usuario1@teste.com', 'usuario1')

        membro1 = Membro.objects.create(usuario=self.user,criador=self.user)
        membro2 = Membro.objects.create(usuario=usuario1, lider=membro1, criador=self.user)

        #adiciona carteiras aos membros
        membro1.carteiras.add(self.carteira)
        membro2.carteiras.add(self.carteira)

        questao1 = mommy.make(
            'oportunidade.Questao',
            filial=self.filial
        )

        self.addPermissions()
        oportunidade = Oportunidade.objects.create(
            filial=self.filial,
            cliente=self.cliente,
            receita=self.receita,
            situacao=self.situacao,
            tipotemperatura=self.tipotemperatura,
            temperatura_auto='Média',
            responsavel=membro2.usuario,
            lider=membro1.usuario,
            dtFechamento='2014-05-01',
            valor=9000,
            criador=membro1.usuario,
        )
        oportunidade.save()

        response = self.client.get('/oportunidade/editar/'+str(oportunidade.id)+'/')
        self.assertEqual(response.status_code, 200) #Testa se retorna o que é de direito

        #Verifica campos que devem ficar desabilitados
        self.assertContains(response,'disabled="True" id="id_lider"')
        self.assertContains(response,'disabled="True" id="id_responsavel"')
        self.assertContains(response,'disabled="True" id="id_receita"')
        self.assertContains(response,'disabled="True" id="id_cliente"')
    
    def test_update(self):
        """
        Teste de atualização das informações
        """
        usuario1 = Usuario.objects.create_user('usuario1', 'usuario1@teste.com', 'usuario1')

        membro1 = Membro.objects.create(usuario=self.user,criador=self.user)
        membro2 = Membro.objects.create(usuario=usuario1, lider=membro1, criador=self.user)

        #adiciona carteiras aos membros
        membro1.carteiras.add(self.carteira)
        membro2.carteiras.add(self.carteira)

        questao1 = mommy.make(
            'oportunidade.Questao',
            filial=self.filial
        )

        self.addPermissions()
        oportunidade = Oportunidade.objects.create(
            filial=self.filial,
            cliente=self.cliente,
            receita=self.receita,
            situacao=self.situacao,
            tipotemperatura=self.tipotemperatura,
            temperatura_auto='Média',
            responsavel=membro2.usuario,
            lider=membro1.usuario,
            dtFechamento='2014-05-01',
            valor=9000,
            criador=membro1.usuario,
        )
        oportunidade.save()

        situacaoNew = mommy.make(Situacao)
        dataPost = {
            'filial':oportunidade.filial.id,
            'cliente':oportunidade.cliente.id,
            'receita':oportunidade.receita.id,
            'situacao':situacaoNew.id,
            'tipotemperatura':oportunidade.tipotemperatura.id,
            'temperatura_auto':'Alta',
            'responsavel':oportunidade.responsavel.id,
            'lider':oportunidade.lider.id,
            'valor':oportunidade.valor,
            'dtFechamento':oportunidade.dtFechamento,
            'criador':oportunidade.criador.id,
        }

        oldTotal = Historico.objects.count()
        response = self.client.post('/oportunidade/editar/'+str(oportunidade.id)+'/',dataPost)
        self.assertEqual(response.status_code, 200) #Testa se retorna o que é de direito

        #Teste para ver se grava histórico
        newTotal = Historico.objects.count()
        self.assertTrue(oldTotal<newTotal)

    def test_answer(self):
        from tsm.oportunidade.models.resposta import Resposta
        """
        Testa se as respostas estão sendo incluídas
        """
        usuario1 = Usuario.objects.create_user('usuario1', 'usuario1@teste.com', 'usuario1')

        membro1 = Membro.objects.create(usuario=self.user,criador=self.user)
        membro2 = Membro.objects.create(usuario=usuario1, lider=membro1, criador=self.user)

        #adiciona carteiras aos membros
        membro1.carteiras.add(self.carteira)
        membro2.carteiras.add(self.carteira)

        questao1 = mommy.make(
            'oportunidade.Questao',
            filial=self.filial
        )

        self.addPermissions()

        #Testa se respostas foram incluídas na inclusão da oportunidade
        dataPost = {
            'filial':self.filial.id,
            'cliente':self.cliente.id,
            'receita':self.receita.id,
            'situacao':self.situacao.id,
            'tipotemperatura':self.tipotemperatura.id,
            'temperatura_auto':'Média',
            'responsavel':usuario1.id,
            'lider':self.user.id,
            'dtFechamento':'2014-05-01',
            'valor':9000,
            'respostas[]': [{
                "questao":questao1.id,
                "resposta":True
            }],
            'criador':self.user.id,
        }
        response = self.client.post('/oportunidade/formulario/',dataPost)
        self.assertEqual(response.status_code, 200)
        respostas = Resposta.objects.count()
        self.assertTrue(respostas)

        #Testa se inclui resposta no update
        oportunidade = Oportunidade.objects.latest('id')
        situacaoNew = mommy.make(Situacao)
        dataPost = {
            'filial':oportunidade.filial.id,
            'cliente':oportunidade.cliente.id,
            'receita':oportunidade.receita.id,
            'situacao':situacaoNew.id,
            'tipotemperatura':oportunidade.tipotemperatura.id,
            'temperatura_auto':'Alta',
            'responsavel':oportunidade.responsavel.id,
            'lider':oportunidade.lider.id,
            'valor':oportunidade.valor,
            'dtFechamento':oportunidade.dtFechamento,
            'criador':oportunidade.criador.id,
            'respostas[]': [{
                "questao":questao1.id,
                "resposta":False
            }]
        }
        response = self.client.post('/oportunidade/editar/'+str(oportunidade.id)+'/',dataPost)
        self.assertEqual(response.status_code, 200)

        #testa se gravou histórico
        totalHist = HistoricoResposta.objects.count()
        self.assertTrue(totalHist)

    def test_calc_temp_auto(self):
        """
        Calcula temperatura automática
        """
        questao1 = mommy.make(
            'oportunidade.Questao',
            filial=self.filial
        )
        dataPost = {
            "respostas[]" : [{
                "id" : questao1.id,
                "resposta": True
            }]
        }
        response = self.client.post('/oportunidade/calculatemp/',dataPost)
        self.assertEqual(response.status_code, 200)