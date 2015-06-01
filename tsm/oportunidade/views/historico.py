# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.db.models import Q

from tsm.core.util import format_number
from tsm.core.base.core_base_datatable import CoreBaseDatatableView
from tsm.core.mixins.core_mixin_form import CoreMixinForm
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired

from tsm.oportunidade.models.oportunidade import Oportunidade
from tsm.oportunidade.models.historico import Historico
from tsm.oportunidade.forms.historicoform import HistoricoForm

from tsm.acesso.models.usuario import Usuario
from tsm.equipe.models.membro import Membro

class HistoricoList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista
    """
    template_name = 'historico_list.html'
    
class HistoricoData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    Json da lista
    """
    model = Historico
    columns = [
        'oportunidade',
        'criado',
        'nome_usuario_add', 
        'nome_situacao', 
        'nome_tipotemperatura', 
        'temperatura_auto',
        'nome_responsavel', 
        'nome_lider', 
        'valor', 
        'ponderado',
        'dtFechamento',
        'buttons',
    ]
    order_columns = [
        'oportunidade',
        'criado',
        'nome_usuario_add', 
        'nome_situacao', 
        'nome_tipotemperatura', 
        'temperatura_auto',
        'nome_responsavel', 
        'nome_lider', 
        'valor', 
        'ponderado',
        'dtFechamento',
    ]
    max_display_length = 500
    url_base_form = '/oportunidade/historico/'

    def render_column(self, row, column):
        if column == 'criado':
            sReturn = row.criado.strftime("%d/%m/%Y")
            return sReturn
        elif column == 'dtFechamento':
            sReturn = row.dtFechamento.strftime("%d/%m/%Y")
            return sReturn
        elif column == 'oportunidade':
            sReturn = row.oportunidade.cliente.nome + ' - ' + row.oportunidade.filial.nome
            return sReturn
        elif column == 'valor':
            sReturn = format_number(row.valor)
            return sReturn
        elif column == 'ponderado':
            sReturn = format_number(row.ponderado)
            return sReturn
        elif column == 'buttons' and self.url_base_form and self.use_buttons:
            sReturn = '<div class="action-buttons">'
            sReturn +='     <a href="/oportunidade/historico/'+str(row.id)+'/" title="Visualizar"><i class="icon-search"></i></a>'
            sReturn +='</div>'
            return sReturn
        else:
            return super(HistoricoData, self).render_column(row, column)

    def filter_queryset(self, qs):
        """
        Filtros da query baseado no datatable
        """
        qs_base_filter = None

        #Verifica pode ver todas oportunidades, senão só exibe as que ele pode ver
        if not self.request.user.has_perm('oportunidade.list_all_opportunities'):
            membros = Membro.objects.filter(usuario__id=self.request.user.id)
            if membros.exists():
                membro = membros[0]
                children = Membro.objects.filter(lider__id=membro.id)
                qs_base_filter = Q(responsavel__id=membro.usuario.id) | Q(lider__id=membro.usuario.id)
                
                if children:
                    while children:
                        for item in children:
                            qs_base_filter = qs_base_filter | Q(lider__id=item.usuario.id)

                        children = Membro.objects.filter(
                            lider__id__in = children.values_list('id', flat=True)
                        )
        else:
            qs_base_filter = Q(
                filial__id__in=Usuario.objects \
                                      .filter(id=self.request.user.id) \
                                      .values_list('filiais__id', flat=True)
            )

        sSearch = self.request.GET.get('sSearch', None)
        qs_params = None
        if sSearch:
            search_parts = sSearch.split('+')
            for part in search_parts:
                q = Q(oportunidade__cliente__nome__istartswith=part)| \
                    Q(nome_situacao__istartswith=part)| \
                    Q(nome_tipotemperatura__istartswith=part)| \
                    Q(temperatura_auto__istartswith=part)| \
                    Q(nome_responsavel__istartswith=part)

                qs_params = qs_params | q if qs_params else q
            
            qs = qs.filter(qs_params)

        if qs_base_filter:
            qs = qs.filter(oportunidade__id__in=Oportunidade.objects.filter(qs_base_filter).values_list('id'))

        return qs

class HistoricoVisao(CoreMixinLoginRequired, UpdateView):
    """
    Formulário de edição de oportunidades
    """
    model = Historico
    template_name = 'historico_form.html'
    success_url = '/'
    form_class = HistoricoForm