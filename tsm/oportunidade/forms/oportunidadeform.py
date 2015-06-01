# -*- coding: ISO-8859-1 -*-
from datetime import date
from django import forms
from django.utils.safestring import mark_safe

from tsm.core.util import format_number
from tsm.core.base.core_widgets_form import CustomWidgetComboAdd
from tsm.oportunidade.models.oportunidade import Oportunidade
from tsm.cliente.models.cliente import Cliente
from tsm.acesso.models.usuario import Usuario

fieldOrder = [
    'criador', 'filial', 'cliente', 'receita',  'produto', 'situacao', 'codcrm', 'valor', 
    'temperatura_auto', 'tipotemperatura', 'responsavel', 'lider', 'dtFechamento',
    'obs', 'rtc', 'arquitetos', 'gpp', 'origem',
]

class OportunidadeForm(forms.ModelForm):
    """
    Formulário de Inclusão
    """

    class Meta:
        model = Oportunidade

    def __init__(self, *args, **kwargs):
        carteiras = None
        liderados = None
        lider = None
        filiais = None
        arquitetos = None
        gpp = None
        produtos = None
        request = None

        if 'carteiras' in kwargs:
            carteiras = kwargs.pop('carteiras')

        if 'liderados' in kwargs:
            liderados = kwargs.pop('liderados')

        if 'lider' in kwargs:
            lider = kwargs.pop('lider')

        if 'filiais' in kwargs:
            filiais = kwargs.pop('filiais')

        if 'arquitetos' in kwargs:
            arquitetos = kwargs.pop('arquitetos')

        if 'gpp' in kwargs:
            gpp = kwargs.pop('gpp')

        if 'produtos' in kwargs:
            produtos = kwargs.pop('produtos')

        if 'request' in kwargs:
            request = kwargs.pop('request')

        super(OportunidadeForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = fieldOrder

        if request:
            if request.user.has_perm('cliente.add_cliente'):
                self.fields['cliente'].widget = CustomWidgetComboAdd()

            if request.user.has_perm('oportunidade.can_change_mw_bc'):
                if 'mw' not in fieldOrder:
                    fieldOrder.append('mw')

                if 'bc' not in fieldOrder:
                    fieldOrder.append('bc')

        if carteiras:
            self.fields['cliente'].queryset = Cliente.objects.filter(id__in=carteiras)
        
        if liderados:
            self.fields['responsavel'].queryset = liderados

        if lider:
            self.fields['lider'].queryset = lider

        if filiais:
            self.fields['filial'].queryset = filiais

        if arquitetos:
            self.fields['arquitetos'].queryset = arquitetos
            
        if produtos:
            self.fields['produto'].queryset = produtos

        if gpp:
            self.fields['gpp'].queryset = gpp

        self.fields['criador'].widget = forms.HiddenInput()
        self.fields['valor'].widget = forms.TextInput()
        self.fields['valor'].widget.attrs['behaveas'] = 'float'
        self.fields['temperatura_auto'].widget.attrs['disabled'] = True
        
    def get_absolute_url(self):
        return reverse('oportunidade.list_oportunidade', kwargs={'pk': self.pk})

class OportunidadeFormUpdate(forms.ModelForm):
    """
    Formulário para Update
    """
    class Meta:
        model = Oportunidade

    def __init__(self, *args, **kwargs):
        liderados = None
        lider = None
        user = None
        arquitetos = None
        gpp = None
        produtos = None
        tipotemperatura = None

        if 'liderados' in kwargs:
            liderados = kwargs.pop('liderados')

        if 'lider' in kwargs:
            lider = kwargs.pop('lider')

        if 'user' in kwargs:
            user = kwargs.pop('user')

        if 'arquitetos' in kwargs:
            arquitetos = kwargs.pop('arquitetos')

        if 'produtos' in kwargs:
            produtos = kwargs.pop('produtos')

        if 'gpp' in kwargs:
            gpp = kwargs.pop('gpp')

        if 'tipotemperatura' in kwargs:
            tipotemperatura = kwargs.pop('tipotemperatura')

        super(OportunidadeFormUpdate, self).__init__(*args, **kwargs)
        self.fields['valor'].widget = forms.TextInput()
        self.fields['valor'].widget.attrs['behaveas'] = 'float'

        if liderados:
            self.fields['responsavel'].queryset = liderados

        if lider:
            self.fields['lider'].queryset = lider

        if user:
            if not user.has_perm('oportunidade.change_owner_opportunity'):
                self.fields['lider'].widget.attrs['disabled'] = True
                self.fields['responsavel'].widget.attrs['disabled'] = True

            if user.has_perm('oportunidade.can_change_mw_bc'):
                if 'mw' not in fieldOrder:
                    fieldOrder.append('mw')

                if 'bc' not in fieldOrder:
                    fieldOrder.append('bc')
            else:
                if self.instance.mw:
                    self.fields['dtFechamento'].widget.attrs['disabled'] = True
                    self.fields['valor'].widget.attrs['disabled'] = True

            if tipotemperatura:
                if not user.has_perm('oportunidade.can_set_close'):
                    self.fields['tipotemperatura'].queryset = tipotemperatura.exclude(tipo='G')


        self.fields.keyOrder = fieldOrder

        if arquitetos:
            self.fields['arquitetos'].queryset = arquitetos

        if produtos:
            self.fields['produto'].queryset = produtos

        if gpp:
            self.fields['gpp'].queryset = gpp

        self.fields['criador'].widget = forms.HiddenInput()
        self.fields['filial'].widget.attrs['disabled'] = True
        self.fields['cliente'].widget.attrs['disabled'] = True
        #self.fields['receita'].widget.attrs['disabled'] = True
        self.fields['temperatura_auto'].widget.attrs['disabled'] = True

        
        
    def get_absolute_url(self):
        return reverse('oportunidade.list_oportunidade', kwargs={'pk': self.pk})