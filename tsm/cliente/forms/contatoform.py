# -*- coding: ISO-8859-1 -*-
import re
from datetime import date
from django import forms

from tsm.cliente.models.contato import Contato

class ContatoForm(forms.ModelForm):
    """
    Formulário de contatos
    """
    class Meta:
        model = Contato
        
    def get_absolute_url(self):
        return reverse('cliente.list_contato', kwargs={'pk': self.pk})

    def __init__(self, *args, **kwargs):
        from tsm.core.util import get_filiais

        from tsm.cliente.models.cliente import Cliente

        request = kwargs.pop('request')
        super(ContatoForm, self).__init__(*args, **kwargs)
        
        self.fields['cliente'].queryset = Cliente.objects.filter(filial__in=get_filiais(request.user.id))