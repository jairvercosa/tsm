# -*- coding: ISO-8859-1 -*-
import re
from datetime import date
from django import forms

from tsm.core.models.parametro import Parametro

class ParametroForm(forms.ModelForm):
    """
    Formulário de parâmetros
    """
    class Meta:
        model = Parametro
        
    def get_absolute_url(self):
        return reverse('core.list_parametro', kwargs={'pk': self.pk})

    def __init__(self, *args, **kwargs):
        from tsm.core.util import get_filiais
        request = kwargs.pop('request')
        super(ParametroForm, self).__init__(*args, **kwargs)
        
        self.fields['filial'].queryset = get_filiais(request.user.id)