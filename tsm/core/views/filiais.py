# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.shortcuts import redirect

from tsm.core.base.core_base_datatable import CoreBaseDatatableView
from tsm.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired
from tsm.core.models.filial import Filial

class FiliaisList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista de filiais
    """
    template_name = 'filial_list.html'
    
class FiliaisData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista de filiais
    """
    model = Filial
    columns = ['id', 'nome', 'buttons']
    order_columns = ['id','nome']
    max_display_length = 500
    url_base_form = '/core/filiais/'
    
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

class FiliaisCreateForm(CreateView,CoreMixinForm):
    """
    Formulário de criação de filiais
    """
    model = Filial
    template_name = 'filial_form.html'
    success_url = '/'

class FiliaisUpdateForm(UpdateView,CoreMixinForm):
    """
    Formulário de criação de filiais
    """
    model = Filial
    template_name = 'filial_form.html'
    success_url = '/'

class FiliaisDelete(CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Filial
    success_url = '/core/filiais/'