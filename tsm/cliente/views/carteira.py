# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.shortcuts import redirect

from tsm.core.base.core_base_datatable import CoreBaseDatatableView
from tsm.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel, CoreMixinPassRequestForm
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired
from tsm.cliente.models.carteira import Carteira
from tsm.cliente.forms.carteiraform import CarteiraForm

class CarteiraList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista de carteiras
    """
    template_name = 'carteira_list.html'
    
class CarteiraData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista de carteiras
    """
    model = Carteira
    columns = ['id','nome','buttons']
    order_columns = ['id','nome']
    max_display_length = 500
    url_base_form = '/cliente/carteiras/'
    
    def filter_queryset(self, qs):
        from tsm.acesso.models.usuario import Usuario
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

        filiais = Usuario.objects.get(id=self.request.user.id).filiais.all()
        qs = qs.filter(Q(filial__id__in=filiais)|Q(filial__isnull=True))
        return qs

class CarteiraCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm, CoreMixinPassRequestForm):
    """
    Formulário de criação de carteiras
    """
    model = Carteira
    template_name = 'carteira_form.html'
    success_url = '/'
    form_class = CarteiraForm

class CarteiraUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm, CoreMixinPassRequestForm):
    """
    Formulário de criação de carteiras
    """
    model = Carteira
    template_name = 'carteira_form.html'
    success_url = '/'
    form_class = CarteiraForm

class CarteiraDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Carteira
    success_url = '/cliente/carteiras/'