# -*- coding: ISO-8859-1 -*-
import ast, json, datetime
from datetime import date

from django.contrib.humanize.templatetags.humanize import intcomma
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q

from tsm.core import constants
from tsm.core.base.core_base_datatable import CoreBaseDatatableView
from tsm.core.util import format_number, getParamByName
from tsm.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired
from tsm.core.mixins.core_mixin_json import JSONResponseMixin

from tsm.oportunidade.models.oportunidade import Oportunidade
from tsm.oportunidade.models.situacao import Situacao
from tsm.oportunidade.models.tipotemperatura import TipoTemperatura
from tsm.oportunidade.models.receita import Receita
from tsm.oportunidade.models.resposta import Resposta
from tsm.oportunidade.models.questao import Questao
from tsm.oportunidade.models.rtc import Rtc
from tsm.oportunidade.forms.oportunidadeform import OportunidadeForm, OportunidadeFormUpdate
from tsm.oportunidade.widgets import Widgets

from tsm.acesso.models.usuario import Usuario
from tsm.equipe.models.membro import Membro
from tsm.cliente.models.carteira import Carteira
from tsm.cliente.models.produto import Produto

class OportunidadeList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista
    """
    template_name = 'oportunidade_list.html'

    def get(self, request, *args, **kwargs):
        situacoes = Situacao.objects.all()
        temperaturas = TipoTemperatura.objects.all()
        optVals = constants.OPT_VALS

        userLogged = Usuario.objects.get(pk=request.user.id)

        receitas = Receita.objects.filter(pk__in=userLogged.receitas.all());

        filiais = userLogged.filiais.all()
        optProdutos = Produto.objects.filter(Q(filial__in=filiais)|Q(filial__isnull=True))

        receitaJson = []
        for item in receitas:
            receitaJson.append({
                "id": item.id,
                "nome": item.nome,
            })

        situacaoJson = []
        for item in situacoes:
            situacaoJson.append({
                "id": item.id,
                "nome": item.nome,
            })

        temperaturaJson = []
        for item in temperaturas:
            if request.user.has_perm('oportunidade.can_set_close') or item.tipo != 'G':
                temperaturaJson.append({
                    "id": item.id,
                    "nome": item.nome,
                    "perc": item.perc,
                })

        produtosJson = []
        for item in optProdutos:
            produtosJson.append({
                "id": item.id,
                "nome": item.nome,
                "fabricante": item.fabricante.nome,
            })

        #Se oriundo do dashboard realiza filtros
        fromDash = request.GET.get('frdash',None)
        dataFilter = None
        if fromDash:
            dataFilter = {}
            visaoPor = request.GET.get('visao',None)
            dia_ini = request.GET.get('dia_ini',None)
            dia_fim = request.GET.get('dia_fim',None)
            receitasFilter = request.GET.get('receitas',None)

            if visaoPor:
                if visaoPor[:6] != 'filial':
                    visaoPor = int(visaoPor[8:])
                    dataFilter.update({'usufilter': visaoPor})

            if dia_ini and dia_fim:
                dataFilter.update({'dtFechamento': dia_ini+':'+dia_fim })
            
            if receitasFilter:
                receita_parts = receitasFilter.split(' ')
                if receita_parts:
                    dataFilter.update({'receitas':receita_parts})

            tipotemp_ret = []
            for item in temperaturas:
                if item.tipo == 'G':
                    tipotemp_ret.append(item.pk)
                    
            dataFilter.update({ 'tipotemperatura': tipotemp_ret })

        kwargs.update({
            #Lista em json
            "receita": json.dumps(receitaJson),
            "situacao": json.dumps(situacaoJson),
            "temperatura": json.dumps(temperaturaJson),
            "produto": json.dumps(produtosJson),

            #Lista comum para uso no template
            "receitas": receitas,
            "situacoes": situacoes,
            "temperaturas": temperaturas,
            "optVals": optVals,
            "optProdutos": optProdutos,
        })

        #prefiltro
        if dataFilter:
            kwargs.update({
                "dataFilter": json.dumps(dataFilter),
            })

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
class OportunidadeData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    Json da lista
    """
    valTotal = 0.00
    pondTotal = 0.00
    canEdit = False
    model = Oportunidade
    columns = [
        'cliente',
        'receita',
        'produto',
        'situacao', 
        'valor', 
        'ponderado', 
        'temperatura_auto', 
        'tipotemperatura', 
        'responsavel', 
        'lider',
        'dtFechamento',
        'rtc',
        'mw',
        'bc',
        'buttons',
        'respostas',
        'id',
    ]
    order_columns = [
        'cliente',
        'receita',
        'produto',
        'situacao', 
        'valor', 
        'ponderado', 
        'temperatura_auto', 
        'tipotemperatura', 
        'responsavel', 
        'lider',
        'dtFechamento',
        'rtc'
    ]
    max_display_length = 500
    url_base_form = '/oportunidade/lista/'

    def render_column(self, row, column):
        if column == 'dtFechamento':
            sReturn = row.dtFechamento.strftime("%d/%m/%Y")
            return sReturn
        elif column == 'cliente':
            sReturn = row.cliente.nome
            return sReturn
        elif column == 'receita':
            sReturn = row.receita.nome
            return sReturn
        elif column == 'produto':
            if row.produto:
                sReturn = row.produto.nome
            else:
                sReturn = 'Não Selecionado'
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
        elif column == 'rtc':
            sReturn = 'Sim' if row.rtc else 'Não'
            return sReturn
        elif column == 'buttons' and self.url_base_form and self.use_buttons:
            sReturn = '<div class="action-buttons">'
            sReturn +='     <a href="'+self.url_base_form+str(row.id)+'/" title="Editar" class="btnEdit"><i class="icon-lapis icon-miniatura"></i></a>'
            
            if self.canEdit:
                sReturn +='     <a href="javascript:;" class="btnEditFast hidden-xs" alt="'+str(row.id)+'" title="Edição Rápida"><i class="icon-align-left"></i></a>'
            
            if self.request.user.has_perm('oportunidade.delete_oportunidade'):
                sReturn +='     <a href="javascript:;" class="btnDel" alt="'+str(row.id)+'" title="Remover"><i class="icon-x"></i></a>'

            sReturn +='</div>'
            return sReturn
        else:
            return super(OportunidadeData, self).render_column(row, column)

    def get_initial_queryset(self):
        """
        Filtros iniciais
        """
        qs_base_filter = None

        userFilter = self.request.GET.get('userfilter',None)

        #Verifica pode ver todas oportunidades, senão só exibe as que ele pode ver
        if not self.request.user.has_perm('oportunidade.list_all_opportunities') or userFilter:
            #Verifica se tem um filtro de usuário, geralmente requisições vindas do dashboard
            if userFilter:
                userFilter = int(userFilter)
            else:
                userFilter = self.request.user.id

            membros = Membro.objects.filter(usuario__id=userFilter)
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

        qs = self.model.objects.filter(qs_base_filter)
        
        #temperaturas fechadas
        tempCloseParam = getParamByName(constants.PAR_TPOPFECHADA,self.request.user.id)
        if(not tempCloseParam):
            tempClose = [0]
        else:
            tempClose = eval('['+tempCloseParam+']')

        if not self.request.user.has_perm('oportunidade.list_all_opportunities') and \
            not self.request.GET.get('frdash',None):
            qs = qs.exclude(tipotemperatura__id__in=tempClose)

        self.canEdit = True if self.request.user.has_perm('oportunidade.change_oportunidade') else False
        return qs

    def filter_queryset(self, qs):
        """
        Filtros da query baseado no datatable
        """
        sSearch = self.request.GET.get('sSearch', None)
        qs_params = None
        if sSearch:
            search_parts = sSearch.split('+')
            for part in search_parts:
                q = Q(cliente__nome__istartswith=part)| \
                    Q(produto__nome__istartswith=part)| \
                    Q(receita__nome__istartswith=part)| \
                    Q(situacao__nome__istartswith=part)| \
                    Q(temperatura_auto__istartswith=part)| \
                    Q(tipotemperatura__nome__istartswith=part)| \
                    Q(responsavel__first_name__istartswith=part)|Q(responsavel__last_name__istartswith=part)| \
                    Q(lider__first_name__istartswith=part)|Q(lider__last_name__istartswith=part)

                qs_params = qs_params | q if qs_params else q
            
            qs = qs.filter(qs_params)
        else:
            #Pesquisa dos campos customizados
            sCliente = self.request.GET.get('cliente', None)
            sReceita = self.request.GET.get('receita', None)
            sSituacao = self.request.GET.get('situacao', None)
            sTemperatura_Auto = self.request.GET.get('temperatura_auto', None)
            sTipoTemperatura = self.request.GET.get('tipotemperatura', None)
            sResponsavel = self.request.GET.get('responsavel', None)
            sLider = self.request.GET.get('lider', None)
            sDtFechamento = self.request.GET.get('dtfechamento', None)
            nValor = self.request.GET.get('valor', None)
            nPonderado = self.request.GET.get('ponderado', None)
            nProduto = self.request.GET.get('produto', None)
            rtc = self.request.GET.get('rtc', None)
            mw = self.request.GET.get('mw', None)
            bc = self.request.GET.get('bc', None)

            if sCliente:
                qs_params = None
                cliente_parts = sCliente.split(' ')
                for part in cliente_parts:
                    q = Q(cliente__nome__icontains=part)

                    qs_params = qs_params | q if qs_params else q
                
                qs = qs.filter(qs_params)

            if sReceita:
                qs_params = None
                receita_parts = sReceita.split('+')
                for part in receita_parts:
                    q = Q(receita__nome__icontains=part)

                    qs_params = qs_params | q if qs_params else q

                qs = qs.filter(qs_params)

            if nProduto:
                qs = qs.filter(produto__id=int(nProduto))

            if sSituacao:
                qs_params = None
                situacao_parts = sSituacao.split('+')
                for part in situacao_parts:
                    q = Q(situacao__nome__icontains=part)

                    qs_params = qs_params | q if qs_params else q

                qs = qs.filter(qs_params)

            if sTemperatura_Auto:
                qs_params = None
                temperatura_parts = sTemperatura_Auto.split('+')
                for part in temperatura_parts:
                    q = Q(temperatura_auto__icontains=part)

                    qs_params = qs_params | q if qs_params else q

                qs = qs.filter(qs_params)

            if sTipoTemperatura:
                qs_params = None
                tipotemperatura_parts = sTipoTemperatura.split('+')
                for part in tipotemperatura_parts:
                    q = Q(tipotemperatura__nome__icontains=part)

                    qs_params = qs_params | q if qs_params else q

                qs = qs.filter(qs_params)

            if sResponsavel:
                qs = qs.filter(responsavel__id=int(sResponsavel))
                
            if sLider:
                widget = Widgets(self.request.user, {"id":int(sLider),"tipo":"usuario"}, "")
                qs = qs.filter(lider__id__in=widget.getMembros())

            if sDtFechamento:
                try:
                    if ':' in sDtFechamento:
                        sDtFechamento_parts = sDtFechamento.split(':')
                        dDataIni = datetime.datetime.strptime(sDtFechamento_parts[0],"%d/%m/%Y")
                        dDataFim = datetime.datetime.strptime(sDtFechamento_parts[1],"%d/%m/%Y")

                        qs = qs.filter(dtFechamento__gte=dDataIni)
                        qs = qs.filter(dtFechamento__lte=dDataFim)
                    else:
                        if '>=' in sDtFechamento:
                            sDtFechamento = sDtFechamento.replace(">=", "")
                            dData =  datetime.datetime.strptime(sDtFechamento,"%d/%m/%Y")
                            qs = qs.filter(dtFechamento__gte=dData)
                        elif '>' in sDtFechamento:
                            sDtFechamento = sDtFechamento.replace(">", "")
                            dData =  datetime.datetime.strptime(sDtFechamento,"%d/%m/%Y")
                            qs = qs.filter(dtFechamento__gt=dData)
                        elif '<=' in sDtFechamento:
                            sDtFechamento = sDtFechamento.replace("<=", "")
                            dData =  datetime.datetime.strptime(sDtFechamento,"%d/%m/%Y")
                            qs = qs.filter(dtFechamento__lte=dData)
                        elif '<' in sDtFechamento:
                            sDtFechamento = sDtFechamento.replace("<", "")
                            dData =  datetime.datetime.strptime(sDtFechamento,"%d/%m/%Y")
                            qs = qs.filter(dtFechamento__lt=dData)
                        else:
                            dData =  datetime.datetime.strptime(sDtFechamento,"%d/%m/%Y")
                            qs = qs.filter(dtFechamento=dData)
                except Exception, e:
                    print 'Falha no filtro de data de fechamento na oportunidade'

            if nValor: #Não realiza filtros se igual a zero pois deve trazer todos
                vals = constants.OPT_VALS[int(nValor)]
                ini = vals['ini']
                end = vals['end']

                if ini:
                    qs = qs.filter(valor__gte=ini)

                if end:
                    qs = qs.filter(valor__lte=end)

            if nValor: #Não realiza filtros se igual a zero pois deve trazer todos
                vals = constants.OPT_VALS[int(nValor)]
                ini = vals['ini']
                end = vals['end']

                if ini:
                    qs = qs.filter(valor__gte=ini)

                if end:
                    qs = qs.filter(valor__lte=end)

            if rtc != "" and rtc != None: #Faz o teste dessa maneira para permitir o Zero
                qs = qs.filter(rtc=int(rtc))

            if mw != "" and mw != None: #Faz o teste dessa maneira para permitir o Zero
                qs = qs.filter(mw=int(mw))

            if bc != "" and bc != None: #Faz o teste dessa maneira para permitir o Zero
                qs = qs.filter(bc=int(bc))


        return qs

    def get_context_data(self, *args, **kwargs):
        request = self.request
        self.initialize(*args, **kwargs)

        qs = self.get_initial_queryset()

        # number of records before filtering
        total_records = qs.count()

        qs = self.filter_queryset(qs)

        # number of records after filtering
        total_display_records = qs.count()

        qs = self.ordering(qs)

        #Pega valor total antes da paginação
        for item in qs:
            self.valTotal += item.valor
            self.pondTotal += item.ponderado

        qs = self.paging(qs)

        # prepare output data
        aaData = self.prepare_results(qs)

        ret = {'sEcho': int(request.REQUEST.get('sEcho', 0)),
               'iTotalRecords': total_records,
               'iTotalDisplayRecords': total_display_records,
               'aaData': aaData,
               'totalValor': self.valTotal,
               'totalPond': self.pondTotal,
            }

        return ret

