# -*- coding: ISO-8859-1 -*-
from model_mommy import mommy

from tsm.core.base.core_base_test import Testsbase
from tsm.equipe.models.tipometa import TipoMeta

class TestsTipometa(Testsbase):
    modelStandard = TipoMeta
    modelMommy = 'equipe.TipoMeta'
    urlBase = '/equipe/tipometa/'
    fieldTestRender = 'nome'
    dataInsert = {
        'nome'  : 'PAR_01',
        'filial': None,
    }

    def prepare_to_post(self, fromDef):
        """
        Prepara dados para testar post
        """
        filial = mommy.make('core.Filial',responsavel=self.user)
        self.user.filiais.add(filial)
        self.user.save()
        self.dataInsert['filial'] = filial.id

        if fromDef == 'test_insert':
            self.modelPost = self.dataInsert
        else:
            self.modelRow = mommy.make(self.modelStandard, filial=filial)
            self.modelPost = self.dataInsert