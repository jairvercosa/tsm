# -*- coding: ISO-8859-1 -*-
from datetime import date, datetime, timedelta
from django.core.exceptions import PermissionDenied
from django.views.generic.base import TemplateView
from django.db.models import Q

from tsm.core import constants
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired
from tsm.core.mixins.core_mixin_json import JSONResponseMixin
from tsm.core.mixins.core_mixin_base import CoreMixinDispatch
from tsm.core.base.core_base_datatable import CoreBaseDatatableView

from tsm.oportunidade.widgets import Widgets
from tsm.oportunidade.models.rtc import Rtc
from tsm.oportunidade.models.oportunidade import Oportunidade

from tsm.acesso.models.usuario import Usuario

class RtcGerencial(CoreMixinLoginRequired, TemplateView, CoreMixinDispatch):
    """
    View para renderização do relatório
    """
    template_name = 'rtc_gerencial.html'

    def get(self, request, *args, **kwargs):
        #instancia o objeto de widgets por conter o get de membros completo da hierarquia
        if request.user.has_perm('equipe.list_all_members'):
            usuarios = Usuario.objects.all().order_by('first_name','last_name')
        else:
            widget = Widgets(request.user, {"id":request.user.id,"tipo":"usuario"}, "")
            membros = widget.getMembros()

            usuarios = Usuario.objects.filter(id__in=membros).order_by('first_name','last_name')
        
        hoje = date.today()
        weekRange = hoje + timedelta(days=7)
        kwargs.update({"usuarios":usuarios})
        kwargs.update({
            "hoje":hoje.strftime("%d/%m/%Y"),
            "range":weekRange.strftime("%d/%m/%Y"),
        })
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class RtcHeader(CoreMixinLoginRequired, JSONResponseMixin, TemplateView):
    """
    Retorna o cabecalho de acordo com o filtro da tela
    """

    def get(self, request, *args, **kwargs):
        
        if not 'start' in request.GET or not 'end' in request.GET:
            returnData = {
                "result":False,
                "message": "Parametro start/end nao enviado",
                "status": 400,
            }
        else:

            try:
                start = datetime.strptime(request.GET.get('start',None), '%d/%m/%Y').date()
                end   = datetime.strptime(request.GET.get('end'  ,None), '%d/%m/%Y').date()

                header = []
                diff = abs((end - start).days)
                for n in range(0,diff+1):
                    row = start + timedelta(days=n)
                    day = row.day
                    month = constants.CONST_MESES[row.month-1][1][:3]
                    formated = str(day) + "/" + month
                    header.append(formated)

                returnData = {
                    "header":header,
                    "status": 200,
                }
            except Exception, e:
                returnData = {
                    "result":False,
                    "message": "Falha na conversao das datas",
                    "status": 400,
                }

        context = returnData
        return self.render_to_response(context)

class RtcData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista
    """
    model = Oportunidade
    columns = ['id','data','descricao']
    order_columns = ['id','data','descricao']
    max_display_length = 500
    url_base_form = '/oportunidade/lista/'
    start = None
    end = None
    
    def get_initial_queryset(self):
        """
        Filtros da query baseado no datatable
        """
        qs = self.model.objects.all()

        self.start = datetime.strptime(self.request.GET.get('start',None), '%d/%m/%Y').date()
        self.end   = datetime.strptime(self.request.GET.get('end'  ,None), '%d/%m/%Y').date()

        if self.request.user.has_perm('equipe.list_all_members'):
            usuarios = Usuario.objects.all()
        else:
            widget = Widgets(self.request.user, {"id":self.request.user.id,"tipo":"usuario"}, "")
            membros = widget.getMembros()

            usuarios = Usuario.objects.filter(id__in=membros)

        qs = qs.filter(Q(lider__id__in=usuarios)|Q(responsavel__id__in=usuarios))
        qs = qs.filter(dtFechado__isnull=True).exclude(tipotemperatura__tipo='P').order_by('cliente__nome')

        return qs

    def render_column(self, row, column):
        if column == 'data':
            sReturn = row.data.strftime("%d/%m/%Y")
            return sReturn
        else:
            return super(RtcData, self).render_column(row, column)

    def prepare_results(self, qs):
        data = []

        columns = ['oportunidade']

        diff = abs((self.end - self.start).days)
        for n in range(0,diff+1):
            row = self.start + timedelta(days=n)
            day = row.day
            month = constants.CONST_MESES[row.month-1][1][:3]
            formated = str(day) + "/" + month
            columns.append(formated)

        row = []
        for item in qs:
            row = []
            key = item.id
            row.append(item.cliente.nome + ' / ' + item.codcrm)

            for dayRow in columns:
                if dayRow != 'oportunidade':
                    row.append([])

            events = item.oportunidade_rtc_set.filter(data__gte=self.start,data__lte=self.end)

            for event in events:
                day = event.data.day
                month = constants.CONST_MESES[event.data.month-1][1][:3]
                formated = str(day) + "/" + month

                idx = columns.index(formated)
                row[idx].append({
                    "descricao": event.descricao,
                    "id": event.id,
                    "oportunidade": item.id
                })

            data.append(row)

        return data

