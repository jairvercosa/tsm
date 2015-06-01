# -*- coding: ISO-8859-1 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.utils.translation import ugettext, ugettext_lazy as _

from passwords.fields import PasswordField

from tsm.acesso.models.usuario import Usuario
from tsm.acesso.models.usuario import UsuarioReceitas
from tsm.oportunidade.models.receita import Receita

class UsuarioCreateForm(UserCreationForm):
    """
    Formulário de usuários
    """
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    password1 = PasswordField(
        label="Senha",
        help_text='Deve conter no mínimo %s caracteres. Ao menos %s caractere(s) deve ser maiúsculo(s), \
        e ao menos %s caractere(s) deve ser minúsculo(s), use pelo menos %s dígito(s) (0-9) e %s caractere(s) \
        de pontuação na composição da senha (!,:).' % (
                    str(settings.PASSWORD_MIN_LENGTH), 
                    str(settings.PASSWORD_COMPLEXITY["UPPER"]), 
                    str(settings.PASSWORD_COMPLEXITY["LOWER"]),
                    str(settings.PASSWORD_COMPLEXITY["DIGITS"]),
                    str(settings.PASSWORD_COMPLEXITY["PUNCTUATION"]),
                )
        )
    
    class Meta:
        model = Usuario
        exclude = ('last_login','is_staff','date_joined','is_superuser', 'assistentes', 'receitas',)

    def __init__(self, *args, **kwargs):
        super(UsuarioCreateForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'username', 'first_name', 'last_name', 'email', 'telefone', 
            'funcao', 'is_active', 'password1', 'password2','showToTeam', 'segmentos','forca_troca_senha',
        ]

    def get_absolute_url(self):
        return reverse('acesso.list_usuario', kwargs={'pk': self.pk})

class UsuarioUpdateForm(UserChangeForm):
    """
    Formulário de usuários
    """
    username = forms.CharField(required=False)
    #password = forms.CharField(widget=forms.PasswordInput, required=False)
    password = PasswordField(
        required=False,
        help_text='Deve conter no mínimo %s caracteres. Ao menos %s caractere(s) deve ser maiúsculo(s), \
        e ao menos %s caractere(s) deve ser minúsculo(s), use pelo menos %s dígito(s) (0-9) e %s caractere(s) \
        de pontuação na composição da senha (!,:).' % (
                    str(settings.PASSWORD_MIN_LENGTH), 
                    str(settings.PASSWORD_COMPLEXITY["UPPER"]), 
                    str(settings.PASSWORD_COMPLEXITY["LOWER"]),
                    str(settings.PASSWORD_COMPLEXITY["DIGITS"]),
                    str(settings.PASSWORD_COMPLEXITY["PUNCTUATION"]),
                )
        )
    m2mSave  = False
    
    class Meta:
        model = Usuario
        exclude = ('last_login','is_staff','date_joined','is_superuser',)

    def __init__(self, *args, **kwargs):
        super(UsuarioUpdateForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'username', 'first_name', 'last_name', 'password', 'email', 
            'telefone', 'funcao', 'assistentes', 'receitas', 'segmentos', 'is_active',
            'filiais', 'groups', 'user_permissions','showToTeam','forca_troca_senha',
        ]

    def clean_password(self):
        """
        Permite alteração da senha no formulário de usuários
        """
        if len(self.cleaned_data.get('password')):
            return make_password(self.cleaned_data.get('password'))
        else:
            return self.initial["password"]

    def save(self, commit=True):
        instance = super(UsuarioUpdateForm,self).save(commit=False)
        old_save_m2m = self.save_m2m #guarda antiga função para campos manytomany

        def save_m2m():
            if not self.m2mSave:
                #old_save_m2m()
                instance.user_permissions.clear()
                instance.groups.clear()
                instance.filiais.clear()
                instance.assistentes.clear()
                instance.segmentos.clear()

                usuarioReceitaDel = UsuarioReceitas.objects.filter(usuario=instance).delete()

                for assistente in self.cleaned_data['assistentes']:
                    instance.assistentes.add(assistente)

                for receitaId in self.cleaned_data['receitas']:
                    receita = Receita.objects.get(id=receitaId)
                    usuarioReceita = UsuarioReceitas(usuario=instance, receita=receita)
                    usuarioReceita.save()

                for segmento in self.cleaned_data['segmentos']:
                    instance.segmentos.add(segmento)

                for permission in self.cleaned_data['user_permissions']:
                    instance.user_permissions.add(permission)

                for group in self.cleaned_data['groups']:
                    instance.groups.add(group)

                for filial in self.cleaned_data['filiais']:
                    instance.filiais.add(filial)
                #self.m2mSave = True
        self.save_m2m = save_m2m

        if commit:
            instance.save()
            self.save_m2m()

        return instance

class UsuarioTrocaSenha(PasswordChangeForm):

    """
    Troca de senha de usuários
    """
    new_password1 = PasswordField(
        label=_("New password"), 
        help_text='Deve conter no mínimo %s caracteres. Ao menos %s caractere(s) deve ser maiúsculo(s), \
        e ao menos %s caractere(s) deve ser minúsculo(s), use pelo menos %s dígito(s) (0-9) e %s caractere(s) \
        de pontuação na composição da senha (!,:).' % (
                    str(settings.PASSWORD_MIN_LENGTH), 
                    str(settings.PASSWORD_COMPLEXITY["UPPER"]), 
                    str(settings.PASSWORD_COMPLEXITY["LOWER"]),
                    str(settings.PASSWORD_COMPLEXITY["DIGITS"]),
                    str(settings.PASSWORD_COMPLEXITY["PUNCTUATION"]),
                )
        )
    new_password2 = PasswordField(label=_("New password confirmation"))
