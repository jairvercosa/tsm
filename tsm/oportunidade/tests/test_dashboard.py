# -*- coding: ISO-8859-1 -*-
"""
Testes para dashboard
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

from model_mommy import mommy

class TestsOportundade(TestCase):
    funcao = None
    filial = None
    tipotemperatura = None
    carteira = None
    cliente = None
    receita = None
    situacao = None

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
        self.tipotemperatura = mommy.make('oportunidade.TipoTemperatura', perc=93.00)
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

        #Cria dados para teste
        usuario1 = Usuario.objects.create_user('usuario1', 'usuario1@teste.com', 'usuario1')
        usuario2 = Usuario.objects.create_user('usuario2', 'usuario2@teste.com', 'usuario2')

        membro1 = Membro.objects.create(usuario=self.user,criador=self.user)
        membro2 = Membro.objects.create(usuario=usuario1, lider=membro1, criador=self.user)
        membro3 = Membro.objects.create(usuario=usuario2,criador=self.user)

        self.oportunidade1 = mommy.make(
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

        self.oportunidade2 = mommy.make(
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

        self.client.login(username=self.data['username'], password=self.data['senha'])

    def add_permissions(self):
        #busca tabela de models
        contentItem = ContentType.objects.get(app_label='oportunidade',model='oportunidade')
        #busca permissoes do model
        if not contentItem:
            self.assertTrue(False)

        customPermission = Permission(name='Dashboard',content_type=contentItem,codename='index_dashboard')
        customPermission.save()

        permissions = Permission.objects.filter(content_type=contentItem.id)
    
        for permission in permissions:
            self.user.user_permissions.add(permission)

    def test_open_dashboard(self):
        #Teste de permissão

        """
        Este teste precisa ser reformulado aplicando as regras dos widgets exibidos no dashboard - 16/06/2014
        """
        response = self.client.get('/oportunidade/dashboard/')
        self.assertEqual(response.status_code, 403)
        self.add_permissions()

        response = self.client.get('/oportunidade/dashboard/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/oportunidade/dashboard/data/')
        self.assertEqual(response.status_code, 200)