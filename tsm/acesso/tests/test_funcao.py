# -*- coding: ISO-8859-1 -*-
from tsm.core.base.core_base_test import Testsbase
from tsm.acesso.models.funcao import Funcao

class TestsFuncao(Testsbase):
    modelStandard = Funcao
    modelMommy = 'acesso.Funcao'
    urlBase = '/acesso/funcoes/'
    fieldTestRender = 'nome'
    dataInsert = {
        'nome'  : 'PAR_01',
    }