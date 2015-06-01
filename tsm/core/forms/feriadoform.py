# -*- coding: ISO-8859-1 -*-
from datetime import date
from django import forms

from tsm.core.models.feriado import Feriado

class FeriadoForm(forms.ModelForm):
    """
    Formulário de feriados
    """
    class Meta:
        model = Feriado
        
    def get_absolute_url(self):
        return reverse('core.list_feriados', kwargs={'pk': self.pk})

    def __init__(self, *args, **kwargs):
        from tsm.core.util import get_filiais
        
        request = kwargs.pop('request')
        super(FeriadoForm, self).__init__(*args, **kwargs)
        
        self.fields['filial'].queryset = get_filiais(request.user.id)