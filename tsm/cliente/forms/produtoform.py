# -*- coding: ISO-8859-1 -*-
import re
from datetime import date
from django import forms

from tsm.cliente.models.produto import Produto

class ProdutoForm(forms.ModelForm):
    """
    Formulário de produtos
    """
    class Meta:
        model = Produto
        
    def get_absolute_url(self):
        return reverse('cliente.list_produto', kwargs={'pk': self.pk})

    def __init__(self, *args, **kwargs):
        from tsm.core.util import get_filiais
        request = kwargs.pop('request')
        super(ProdutoForm, self).__init__(*args, **kwargs)
        
        self.fields['filial'].queryset = get_filiais(request.user.id)