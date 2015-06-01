# -*- coding: ISO-8859-1 -*-
from tsm.core.base.core_base_test import Testsbase
from tsm.cliente.models.segmento import Segmento

class TestsSegmento(Testsbase):
    modelStandard = Segmento
    modelMommy = 'cliente.Segmento'
    urlBase = '/cliente/segmentos/'
    fieldTestRender = 'nome'
    dataInsert = {
        'nome'  : 'Name1',
        'cnae'  : '990099',
        'subsegmento': 'Subsegmento1'
    }