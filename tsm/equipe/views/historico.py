# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.db.models import Q

from tsm.core.base.core_base_datatable import CoreBaseDatatableView
from tsm.core.mixins.core_mixin_form import CoreMixinForm
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired
from tsm.core.mixins.core_mixin_base import CoreMixinDispatch
from tsm.core.util import format_number

from tsm.equipe.models.membrohistorico import MembroHistorico
from tsm.equipe.models.membrometahistorico import MembroMetaHistorico
from tsm.equipe.forms.membrohistoricoform import MembroHistoricoForm
from tsm.equipe.forms.membrometahistoricoform import MembroMetaHistoricoForm

class MembroHistoricoList(CoreMixinLoginRequired, TemplateView, CoreMixinDispatch):
    """
    View para renderização da lista
    """
    template_name = 'membrohistorico_list.html'
    
class MembroHistoricoData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    Json da lista
    """
    model = MembroHistorico
    columns = [
        'nome_usuario_add',
        'nome_membro',
        'nome_lider', 
        'criado', 
        'buttons',
    ]
    order_columns = [
        'nome_usuario_add',
        'nome_membro',
        'nome_lider', 
        'criado', 
    ]
    max_display_length = 500
    url_base_form = '/equipe/membro/historico/'

    def render_column(self, row, column):
        if column == 'criado':
            sReturn = row.criado.strftime("%d/%m/%Y")
            return sReturn
        elif column == 'buttons' and self.url_base_form and self.use_buttons:
            sReturn = '<div class="action-buttons">'
            sReturn +='     <a href="/equipe/membro/historico/'+str(row.id)+'/" title="Visualizar"><i class="icon-search"></i></a>'
            sReturn +='</div>'
            return sReturn
        else:
            return super(MembroHistoricoData, self).render_column(row, column)

    def filter_queryset(self, qs):
        """
        Filtros da query baseado no datatable
        """
        sSearch = self.request.GET.get('sSearch', None)
        qs_params = None
        if sSearch:
            search_parts = sSearch.split('+')
            for part in search_parts:
                q = Q(nome_membro__contains=part)

                qs_params = qs_params | q if qs_params else q
            
            qs = qs.filter(qs_params)

        return qs

class MembroHistoricoVisao(CoreMixinLoginRequired, UpdateView):
    model = MembroHistorico
    template_name = 'membrohistorico_form.html'
    success_url = '/'
    form_class = MembroHistoricoForm

class MembroMetaHistoricoList(CoreMixinLoginRequired, TemplateView, CoreMixinDispatch):
    """
    View para renderização da lista
    """
    template_name = 'membrometahistorico_list.html'
    
class MembroMetaHistoricoData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    Json da lista
    """
    model = MembroMetaHistorico
    columns = [
        'nome_usuario_add',
        'nome_membro',
        'nome_lider',
        'nome_tipometa',
        'valor',
        'criado', 
        'buttons',
    ]
    order_columns = [
        'nome_usuario_add',
        'nome_membro',
        'nome_lider', 
        'nome_tipometa',
        'valor',
        'criado', 
    ]
    max_display_length = 500
    url_base_form = '/equipe/membro/meta/historico/'

    def render_column(self, row, column):
        if column == 'criado':
            sReturn = row.criado.strftime("%d/%m/%Y")
            return sReturn
        elif column == 'valor':
            sReturn = format_number(row.valor)
            return sReturn
        elif column == 'buttons' and self.url_base_form and self.use_buttons:
            sReturn = '<div class="action-buttons">'
            sReturn +='     <a href="/equipe/membro/meta/historico/'+str(row.id)+'/" title="Visualizar"><i class="icon-search"></i></a>'
            sReturn +='</div>'
            return sReturn
        else:
            return super(MembroMetaHistoricoData, self).render_column(row, column)

    def filter_queryset(self, qs):
        """
        Filtros da query baseado no datatable
        """
        sSearch = self.request.GET.get('sSearch', None)
        qs_params = None
        if sSearch:
            search_parts = sSearch.split('+')
            for part in search_parts:
                q = Q(nome_membro__contains=part)| \
                    Q(nome_tipometa__contains=part)

                qs_params = qs_params | q if qs_params else q
            
            qs = qs.filter(qs_params)

        return qs

class MembroMetaHistoricoVisao(CoreMixinLoginRequired, UpdateView):
    model = MembroMetaHistorico
    template_name = 'membrometahistorico_form.html'
    success_url = '/'
    form_class = MembroMetaHistoricoForm