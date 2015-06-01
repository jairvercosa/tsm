# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.shortcuts import redirect

from tsm.core.base.core_base_datatable import CoreBaseDatatableView
from tsm.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired
from tsm.oportunidade.models.tipotemperatura import TipoTemperatura

class TpTemperaturaList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista de tipotemperatura
    """
    template_name = 'tipo_temperatura_list.html'
    
class TpTemperaturaData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista de tipotemperatura
    """
    model = TipoTemperatura
    columns = ['id','nome','tipo','buttons']
    order_columns = ['id','nome','tipo']
    max_display_length = 500
    url_base_form = '/oportunidade/tipotemperatura/'
    
    def render_column(self, row, column):
        """
        Renderização das colunas
        """

        if column == 'tipo':
            if row.tipo == 'P':
                return 'Perda'
            elif row.tipo == 'G':
                return 'Ganho'
            else:
                return ''
        else:
            return super(TpTemperaturaData, self).render_column(row, column)

    def filter_queryset(self, qs):
        """
        Filtros da query baseado no datatable
        """
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            search_parts = sSearch.split('+')
            qs_params = None
            for part in search_parts:
                if part.lower() == 'perda':
                    q = Q(tipo='P')
                elif part.lower() == 'ganho':
                    q = Q(tipo='G')
                else:
                    q = Q(nome__istartswith=part)

                qs_params = qs_params | q if qs_params else q

            qs = qs.filter(qs_params)
        return qs

class TpTemperaturaCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm):
    """
    Formulário de criação de tipotemperatura
    """
    model = TipoTemperatura
    template_name = 'tipo_temperatura_form.html'
    success_url = '/'

class TpTemperaturaUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm):
    """
    Formulário de criação de tipotemperatura
    """
    model = TipoTemperatura
    template_name = 'tipo_temperatura_form.html'
    success_url = '/'

class TpTemperaturaDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = TipoTemperatura
    success_url = '/oportunidade/tipotemperatura/'