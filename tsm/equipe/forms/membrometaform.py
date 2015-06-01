# -*- coding: ISO-8859-1 -*-
import re
from datetime import date
from django import forms

from tsm.equipe.models.membrometa import MembroMeta

class MembroMetaForm(forms.ModelForm):
    """
    Formulário de Inclusão
    """
    class Meta:
        model = MembroMeta
        
    def get_absolute_url(self):
        return reverse('equipe.list_membrometa', kwargs={'pk': self.pk})

    def __init__(self, *args, **kwargs):
        super(MembroMetaForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['membro'].widget = forms.HiddenInput()
        self.fields['criador'].widget = forms.HiddenInput()
        self.fields['valor'].widget = forms.TextInput()
        self.fields['valor'].widget.attrs['behaveas'] = 'float'