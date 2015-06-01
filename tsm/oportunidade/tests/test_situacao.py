# -*- coding: ISO-8859-1 -*-
from tsm.core.base.core_base_test import Testsbase
from tsm.oportunidade.models.situacao import Situacao

class Testssituacao(Testsbase):
    modelStandard = Situacao
    modelMommy = 'oportunidade.Situacao'
    urlBase = '/oportunidade/situacao/'
    fieldTestRender = 'nome'
    dataInsert = {
        'nome'  : 'PAR_01',
        'perc'  : 10.00,
        'fator' : 1.1,
        'operador': 'D',
    }