# -*- coding: ISO-8859-1 -*-
from model_mommy import mommy
from tsm.core.base.core_base_test import Testsbase
from tsm.cliente.models.produto import Produto

class TestsProduto(Testsbase):
    modelStandard = Produto
    modelMommy = 'cliente.Produto'
    urlBase = '/cliente/produtos/'
    fieldTestRender = 'nome'
    dataInsert = {
        'nome'  : 'PAR_01',
        'segmento'  : 'segmento1',
        'fabricante'  : None,
        'filial' : None,
    }

    def prepare_to_post(self, fromDef):
        """
        Prepara dados para testar post
        """
        filial = mommy.make('core.Filial',responsavel=self.user)
        
        self.user.filiais.add(filial)
        self.user.save()
        self.dataInsert['filial'] = filial.id

        fabricante = mommy.make('cliente.Fabricante')
        self.dataInsert['fabricante'] = fabricante.id

        if fromDef == 'test_insert':
            self.modelPost = self.dataInsert
        else:
            self.modelRow = mommy.make(self.modelStandard, filial=filial, fabricante=fabricante)
            self.modelPost = self.dataInsert