# -*- coding: ISO-8859-1 -*-
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from tsm.core.base.core_base_datatable import CoreBaseDatatableView
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired
from tsm.core.mixins.core_mixin_json import JSONResponseMixin
from tsm.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel
from tsm.core.mixins.core_mixin_json import JSONResponseMixin
from tsm.core.util import getParamByName, get_filiais, format_number
from tsm.core import constants

from tsm.acesso.models.usuario import Usuario
from tsm.equipe.models.membro import Membro
from tsm.equipe.models.membrometa import MembroMeta

from tsm.oportunidade.models.oportunidade import Oportunidade
from tsm.oportunidade.models.resposta import Resposta

class VisaoGerencial(CoreMixinLoginRequired, TemplateView):
    """
    Visão gerencial da oportunidade
    """
    template_name = 'visaogerencial_list.html'    

class VisaoGerencialData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    Json da lista
    """
    model = Oportunidade
    columns = [
        'cliente',
        'receita',
        'situacao', 
        'valor', 
        'ponderado', 
        'temperatura_auto', 
        'tipotemperatura', 
        'responsavel', 
        'lider',
        'dtFechamento',
        'respostas',
        'id',
    ]
    order_columns = [
        'cliente',
        'receita',
        'situacao', 
        'valor', 
        'ponderado', 
        'temperatura_auto', 
        'tipotemperatura', 
        'responsavel', 
        'lider',
        'dtFechamento',
    ]
    max_display_length = 500
    url_base_form = '/oportunidade/visaogerencial/'

    def render_column(self, row, column):
        if column == 'cliente':
            sReturn = row.cliente.nome
            return sReturn
        elif column == 'receita':
            sReturn = row.receita.nome
            return sReturn
        elif column == 'situacao':
            sReturn = row.situacao.nome
            return sReturn
        elif column == 'tipotemperatura':
            sReturn = row.tipotemperatura.nome
            return sReturn
        elif column == 'responsavel':
            sReturn = row.responsavel.first_name + ' ' + row.responsavel.last_name
            return sReturn
        elif column == 'lider':
            sReturn = row.lider.first_name
            return sReturn
        elif column == 'valor':
            sReturn = format_number(row.valor)
            return sReturn
        elif column == 'ponderado':
            sReturn = format_number(row.ponderado)
            return sReturn
        elif column == 'respostas':
            dictReturn = []
            respostas = Resposta.objects.filter(oportunidade__id=row.id).order_by('questao__ordem')
            for resposta in respostas:
                dictReturn.append({
                    "pergunta": resposta.questao.pergunta,
                    "resposta": "Sim" if resposta.resposta else "Não",
                })
            return dictReturn 
        elif column == 'dtFechamento':
            sReturn = row.dtFechamento.strftime("%d/%m/%Y")
            return sReturn
        elif column == 'buttons' and self.url_base_form and self.use_buttons:
            sReturn = '<div class="action-buttons">'
            sReturn +='     <a href="/oportunidade/editar/'+str(row.id)+'/" title="Editar" class="btnEdit"><i class="icon-lapis icon-miniatura"></i></a>'
            sReturn +='</div>'
            return sReturn
        else:
            return super(VisaoGerencialData, self).render_column(row, column)

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
                q = Q(cliente__nome__istartswith=part)| \
                    Q(receita__nome__istartswith=part)| \
                    Q(situacao__nome__istartswith=part)| \
                    Q(temperatura_auto__istartswith=part)| \
                    Q(tipotemperatura__nome__istartswith=part)| \
                    Q(responsavel__first_name__istartswith=part)|Q(responsavel__last_name__istartswith=part)| \
                    Q(lider__first_name__istartswith=part)|Q(lider__last_name__istartswith=part)

                qs_params = qs_params | q if qs_params else q
            
            qs = qs.filter(qs_params)

        if qs_base_filter:
            qs = qs.filter(qs_base_filter)

        return qs

class VisaoGerencialIndicador(CoreMixinLoginRequired, JSONResponseMixin, TemplateView):
    """
    Retorna os indicadores relativos a cada oportunidade
    """

    def get(self, request, *args, **kwargs):
        oportunidade = get_object_or_404(Oportunidade,id=self.kwargs.get('pk', None)) 

        #calcula percentual em relacao a todas as oportunidades ainda não fechadas
        valOportunidade = 0
        oportunidades = Oportunidade.objects.filter(tipotemperatura__tipo__isnull=True) \
                                            .aggregate(Sum('valor'))

        if oportunidades:
            valOportunidade = (oportunidade.valor * 100)/oportunidades['valor__sum']

        if valOportunidade == 100:
            valOportunidade = valOportunidade

        #percentual do responsavel em relacao a sua meta
        valResponsavel = 0
        membroMeta = MembroMeta.objects.filter(
                                    membro__usuario__id=oportunidade.responsavel.id, 
                                    is_Visible=True,
                                    mesVigencia=oportunidade.dtFechamento.strftime("%m"),
                                    anoVigencia=oportunidade.dtFechamento.strftime("%Y"),
                                    tipometa__id=getParamByName(constants.PAR_TPMETA, request.user.id)
                     )

        if membroMeta:
            valResponsavel = (oportunidade.valor * 100)/ membroMeta[0].valor
            if valResponsavel > 100:
                valResponsavel = 100
        
        #percentual do lider em relacao a sua meta
        valLider = 0
        membroMeta = MembroMeta.objects.filter(
                                    membro__usuario__id=oportunidade.lider.id, 
                                    is_Visible=True,
                                    mesVigencia=oportunidade.dtFechamento.strftime("%m"),
                                    anoVigencia=oportunidade.dtFechamento.strftime("%Y"),
                                    tipometa__id=getParamByName(constants.PAR_TPMETA, request.user.id)
                     )
    
        if membroMeta:
            valLider = (oportunidade.valor * 100)/ membroMeta[0].valor
            if valLider > 100:
                valLider = 100

        
        data = {
            "result" : "ok",
            "data" : {
                "oportunidade": oportunidade.id,
                "values":{
                    "oportunidade": round(valOportunidade,2),
                    "responsavel": round(valResponsavel,2),
                    "lider" : round(valLider,2)
                }
            }
        }
        context = data
        
        return self.render_to_response(context)

class VisaoGerencialIndicadorTop(CoreMixinLoginRequired, JSONResponseMixin, TemplateView):
    """
    Retorna os indicadores do topo da tela
    """

    def get(self, request, *args, **kwargs):
        from datetime import date
        from tsm.oportunidade.models.situacao import Situacao
        from tsm.oportunidade.models.tipotemperatura import TipoTemperatura

        if not self.request.user.has_perm('oportunidade.list_all_opportunities'):
            membros = Membro.objects.filter(usuario__id=request.user.id)
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
                                      .filter(id=request.user.id) \
                                      .values_list('filiais__id', flat=True)
            )

        oportunidades = Oportunidade.objects.filter(qs_base_filter)
        oportunidades.exclude(dtFechamento__lt=date(date.today().year, date.today().month, 1)) \
                     .exclude(tipotemperatura__tipo='P')

        #FCST Gross
        temperaturas = [
            [1,6], #Adiada + Alta
            [2], #Media
            [3], #Fechada 
        ]
        totalGross = float(0)
        gross = []
        for item in temperaturas:
            temps = TipoTemperatura.objects.filter(id__in=item)
            strTitle = ''
            for temp in temps:
                if strTitle:
                    strTitle = strTitle + ' + '
                strTitle = strTitle + temp.nome

            gross.append({
                'id': item,
                'title': strTitle,
                'value': 0,
            })

        #lideres
        lideres = []
        for oportunidade in oportunidades:
            if not oportunidade.lider.id in lideres:
                lideres.append(oportunidade.lider.id);

        #FCST Ponderado
        totalPonderado = float(0)
        ponderado = []
        for item in lideres:
            ponderado.append({
                'id': item,
                'name': '',
                'value':0,
            })

        #FATOR Situacao (P/U)
        totalSituacao = 0
        situacoes = Situacao.objects.all()
        fatorSit = []
        for item in lideres:
            fatorSit.append({
                'id': item,
                'name': '',
                'situacoes':[],
            })

            for situacao in situacoes:
                fatorSit[len(fatorSit)-1]['situacoes'].append({
                    'id': situacao.id,
                    'name': situacao.nome,
                    'perc': situacao.perc,
                    'value': 0,
                })

        #FATOR Calculo (66)
        totalFator = float(0)
        fatorCal = []
        for item in lideres:
            fatorCal.append({
                'id': item,
                'name': '',
                'value': 0,
            })

        #Realiza calculo
        for oportunidade in oportunidades:
            #atualiza dados do Gross
            totalGross += oportunidade.valor
            i = 0
            for item in gross:
                if oportunidade.tipotemperatura.id in item['id']:
                    gross[i]['value'] += oportunidade.valor
                i += 1

            #atualiza dados do ponderado
            totalPonderado += oportunidade.ponderado
            i = 0
            for item in ponderado:
                if oportunidade.lider.id == item['id']:
                    ponderado[i]['value'] += oportunidade.ponderado
                    ponderado[i]['name'] = oportunidade.lider.first_name
                i += 1

            #atualiza dados do fator situacao
            totalSituacao += round((oportunidade.valor * oportunidade.situacao.perc)/100,2)
            i = 0
            for item in fatorSit:
                if oportunidade.lider.id == item['id']:
                    fatorSit[i]['name'] = oportunidade.lider.first_name

                    j = 0
                    for situacao in item['situacoes']:
                        if situacao['id'] == oportunidade.situacao.id:
                            fatorSit[i]['situacoes'][j]['value'] = round((oportunidade.valor * oportunidade.situacao.perc)/100,2)
                        j += 1
                i += 1

            #atualiza dados do cálculo 66
            fator = float(getParamByName(constants.PAR_POND66, request.user.id))
            totalFator += round(oportunidade.ponderado * fator,2)
            i=0
            for item in fatorCal:
                if oportunidade.lider.id == item['id']:
                    fatorCal[i]['value'] += round(oportunidade.ponderado * fator,2)
                    fatorCal[i]['name'] = oportunidade.lider.first_name
                i += 1

        data = {
            "result" : "ok",
            "data" : {
                "gross": {
                    "total" : totalGross,
                    "items" : gross,
                },
                "ponderado":{
                    "total": totalPonderado,
                    "items": ponderado,
                },
                "situacao":{
                    "total": totalSituacao,
                    "items": fatorSit,
                },
                "fator":{
                    "perc": fator,
                    "total": totalFator,
                    "items": fatorCal,
                },
            },
        }
        context = data
        
        return self.render_to_response(context)