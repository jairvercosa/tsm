# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.shortcuts import redirect
from django.http import Http404

from tsm.core.util import get_filiais
from tsm.core.base.core_base_datatable import CoreBaseDatatableView
from tsm.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel, CoreMixinPassRequestForm
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired
from tsm.core.models.feriado import Feriado
from tsm.core.forms.feriadoform import FeriadoForm

class FeriadoList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista
    """
    template_name = 'feriado_list.html'
    
class FeriadoData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista em json
    """
    model = Feriado
    columns = ['data', 'nome', 'buttons']
    order_columns = ['data','nome']
    max_display_length = 500
    url_base_form = '/core/feriados/'
    
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

        qs = qs.filter(Q(filial__id__in=get_filiais(self.request.user.id))|Q(filial__id__isnull=True))
        return qs

    def render_column(self, row, column):
        if column == 'data':
            sReturn = row.data.strftime("%d/%m/%Y")
            return sReturn
        else:
            return super(FeriadoData, self).render_column(row, column)

class FeriadoCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm, CoreMixinPassRequestForm):
    """
    Formulário de criação
    """
    model = Feriado
    template_name = 'feriado_form.html'
    success_url = '/'
    form_class = FeriadoForm

class FeriadoUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm, CoreMixinPassRequestForm):
    """
    Formulário de edição
    """
    model = Feriado
    template_name = 'feriado_form.html'
    success_url = '/'
    form_class = FeriadoForm

class FeriadoDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Feriado
    success_url = '/core/feriados/'