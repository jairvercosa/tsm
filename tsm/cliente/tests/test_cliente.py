# -*- coding: ISO-8859-1 -*-
from model_mommy import mommy
from tsm.core.base.core_base_test import Testsbase

from tsm.cliente.models.cliente import Cliente

class TestsCliente(Testsbase):
    modelStandard = Cliente
    modelMommy = 'cliente.Cliente'
    urlBase = '/cliente/clientes/'
    fieldTestRender = 'nome'
    dataInsert = {
        'nome' : 'Empresa Teste',
        'cnpj' : '44356778000103',
        'criado' : '2014-03-13',
        'filial' : None,
        'carteira': None,
        'estado': 'RJ',
    }

    def prepare_to_post(self, fromDef):
        """
        Prepara dados para testar post
        """
        filial = mommy.make('core.Filial',responsavel=self.user)
        self.dataInsert['filial'] = filial.id
        self.user.filiais.add(filial)
        self.user.save()

        carteira = mommy.make('cliente.Carteira',filial=filial)
        self.dataInsert['carteira'] = carteira.id
        if fromDef == 'test_insert':
            self.modelPost = self.dataInsert
        else:
            self.modelRow = mommy.make(self.modelStandard, filial=filial, carteira=carteira, cnpj='44356778000103', cep='99999-999', estado='RJ')
            self.modelPost = self.dataInsert