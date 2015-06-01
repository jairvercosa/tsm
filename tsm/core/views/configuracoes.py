# -*- coding: ISO-8859-1 -*-
from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin

from tsm.core.mixins.core_mixin_base import CoreMixinDispatch

class Configuracoes(LoginRequiredMixin, TemplateView, CoreMixinDispatch):
    template_name = "configuracoes.html"
    login_url = "/acesso/auth/"

class Cadastros(LoginRequiredMixin, TemplateView):
    template_name = "cadastros.html"
    login_url = "/acesso/auth/"

class Historico(LoginRequiredMixin, TemplateView):
    template_name = "historico.html"
    login_url = "/acesso/auth/"