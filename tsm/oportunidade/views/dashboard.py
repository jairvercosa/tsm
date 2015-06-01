# -*- coding: ISO-8859-1 -*-
import json
from calendar import monthrange
from datetime import date, datetime
from django.views.generic.base import TemplateView

from tsm.core import constants, util
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired
from tsm.core.mixins.core_mixin_base import CoreMixinDispatch
from tsm.core.mixins.core_mixin_json import JSONResponseMixin

from tsm.acesso.models.usuario import Usuario
from tsm.equipe.models.membro import Membro
from tsm.equipe.models.membrometa import MembroMeta
from tsm.equipe.models.tipometa import TipoMeta

from tsm.oportunidade.widgets import Widgets
from tsm.oportunidade.models.receita import Receita

class DashboardIndex(CoreMixinLoginRequired, TemplateView, CoreMixinDispatch):
    """
    Dashboard
    """
    template_name = 'dashboard_index.html'

    def getListView(self, *args, **kwargs):
        """
        Retorna a lista dos tipos de visão permitidos no Dashboard (Filial, GAR, EAR)
        e os tipos de meta
        """
        request = kwargs['request']
        listOpt = []
        listOptMeta = []
        resp_filial = [] #array com os responsaveis por filiais

        if request.user.has_perm('equipe.list_all_members'):
            # pega as filiais
            filiaisList = Usuario.objects.get(id=request.user.id, is_active=True).filiais.all()
            for item in filiaisList:
                nome = item.nome
                if item.responsavel:
                    nome = nome + ' - ' + item.responsavel.first_name + ' ' + item.responsavel.last_name
                    resp_filial.append(item.responsavel.id)

                listOpt.append({
                    "id" : item.pk,
                    "nome" : nome,
                    "tipo" : 'filial',
                })

            if filiaisList:
                # pega os líderes (GAR) e responsáveis (EAR)
                membrosList = Membro.objects \
                                    .filter(usuario__filiais__in=filiaisList) \
                                    .exclude(usuario__id__in=resp_filial) \
                                    .order_by('usuario__first_name', 'usuario__last_name') \
                                    .distinct()

                for item in membrosList:
                    listOpt.append({
                        "id" : item.usuario.id,
                        "nome" : item.usuario.first_name + ' ' + item.usuario.last_name,
                        "tipo" : 'usuario',
                    })

                # pega os tipos de meta
                tiposList = TipoMeta.objects.filter(filial__id__in=filiaisList)
                for item in tiposList:
                    listOptMeta.append({
                        "id" : item.pk,
                        "nome" : item.nome,
                    })
        else:
            widget = Widgets(request.user, {"id":request.user.id,"tipo":"usuario"}, "")
            membros = widget.getMembros()

            membrosList = Membro.objects.filter(usuario__id__in=membros).order_by('usuario__first_name', 'usuario__last_name')
            for item in membrosList:
                listOpt.append({
                    "id" : item.usuario.id,
                    "nome" : item.usuario.first_name + ' ' + item.usuario.last_name,
                    "tipo" : 'usuario',
                })

            #verifica se usuário é um membro de equipe
            membroEquipe = Membro.objects.filter(usuario__id=request.user.id)
            if membroEquipe:
                #verifica se membro tem meta visível pra ele
                membroMeta = MembroMeta.objects \
                                        .filter(membro__id=membroEquipe[0].id) \
                                        .filter(is_Visible=True) \
                                        .filter(mesVigencia=date.today().strftime('%m')) \
                                        .filter(anoVigencia=date.today().year)

                filterMeta = 0
                if membroMeta:
                    filterMeta = membroMeta[0].tipometa.id
                else:
                    paramMeta = util.getParamByName(constants.PAR_TPMETA,request.user.id)
                    if paramMeta:
                        filterMeta = int(paramMeta)

                # pega os tipos de meta
                tiposList = TipoMeta.objects.filter(id=filterMeta)
                for item in tiposList:
                    listOptMeta.append({
                        "id" : item.pk,
                        "nome" : item.nome,
                    })

        return listOpt, listOptMeta


    def get(self, request, *args, **kwargs):
        receitas = Usuario.objects.get(id=request.user.id).receitas.all()
        listOpt, listOptMeta = self.getListView(request=request)

        hoje = date.today()
        diaIni = datetime.strptime(str(hoje.year)+'-'+hoje.strftime('%m')+'-01','%Y-%m-%d')
        diaFim = datetime.strptime(str(hoje.year)+'-'+hoje.strftime('%m')+'-'+str(monthrange(hoje.year,hoje.month)[1]),'%Y-%m-%d')

        return self.render_to_response(self.get_context_data(
            receitas = receitas,
            listOpt = listOpt,
            listOptMeta = listOptMeta,
            diaIni=diaIni.strftime('%d/%m/%Y'),
            diaFim=diaFim.strftime('%d/%m/%Y'),
        ))

class DashboardGetData(CoreMixinLoginRequired, JSONResponseMixin, TemplateView):
    """
    Retorna os indicadores
    """

    def get(self, request, *args, **kwargs):
        receitas = []
        for receita in request.GET.getlist('receitas[]'):
            receitas.append(int(receita))

        instanceWg = Widgets(
            request.user,
            {
                'id': int(request.GET['visao']),
                'tipo':request.GET['tipovisao']
            },
            int(request.GET['tipometa']),
            request.GET['diaini'],
            request.GET['diafim'],
            receitas
        )
        instanceWg.setup()

        data = {
            "ponderado" : instanceWg.prospeccaoData(),
            "evolucao"  : instanceWg.heatData(),
            "gross"     : instanceWg.heatGross(),
            "linearidade": instanceWg.linearidadeData(),
            "compromisso": instanceWg.entregaData(),
        }

        return self.render_to_response(data)
