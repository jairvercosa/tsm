# -*- coding: ISO-8859-1 -*-
from model_mommy import mommy

from tsm.core.base.core_base_test import Testsbase
from tsm.oportunidade.models.questao import Questao

class TestsQuestao(Testsbase):
    modelStandard = Questao
    modelMommy = 'oportunidade.Questao'
    urlBase = '/oportunidade/questoes/'
    fieldTestRender = 'pergunta'
    dataInsert = {
        'ordem' : '1',
        'pergunta' :'Pergunta1',
        'sim' : 1,
        'nao' :-1,
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
        if fromDef == 'test_insert':
            self.modelPost = self.dataInsert
        else:
            self.modelRow = mommy.make(self.modelStandard, filial=filial)
            self.modelPost = self.dataInsert