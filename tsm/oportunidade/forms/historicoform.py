# -*- coding: ISO-8859-1 -*-
import re
from datetime import date
from django import forms

from tsm.oportunidade.models.historico import Historico

class HistoricoForm(forms.ModelForm):
    """
    Formulário de históricos
    """
    class Meta:
        model = Historico
        
    def get_absolute_url(self):
        return reverse('oportunidade.list_historico', kwargs={'pk': self.pk})

    def __init__(self, *args, **kwargs):
        super(HistoricoForm, self).__init__(*args, **kwargs)
        
        self.fields['oportunidade'].widget.attrs['disabled'] = True
        self.fields['criado'].widget.attrs['disabled'] = True
        self.fields['nome_usuario_add'].widget.attrs['disabled'] = True
        self.fields['nome_situacao'].widget.attrs['disabled'] = True
        self.fields['nome_tipotemperatura'].widget.attrs['disabled'] = True
        self.fields['nome_responsavel'].widget.attrs['disabled'] = True
        self.fields['nome_lider'].widget.attrs['disabled'] = True
        self.fields['valor'].widget.attrs['disabled'] = True
        self.fields['ponderado'].widget.attrs['disabled'] = True
        self.fields['temperatura_auto'].widget.attrs['disabled'] = True
        self.fields['dtFechamento'].widget.attrs['disabled'] = True
        self.fields['obs'].widget.attrs['disabled'] = True
        self.fields['nome_gpp'].widget.attrs['disabled'] = True
        self.fields['nome_arquitetos'].widget.attrs['disabled'] = True
        self.fields['dtFechado'].widget.attrs['disabled'] = True