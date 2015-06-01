# -*- coding: ISO-8859-1 -*-
from tsm.core.base.core_base_test import Testsbase
from tsm.oportunidade.models.receita import Receita

class TestsReceitas(Testsbase):
    modelStandard = Receita
    modelMommy = 'oportunidade.Receita'
    urlBase = '/oportunidade/receita/'
    fieldTestRender = 'nome'
    dataInsert = {
        'nome'  : 'PAR_01'
    }