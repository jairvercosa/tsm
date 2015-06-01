# -*- coding: ISO-8859-1 -*-
from model_mommy import mommy
from tsm.core.base.core_base_test import Testsbase
from tsm.cliente.models.contato import Contato
from tsm.cliente.models.cliente import Cliente

class TestsContato(Testsbase):
    modelStandard = Contato
    modelMommy = 'cliente.Contato'
    urlBase = '/cliente/contatos/'
    fieldTestRender = 'nome'
    dataInsert = {
        'nome'  : 'PAR_01',
        'telefone'  : 'telefone1',
        'celular'  : 'celular1',
        'email' : 'email@email.com',
        'cargo' : 'teste',
        'cliente': None
    }

    def prepare_to_post(self, fromDef):
        """
        Prepara dados para testar post
        """
        filial = mommy.make('core.Filial',responsavel=self.user)
        self.user.filiais.add(filial)
        self.user.save()
        carteira = mommy.make('cliente.Carteira', filial=filial)

        cliente = mommy.make(Cliente, filial=filial, carteira=carteira)
        self.dataInsert['cliente'] = cliente.id

        if fromDef == 'test_insert':
            self.modelPost = self.dataInsert
        else:
            self.modelRow = mommy.make(self.modelStandard, cliente=cliente)
            self.modelPost = self.dataInsert