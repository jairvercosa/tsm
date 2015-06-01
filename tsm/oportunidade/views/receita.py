# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.shortcuts import redirect

from tsm.core.base.core_base_datatable import CoreBaseDatatableView
from tsm.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired
from tsm.oportunidade.models.receita import Receita

class ReceitaList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista de receitas
    """
    template_name = 'receita_list.html'
    
class ReceitaData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista de receitas
    """
    model = Receita
    columns = ['id','nome','buttons']
    order_columns = ['id','nome']
    max_display_length = 500
    url_base_form = '/oportunidade/receita/'
    
    def filter_queryset(self, qs):
        """
        Filtros da query baseado no datatable
        """
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            search_parts = sSearch.split('+')
            qs_params = None
            for part in search_parts:
                q = Q(nome__istartswith=part)
                qs_params = qs_params | q if qs_params else q

            qs = qs.filter(qs_params)
        return qs

class ReceitaCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm):
    """
    Formulário de criação de receitas
    """
    model = Receita
    template_name = 'receita_form.html'
    success_url = '/'

class ReceitaUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm):
    """
    Formulário de criação de receitas
    """
    model = Receita
    template_name = 'receita_form.html'
    success_url = '/'

class ReceitaDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Receita
    success_url = '/oportunidade/receitas/'