class OportunidadeGetLider(CoreMixinLoginRequired, JSONResponseMixin, TemplateView):
    """
    Retorna em json o líder 
    """
    def get(self, request, *args, **kwargs):
        """
        Só envia usuário que seja lider do usuário repassado por parâmetro
        """
        users = Usuario.objects \
                        .filter(
                            id__in=Membro.objects.filter(
                                    id__in=Membro.objects \
                                                 .filter(
                                                    usuario__id=self.kwargs.get('pk', None)
                                                 ).values_list('lider__id')
                            ).values_list('usuario__id')
                        ).exclude(is_active=False)
        
        data = []
        for user in users:
            data.append({
                'id' : user.id,
                'first_name': user.first_name,
                'last_name' : user.last_name,
            })

        context = data
        return self.render_to_response(context)

class Mixin_Oportunidade_Form_Valid(CoreMixinForm):
    """
    Mixin para customizar def de para formulários válidos incluindo as respostas
    enviadas
    """
    def form_valid(self, respostas, form):
        response = super(Mixin_Oportunidade_Form_Valid, self).form_valid(form)

        if respostas:
            for item in respostas:
                result = ast.literal_eval(item)
                respostaFilter = Resposta.objects.filter(
                    oportunidade__id=self.object.id,
                    questao__id=result['questao']
                )

                if respostaFilter.exists():
                    row = respostaFilter[0]
                    if row.resposta != result['resposta']:
                        row.resposta = result['resposta']
                        row.save()
                else:
                    row = Resposta.objects.create(
                        questao=Questao.objects.get(pk=result['questao']),
                        resposta=result['resposta'],
                        oportunidade=self.object
                    ).save()
    
        context={
            'success':True, 
            'message': 'Registro salvo com sucesso...',
            'pk': self.object.id,
        }

        return self.render_to_json_reponse(
            context=context,
            status=200
        )
    
