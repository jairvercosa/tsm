# -*- coding: ISO-8859-1 -*-
from tsm.core.base.core_base_test import Testsbase
from tsm.cliente.models.fabricante import Fabricante

class TestsFabricante(Testsbase):
    modelStandard = Fabricante
    modelMommy = 'cliente.Fabricante'
    urlBase = '/cliente/fabricantes/'
    fieldTestRender = 'nome'
    dataInsert = {
        'nome'  : 'PAR_01',
    }