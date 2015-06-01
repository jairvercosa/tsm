# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q

from tsm.core.base.core_base_datatable import CoreBaseDatatableView
from tsm.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel, CoreMixinPassRequestForm
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired
from tsm.cliente.models.contato import Contato
from tsm.cliente.forms.contatoform import ContatoForm

class ContatoList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista
    """
    template_name = 'contato_list.html'
    
class ContatoData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista
    """
    model = Contato
    columns = ['id','nome','cliente','buttons']
    order_columns = ['id','nome','cliente__nome']
    max_display_length = 500
    url_base_form = '/cliente/contato/'

    def render_column(self, row, column):
        if column == 'cliente':
            sReturn = row.cliente.nome
            return sReturn
        else:
            return super(ContatoData, self).render_column(row, column)
    
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
                q = Q(nome__contains=part)|Q(cliente__istartswith=part)
                qs_params = qs_params | q if qs_params else q

            qs = qs.filter(qs_params)

        filiais = Usuario.objects.get(id=self.request.user.id).filiais.all()
        qs = qs.filter(cliente__filial__id__in=filiais)

        return qs

class ContatoCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm, CoreMixinPassRequestForm):
    """
    Formulário de criação
    """
    model = Contato
    template_name = 'contato_form.html'
    success_url = '/'
    form_class=ContatoForm

class ContatoUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm, CoreMixinPassRequestForm):
    """
    Formulário de criação
    """
    model = Contato
    template_name = 'contato_form.html'
    success_url = '/'
    form_class=ContatoForm

class ContatoDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Contato
    success_url = '/cliente/contatos/'