class OportunidadeCreateForm(CoreMixinLoginRequired, CreateView, Mixin_Oportunidade_Form_Valid):
    """
    Formulário de criação de oportunidades
    """
    model = Oportunidade
    template_name = 'oportunidade_form.html'
    success_url = '/'
    form_class = OportunidadeForm

    def get(self, request, *args, **kwargs):
        from tsm.cliente.models.cliente import Cliente

        membros = Membro.objects.filter(usuario__id=request.user.id)
        filiais = Usuario.objects.get(id=request.user.id).filiais.all()
        #Sempre carrega o formulário com lideres vazio para busca via ajax
        if membros.exists():
            membro = membros[0]
            liderados = Usuario.objects.filter(
                id__in=Membro.objects.filter(Q(lider__id=membro.id)|Q(id=membro.id)) \
                                     .values_list('usuario__id')
            ).exclude(is_active=False)
            widget = Widgets(self.request.user, {"id":request.user.id,"tipo":"usuario"}, "")
            carteirasFilter = Cliente.objects.filter(executivo__id__in=widget.getMembros())
        else:
            liderados = Usuario.objects.filter(
                id__in=Membro.objects.all().values_list('usuario__id'),
                filiais__id__in=filiais
            ).exclude(is_active=False)
            carteirasFilter = Cliente.objects.filter(Q(filial__id__in=filiais)|Q(filial__isnull=True))

        idFuncArq = getParamByName(constants.PAR_FUNCARQ,request.user.id)
        idFuncGPP = getParamByName(constants.PAR_FUNCGPP,request.user.id)
        
        arquitetos = Usuario.objects.filter(funcao__id=int(idFuncArq), is_active=True, filiais__id__in=filiais)
        gpp = Usuario.objects.filter(funcao__id=int(idFuncGPP), is_active=True, filiais__id__in=filiais)
        
        form = OportunidadeForm(
            carteiras=carteirasFilter, 
            liderados=liderados,
            lider=Usuario.objects.filter(id=request.user.id),
            filiais=filiais,
            arquitetos=arquitetos,
            gpp=gpp,
            produtos=Produto.objects.filter(Q(filial__in=filiais)|Q(filial__isnull=True)),
            request=request,
            initial={
                'criador':request.user.id,
                'temperatura_auto':'Baixa'
            }
        )
        self.object = None
        questoes = Questao.objects.filter(Q(filial__id__in=filiais)|Q(filial__isnull=True)).order_by('ordem')
        questoesRender = []
        for questao in questoes:
            questoesRender.append({
                'id':questao.id,
                'pergunta':questao.pergunta,
                'sim':questao.sim,
                'nao':questao.nao,
                'resposta':False,
            })

        return self.render_to_response(self.get_context_data(form=form,questoes=questoesRender,rtc=[]))

    def post(self, request, *args, **kwargs):
        self.object = None

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        respostas = request.POST.getlist('respostas[]')
        arquitetos = request.POST.getlist('arquitetos[]')

        if not len(respostas):
            return self.render_to_json_reponse({
                    "respostas":"Você precisa responder todas as perguntas.",
                    "message":"Existem erros no formulário.",
                }, status=400)

        if form.is_valid():
            form.cleaned_data['arquitetos'] = arquitetos
            return self.form_valid(respostas, form)
        else:
            return self.form_invalid(form)

