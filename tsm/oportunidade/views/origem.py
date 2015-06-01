# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q

from tsm.core.base.core_base_datatable import CoreBaseDatatableView
from tsm.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired
from tsm.oportunidade.models.origem import Origem

class OrigemList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista
    """
    template_name = 'origem_list.html'
    
class OrigemData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização json da lista
    """
    model = Origem
    columns = ['id','nome','buttons']
    order_columns = ['id','nome']
    max_display_length = 500
    url_base_form = '/oportunidade/origem/'
    
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

class OrigemCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm):
    """
    Formulário de criação
    """
    model = Origem
    template_name = 'origem_form.html'
    success_url = '/'

class OrigemUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm):
    """
    Formulário de edição
    """
    model = Origem
    template_name = 'origem_form.html'
    success_url = '/'

class OrigemDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Origem
    success_url = '/oportunidade/origem/'