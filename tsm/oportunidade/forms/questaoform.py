# -*- coding: ISO-8859-1 -*-
import re
from datetime import date
from django import forms

from tsm.oportunidade.models.questao import Questao

class QuestaoForm(forms.ModelForm):
    """
    Formulário de carteiras
    """
    class Meta:
        model = Questao
        
    def get_absolute_url(self):
        return reverse('oportunidade.list_questao', kwargs={'pk': self.pk})

    def __init__(self, *args, **kwargs):
        from tsm.core.util import get_filiais
        request = kwargs.pop('request')
        super(QuestaoForm, self).__init__(*args, **kwargs)
        
        self.fields['filial'].queryset = get_filiais(request.user.id)