class OportunidadeUpdateForm(CoreMixinLoginRequired, UpdateView, Mixin_Oportunidade_Form_Valid):
    """
    Formulário de edição de oportunidades
    """
    model = Oportunidade
    template_name = 'oportunidade_form.html'
    success_url = '/'
    form_class = OportunidadeFormUpdate

    def get(self, request, *args, **kwargs):
        
        membros = Membro.objects.filter(usuario__id=request.user.id)
        filiais = Usuario.objects.get(id=request.user.id).filiais.all()

        if membros.exists():
            membro = membros[0]
            #Verifica pode ver todas oportunidades, senão só exibe se usuário tiver acesso
            if not request.user.has_perm('oportunidade.list_all_opportunities'):
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

            self.object = self.get_object(Oportunidade.objects.filter(qs_base_filter))

            liderados = Usuario.objects.filter(
                    Q(
                        id__in=Membro.objects.filter(Q(lider__id=membro.id)|Q(id=membro.id)) \
                                             .values_list('usuario__id')
                    )|Q(id=self.object.responsavel.id)
            ).exclude(is_active=False)
            
        else:
            self.object = self.get_object(Oportunidade.objects.filter(filial__id__in=filiais))
            liderados = Usuario.objects.filter(
                id__in=Membro.objects.all().values_list('usuario__id'),
                filiais__id__in=filiais
            ).exclude(is_active=False)

        respostas = Resposta.objects.filter(oportunidade__id=self.object.id).order_by('questao__ordem')
        questoesRender = []
        for resposta in respostas:
            questoesRender.append({
                'id':resposta.questao.id,
                'pergunta':resposta.questao.pergunta,
                'sim':resposta.questao.sim,
                'nao':resposta.questao.nao,
                'resposta':resposta.resposta,
            })

        idFuncArq = getParamByName(constants.PAR_FUNCARQ,request.user.id)
        idFuncGPP = getParamByName(constants.PAR_FUNCGPP,request.user.id)
        
        arquitetos = Usuario.objects.filter(funcao__id=int(idFuncArq), is_active=True, filiais__id__in=filiais)
        gpp = Usuario.objects.filter(funcao__id=int(idFuncGPP), is_active=True, filiais__id__in=filiais)
        
        hoje = date.today()
        rtc = Rtc.objects.filter(oportunidade__id=self.object.id,data__gte=hoje)[:5]
        
        if rtc and not self.object.rtc:
            self.object.rtc = True

        self.object.save()

        form = OportunidadeFormUpdate(
            instance=self.object,
            liderados=liderados,
            lider=Usuario.objects.filter(Q(id=request.user.id)|Q(id=self.object.lider.id)),
            arquitetos=arquitetos,
            produtos=Produto.objects.filter(Q(filial__in=filiais)|Q(filial__isnull=True)),
            tipotemperatura=TipoTemperatura.objects.all(),
            gpp=gpp,
            user=request.user,
            initial={
                'criador':request.user.id,
            }
        )
        return self.render_to_response(self.get_context_data(form=form, questoes=questoesRender, rtc=rtc))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        self.object.arquitetos.clear()
        respostas = request.POST.getlist('respostas[]')
        arquitetos = request.POST.getlist('arquitetos[]')

        if form.is_valid():
            form.cleaned_data['arquitetos'] = arquitetos

            return self.form_valid(respostas,form)
        else:
            return self.form_invalid(form)

