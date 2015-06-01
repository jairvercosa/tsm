# -*- coding: ISO-8859-1 -*-
from datetime import date
from django import forms

from tsm.core import util
from tsm.oportunidade.models.rtc import Rtc

class RtcForm(forms.ModelForm):
    user = None
    """
    Formulário
    """
    class Meta:
        model = Rtc
        
    def get_absolute_url(self):
        return reverse('oportunidade.list_rtc', kwargs={'pk': self.pk})

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        self.user = request.user

        super(RtcForm, self).__init__(*args, **kwargs)
        self.fields['oportunidade'].widget = forms.HiddenInput()
        self.fields.keyOrder = ['oportunidade', 'data', 'hora', 'descricao', 'recursos']

    def clean_data(self):
        """
        Valida se é dia útil
        """
        if "data" in self.initial:
            data = self.initial["data"]
        else:
            data = None

        if data != self.cleaned_data.get('data'):
            dataFromForm = self.cleaned_data.get('data')
            isDiaUtil, message = util.isDiaUtil(dataFromForm,self.user)
            if not isDiaUtil:
                raise forms.ValidationError(message)
            else:
                return dataFromForm
        else:
            return self.initial["data"]
        