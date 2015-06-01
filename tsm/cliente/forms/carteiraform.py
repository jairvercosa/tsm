# -*- coding: ISO-8859-1 -*-
import re
from datetime import date
from django import forms

from tsm.cliente.models.carteira import Carteira

class CarteiraForm(forms.ModelForm):
    """
    Formulário de carteiras
    """
    class Meta:
        model = Carteira
        
    def get_absolute_url(self):
        return reverse('cliente.list_carteira', kwargs={'pk': self.pk})

    def __init__(self, *args, **kwargs):
        from tsm.core.util import get_filiais
        request = kwargs.pop('request')
        super(CarteiraForm, self).__init__(*args, **kwargs)
        
        self.fields['filial'].queryset = get_filiais(request.user.id)