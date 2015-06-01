# -*- coding: ISO-8859-1 -*-
from datetime import date, datetime
from django.core.exceptions import PermissionDenied
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.shortcuts import redirect

from tsm.core.base.core_base_datatable import CoreBaseDatatableView
from tsm.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired
from tsm.core.mixins.core_mixin_json import JSONResponseMixin

from tsm.oportunidade.widgets import Widgets
from tsm.oportunidade.models.rtc import Rtc
from tsm.oportunidade.models.oportunidade import Oportunidade
from tsm.oportunidade.forms.rtcform import RtcForm

from tsm.acesso.models.usuario import Usuario

class RtcList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista
    """
    template_name = 'rtc_list.html'

    def get(self, request, *args, **kwargs):
        oportunidadeID = self.kwargs.get('op', None)
        oportunidade = Oportunidade.objects.get(id=oportunidadeID)

        kwargs.update({"oportunidade":oportunidade})
        kwargs.update({"oportunidadeUrl": str(oportunidade.id)+"/"})

        context = self.get_context_data(**kwargs)

        return self.render_to_response(context)
    
class RtcData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista
    """
    model = Rtc
    columns = ['id','data','descricao','buttons']
    order_columns = ['id','data','descricao']
    max_display_length = 500
    url_base_form = '/oportunidade/lista/'
    
    def filter_queryset(self, qs):
        """
        Filtros da query baseado no datatable
        """
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            search_parts = sSearch.split('+')
            qs_params = None
            for part in search_parts:
                q = Q(descricao__contains=part)
                qs_params = qs_params | q if qs_params else q

            qs = qs.filter(qs_params)

        qs = qs.filter(Q(oportunidade__id=self.kwargs.get('op', None)))

        return qs

    def render_column(self, row, column):
        if column == 'data':
            sReturn = row.data.strftime("%d/%m/%Y")
            return sReturn
        elif column == 'buttons' and self.url_base_form and self.use_buttons:
            sReturn = '<div class="action-buttons">'
            sReturn +='     <a href="'+self.url_base_form+str(row.oportunidade.id)+'/rtc/'+str(row.id)+'/" title="Editar" class="btnEdit"><i class="icon-lapis icon-miniatura"></i></a>'
            sReturn +='     <a href="javascript:;" class="btnDel" alt="'+str(row.id)+'" title="Remover"><i class="icon-x"></i></a>'
            sReturn +='</div>'
            return sReturn
        else:
            return super(RtcData, self).render_column(row, column)

class RtcMixinForm(CoreMixinForm):
    """Mixin do RTC para repassar a request ao formulário
    """
    def get_form_kwargs(self):
        kwargs = super(RtcMixinForm, self).get_form_kwargs()
        kwargs.update({
            "request": self.request
        })

        return kwargs

class RtcCreateForm(CoreMixinLoginRequired, CreateView, RtcMixinForm):
    """
    Formulário de criação
    """
    model = Rtc
    template_name = 'rtc_form.html'
    success_url = '/'
    form_class = RtcForm

    def get(self, request, *args, **kwargs):
        self.object = None

        returnOp = False
        if 'return' in request.GET:
            returnOp = True
        
        oportunidade = Oportunidade.objects.get(id=self.kwargs.get('op',None))
        self.initial = {
            "oportunidade": oportunidade
        }

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        return self.render_to_response(self.get_context_data(
            form=form,
            oportunidade=oportunidade,
            oportunidadeUrl=str(oportunidade.id)+"/",
            returnOp=returnOp
        ))

    def post(self, request, *args, **kwargs):
        self.object = None

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        recursos = request.POST.getlist('recursos[]')
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class RtcUpdateForm(CoreMixinLoginRequired, UpdateView, RtcMixinForm):
    """
    Formulário de edição
    """
    model = Rtc
    template_name = 'rtc_form.html'
    success_url = '/'
    form_class = RtcForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        returnOp = False
        if 'return' in request.GET:
            returnOp = True

        oportunidade = Oportunidade.objects.get(id=self.kwargs.get('op',None))    
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        return self.render_to_response(self.get_context_data(
            form=form,
            oportunidade=oportunidade,
            oportunidadeUrl=str(oportunidade.id)+"/",
            returnOp=returnOp
        ))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        self.object.recursos.clear()
        recursos = request.POST.getlist('recursos[]')
        if form.is_valid():
            form.cleaned_data['recursos'] = recursos
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class RtcDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Rtc
    success_url = '/oportunidade/rtc/'

class RtcAgenda(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da agenda
    """
    template_name = 'rtc_agenda.html'

    def get(self, request, *args, **kwargs):
        #instancia o objeto de widgets por conter o get de membros completo da hierarquia
        if request.user.has_perm('equipe.list_all_members'):
            usuarios = Usuario.objects.all().order_by('first_name', 'last_name' )
        else:
            widget = Widgets(request.user, {"id":request.user.id,"tipo":"usuario"}, "")
            membros = widget.getMembros()

            usuarios = Usuario.objects.filter(id__in=membros).order_by('first_name', 'last_name' )

        kwargs.update({"usuarios":usuarios})
        kwargs.update({"hoje":date.today().strftime("%Y-%m-%d")})

        context = self.get_context_data(**kwargs)

        return self.render_to_response(context)

class RtcAgendaData(CoreMixinLoginRequired, JSONResponseMixin, TemplateView):
    """
    View para renderização da agenda json
    """
    def get(self, request, *args, **kwargs):
        if not 'usuario' in request.GET:
            raise PermissionDenied()
        elif not 'start' in request.GET:
            raise PermissionDenied()
        elif not 'end' in request.GET:
            raise PermissionDenied()

        usuarioRequest = Usuario.objects.get(id=request.GET.get('usuario',None))
        start = datetime.strptime(request.GET.get('start',None),'%Y-%m-%d')
        end = datetime.strptime(request.GET.get('end',None),'%Y-%m-%d')
        
        #instancia o objeto de widgets por conter o get de membros completo da hierarquia
        if usuarioRequest.has_perm('equipe.list_all_members'):
            usuarios = Usuario.objects.all()
        else:
            widget = Widgets(request.user, {"id":usuarioRequest.id,"tipo":"usuario"}, "")
            membros = widget.getMembros()

            usuarios = Usuario.objects.filter(id__in=membros)

        eventos = Rtc.objects.filter(
            oportunidade__id__in=Oportunidade.objects.filter(Q(lider__id__in=usuarios)|Q(responsavel__id__in=usuarios)),
            data__gte=start,
            data__lte=end
        )

        dataReturn = []

        for evento in eventos:
            dataReturn.append({
                "id": evento.id,
                "title": evento.oportunidade.cliente.nome[:10] + '... ' + evento.descricao[:40],
                "start": evento.data.strftime("%Y-%m-%d")+'T'+evento.hora.strftime("%H:%M:%S")
            })
            
        context = dataReturn
        return self.render_to_response(context)
        
class RtcMinView(CoreMixinLoginRequired, DetailView):
    """
    visualização mínima do evento
    """
    template_name = 'rtc_evento.html'
    model = Rtc