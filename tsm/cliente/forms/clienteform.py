# -*- coding: ISO-8859-1 -*-
import re
from datetime import date
from django import forms
from django.db.models import Q
from django_localflavor_br.forms import BRCNPJField, BRStateChoiceField, BRZipCodeField

from tsm.cliente.models.cliente import Cliente
from tsm.acesso.models.usuario import Usuario
from tsm.oportunidade.widgets import Widgets

class ClienteForm(forms.ModelForm):
    """
    Formulário de Inclusão
    """
    error_messages_cnpj={
        'invalid': "CNPJ Inválido",
        'digits_only': "Utilize apenas números ou os caracteres '.', '/' ou '-'.",
        'max_digits': "Este campo requer 14 dígitos",
    }
    cnpj = BRCNPJField(error_messages=error_messages_cnpj)
    cnpj_matriz = BRCNPJField(error_messages=error_messages_cnpj)
    estado = BRStateChoiceField()
    cep = BRZipCodeField(
        error_messages={
            'invalid': 'Use o formato XXXXX-XXX para digitar um CEP.',
        }
    )
    
    class Meta:
        model = Cliente
        
    def get_absolute_url(self):
        return reverse('cliente.list_cliente', kwargs={'pk': self.pk})

    def __init__(self, *args, **kwargs):
        from tsm.core.util import get_filiais

        from tsm.cliente.models.carteira import Carteira
        from tsm.cliente.models.produto import Produto

        request = kwargs.pop('request')
        usuario = Usuario.objects.get(id=request.user.id)
        
        # valida executivo
        if request.user.has_perm('equipe.list_all_members'):
            usuarios = Usuario.objects.filter(filiais__in=usuario.filiais.all()).order_by('first_name','last_name').distinct()
        else:
            widget = Widgets(request.user, {"id":request.user.id,"tipo":"usuario"}, "")
            usuarios = Usuario.objects.filter(id__in=widget.getMembros()).distinct()

        super(ClienteForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if not instance or not instance.pk:
            self.fields['criado'].widget = forms.HiddenInput()

        #self.fields['cnpj'].required = False
        self.fields['cnpj_matriz'].required = False
        self.fields['criado'].required = False
        self.fields['cep'].required = False
        
        self.fields['criado'].widget.attrs['readonly'] = True
        
        self.fields['filial'].queryset = get_filiais(request.user.id)
        self.fields['carteira'].queryset = Carteira.objects.filter(Q(filial__id__in=get_filiais(request.user.id))|Q(filial__isnull=True))
        self.fields['produtos'].queryset = Produto.objects.filter(
                                                Q(filial__id__in=get_filiais(request.user.id))| \
                                                Q(filial__id__isnull=True)
                                           )
        self.fields['executivo'].queryset = usuarios

    def remove_mask(self, text):
        return re.sub("[-/\.]", "", text)

    def clean_criado(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.criado
        else:
            return date.today()

    def clean_cnpj(self):
        return self.remove_mask(self.cleaned_data['cnpj'])

    def clean_cnpj_matriz(self):
        return self.remove_mask(self.cleaned_data['cnpj_matriz'])

    def clean_cep(self):
        return self.remove_mask(self.cleaned_data['cep'])

    def save(self, commit=True):
        instance = super(ClienteForm,self).save(commit=False)

        def save_m2m():
            instance.produtos.clear()

            for produto in self.cleaned_data['produtos']:
                instance.produtos.add(produto)

            self.m2mSave = True
        self.save_m2m = save_m2m

        if commit:
            instance.save()
            self.save_m2m()

        return instance

class ClienteFormMin(forms.ModelForm):
    """
    Formulário de inclusão de clientes mínimo usado para inclusões rápidas
    """
    error_messages_cnpj={
        'invalid': "CNPJ Inválido",
        'digits_only': "Utilize apenas números ou os caracteres '.', '/' ou '-'.",
        'max_digits': "Este campo requer 14 dígitos",
    }
    cnpj = BRCNPJField(error_messages=error_messages_cnpj)
    
    class Meta:
        model = Cliente
        exclude = ('cnpj_matriz', 'endereco', 'bairro', 'cidade', 'estado', 'cep', 'webpage', 'produtos',)
        
    def get_absolute_url(self):
        return reverse('cliente.list_cliente', kwargs={'pk': self.pk})

    def __init__(self, *args, **kwargs):
        from tsm.core.util import get_filiais

        from tsm.cliente.models.carteira import Carteira

        request = kwargs.pop('request')
        usuario = Usuario.objects.get(id=request.user.id)
        
        # valida executivo
        if request.user.has_perm('equipe.list_all_members'):
            usuarios = Usuario.objects.filter(filiais__in=usuario.filiais.all()).order_by('first_name','last_name').distinct()
        else:
            widget = Widgets(request.user, {"id":request.user.id,"tipo":"usuario"}, "")
            usuarios = Usuario.objects.filter(id__in=widget.getMembros()).distinct()

        super(ClienteFormMin, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if not instance or not instance.pk:
            self.fields['criado'].widget = forms.HiddenInput()

        self.fields['criado'].required = False
        #self.fields['cnpj'].required = False
        self.fields['filial'].queryset = get_filiais(request.user.id)
        self.fields['carteira'].queryset = Carteira.objects.filter(Q(filial__id__in=get_filiais(request.user.id))|Q(filial__isnull=True))
        self.fields['executivo'].queryset = usuarios
        
    def remove_mask(self, text):
        return re.sub("[-/\.]", "", text)

    def clean_criado(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.criado
        else:
            return date.today()

    def clean_cnpj(self):
        return self.remove_mask(self.cleaned_data['cnpj'])