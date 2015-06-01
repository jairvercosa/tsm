# -*- coding: ISO-8859-1 -*-
from django import forms

from tsm.equipe.models.membrohistorico import MembroHistorico

class MembroHistoricoForm(forms.ModelForm):
    class Meta:
        model = MembroHistorico
        
    def get_absolute_url(self):
        return reverse('equipe.list_membrometa', kwargs={'pk': self.pk})

    def __init__(self, *args, **kwargs):
        super(MembroHistoricoForm, self).__init__(*args, **kwargs)
        self.fields['nome_usuario_add'].widget.attrs['disabled'] = True
        self.fields['nome_membro'].widget.attrs['disabled'] = True
        self.fields['nome_lider'].widget.attrs['disabled'] = True
        self.fields['criado'].widget.attrs['disabled'] = True