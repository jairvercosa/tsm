# -*- coding: ISO-8859-1 -*-
from django import forms

from tsm.equipe.models.membrometahistorico import MembroMetaHistorico

class MembroMetaHistoricoForm(forms.ModelForm):
    class Meta:
        model = MembroMetaHistorico
        
    def get_absolute_url(self):
        return reverse('equipe.list_membrometa', kwargs={'pk': self.pk})

    def __init__(self, *args, **kwargs):
        super(MembroMetaHistoricoForm, self).__init__(*args, **kwargs)
        self.fields['nome_usuario_add'].widget.attrs['disabled'] = True
        self.fields['nome_membro'].widget.attrs['disabled'] = True
        self.fields['nome_lider'].widget.attrs['disabled'] = True
        self.fields['nome_tipometa'].widget.attrs['disabled'] = True
        self.fields['valor'].widget.attrs['disabled'] = True
        self.fields['criado'].widget.attrs['disabled'] = True