class OportunidadeTemperatura(CoreMixinLoginRequired, JSONResponseMixin, TemplateView):
    """
    Api para cálculo da temperatura automática
    """
    def get(self, request, *args, **kwargs):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()

    def post(self, request, *args, **kwargs):
        from django.core.exceptions import PermissionDenied
        from tsm.oportunidade.util import calculoTemperatura
        
        """
        Recebe o post com os dados de respostas e envia para rotina de cálculo
        de temperatura
        """
        result = request.POST.getlist('respostas[]')
        if not result:
            raise PermissionDenied()

        respostas = []
        for item in result:
            respostas.append(ast.literal_eval(item))

        temperatura = calculoTemperatura(respostas)

        return self.render_to_response({
                    'success':True, 
                    'temperatura': temperatura,
                })

class OportunidadeDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Oportunidade
    success_url = '/oportunidade/lista/'

class OportunidadeFastUpdate(CoreMixinLoginRequired, JSONResponseMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()

    def post(self, request, *args, **kwargs):
        from django.core.exceptions import PermissionDenied
        
        objectRow = Oportunidade.objects.get(id=self.kwargs.get('pk',None))
                
        if self.request.method in ('POST', 'PUT'):

            if self.request.POST.get('receita',None) and self.request.POST.get('situacao',None) and \
                self.request.POST.get('valor',None) and self.request.POST.get('tipotemperatura',None) and \
                self.request.POST.get('dtFechamento',None):
                objectRow.receita = Receita.objects.get(id=self.request.POST.get('receita',None))
                objectRow.situacao = Situacao.objects.get(id=self.request.POST.get('situacao',None))
                objectRow.valor = float(self.request.POST.get('valor',None))
                objectRow.tipotemperatura = TipoTemperatura.objects.get(id=self.request.POST.get('tipotemperatura',None))
                objectRow.dtFechamento = datetime.datetime.strptime(self.request.POST.get('dtFechamento',None),"%d/%m/%Y")
                objectRow.produto = Produto.objects.get(id=self.request.POST.get('produto',None))
                objectRow.save()
            else:
                return self.render_to_response({
                    'success':False, 
                    'message': 'Existem dados inválidos no formulário.',
                })                

        return self.render_to_response({
                'success':True, 
                'message': 'Registro salvo com sucesso...',
                'data': {
                    "id"             : objectRow.id,
                    "receita"        : objectRow.receita.nome,
                    "situacao"       : objectRow.situacao.nome,
                    "valor"          : objectRow.valor,
                    "ponderado"      : objectRow.ponderado,
                    "tipotemperatura": objectRow.tipotemperatura.nome,
                    "dtFechamento"   : objectRow.dtFechamento.strftime("%d/%m/%Y"),
                    "produto"        : objectRow.produto.nome,
                }
            })

class OportunidadeCheck(CoreMixinLoginRequired, JSONResponseMixin, TemplateView):
    """
    Check de MW e BC
    """
    def get(self, request, *args, **kwargs):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()

    def post(self, request, *args, **kwargs):
        from django.core.exceptions import PermissionDenied
        
        objectRow = Oportunidade.objects.get(id=self.kwargs.get('pk',None))
                
        if self.request.method in ('POST', 'PUT'):
            mwChk = self.request.POST.get('mw',None)
            bcChk = self.request.POST.get('bc',None)

            if mwChk != None:
                objectRow.mw = True if int(mwChk) else False

            if bcChk != None:
                objectRow.bc = True if int(bcChk) else False

            if objectRow.mw or objectRow.bc:
                typeCommited = getParamByName(constants.PAR_COMMITED_ID, request.user.pk)
                if typeCommited:
                    objectRow.situacao = Situacao.objects.get(pk=int(typeCommited))

            objectRow.save()

        return self.render_to_response({'success':True, 'situacao': objectRow.situacao.nome})
