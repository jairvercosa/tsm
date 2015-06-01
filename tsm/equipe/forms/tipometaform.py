# -*- coding: ISO-8859-1 -*-
import re
from datetime import date
from django import forms

from tsm.equipe.models.tipometa import TipoMeta

class TipoMetaForm(forms.ModelForm):
    """
    Formulário de Tipos de meta
    """
    class Meta:
        model = TipoMeta
        
    def get_absolute_url(self):
        return reverse('equipe.list_tipometa', kwargs={'pk': self.pk})

    def __init__(self, *args, **kwargs):
        from tsm.core.util import get_filiais
        request = kwargs.pop('request')
        
        super(TipoMetaForm, self).__init__(*args, **kwargs)
        
        self.fields['filial'].queryset = get_filiais(request.user.id)