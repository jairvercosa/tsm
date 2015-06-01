# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.shortcuts import redirect

from tsm.core.base.core_base_datatable import CoreBaseDatatableView
from tsm.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel, CoreMixinPassRequestForm
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired
from tsm.cliente.models.segmento import Segmento

class SegmentoList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista
    """
    template_name = 'segmento_list.html'
    
class SegmentoData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para envio de dados
    """
    model = Segmento
    columns = ['id','nome', 'buttons', ]
    order_columns = ['id','nome', ]
    max_display_length = 500
    url_base_form = '/cliente/segmentos/'
    
    def filter_queryset(self, qs):
        """
        Filtros da query baseado no datatable
        """
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            search_parts = sSearch.split('+')
            qs_params = None
            for part in search_parts:
                q = Q(nome__contains=part)
                qs_params = qs_params | q if qs_params else q

            qs = qs.filter(qs_params)

        return qs

class SegmentoCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm):
    """
    Formulário de criação
    """
    model = Segmento
    template_name = 'segmento_form.html'
    success_url = '/'

class SegmentoUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm):
    """
    Formulário para edição
    """
    model = Segmento
    template_name = 'segmento_form.html'
    success_url = '/'

class SegmentoDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Segmento
    success_url = '/cliente/segmentos/'