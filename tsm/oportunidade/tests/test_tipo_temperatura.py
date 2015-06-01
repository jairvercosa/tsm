# -*- coding: ISO-8859-1 -*-
from tsm.core.base.core_base_test import Testsbase
from tsm.oportunidade.models.tipotemperatura import TipoTemperatura

class Teststipotemperatura(Testsbase):
    modelStandard = TipoTemperatura
    modelMommy = 'oportunidade.TipoTemperatura'
    urlBase = '/oportunidade/tipotemperatura/'
    fieldTestRender = 'nome'
    dataInsert = {
        'nome'  : 'PAR_01',
        'perc' : 90,
        'tipo' : 'G',
    }