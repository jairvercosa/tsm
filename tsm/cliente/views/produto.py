# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q

from tsm.core.util import get_filiais
from tsm.core.base.core_base_datatable import CoreBaseDatatableView
from tsm.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel, CoreMixinPassRequestForm
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired

from tsm.cliente.models.produto import Produto
from tsm.cliente.forms.produtoform import ProdutoForm

class ProdutoList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista
    """
    template_name = 'produto_list.html'
    
class ProdutoData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista
    """
    model = Produto
    columns = ['nome' , 'fabricante' , 'buttons', ]
    order_columns = ['nome', 'fabricante__nome', ]
    max_display_length = 500
    url_base_form = '/cliente/produtos/'

    def render_column(self, row, column):
        if column == 'fabricante':
            sReturn = row.fabricante.nome
            return sReturn
        else:
            return super(ProdutoData, self).render_column(row, column)
    
    def filter_queryset(self, qs):
        """
        Filtros da query baseado no datatable
        """
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            search_parts = sSearch.split('+')
            qs_params = None
            for part in search_parts:
                q = Q(nome__contains=part)|Q(fabricante__nome__istartswith=part)
                qs_params = qs_params | q if qs_params else q
            
            qs = qs.filter(qs_params)

        qs = qs.filter(Q(filial__id__in=get_filiais(self.request.user.id))|Q(filial__id__isnull=True))
        return qs

class ProdutoCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm, CoreMixinPassRequestForm):
    """
    Formulário de criação
    """
    model = Produto
    template_name = 'produto_form.html'
    success_url = '/'
    form_class= ProdutoForm

class ProdutoUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm, CoreMixinPassRequestForm):
    """
    Formulário de criação
    """
    model = Produto
    template_name = 'produto_form.html'
    success_url = '/'
    form_class= ProdutoForm

class ProdutoDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Produto
    success_url = '/cliente/produtos/'