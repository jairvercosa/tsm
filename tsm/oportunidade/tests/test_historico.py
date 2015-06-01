# -*- coding: ISO-8859-1 -*-
"""
Testes de histórico
"""
import json

from django.test import TestCase, Client
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from tsm.core.models.filial import Filial
from tsm.acesso.models.usuario import Usuario

class TestsOportundade(TestCase):
    def setUp(self):
        self.data = {
            'username' : 'testuser',
            'senha'       : 'testpass',
            'email'       : 'test@test.com',
            'funcao'   : None
        }
        self.user = Usuario.objects.create_user(self.data['username'], self.data['email'], self.data['senha'])
        self.client.login(username=self.data['username'], password=self.data['senha'])

    def test_acesso(self):
        #Acesso a tela
        response = self.client.get('/oportunidade/historico/')
        self.assertEqual(response.status_code, 200)

        #Retorno aos dados
        response = self.client.get('/oportunidade/historico/data/')
        self.assertContains(response, '"result": "ok"', status_code=200)