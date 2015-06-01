# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.shortcuts import redirect

from tsm.core.base.core_base_datatable import CoreBaseDatatableView
from tsm.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel, CoreMixinPassRequestForm
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired

from tsm.cliente.models.cliente import Cliente
from tsm.cliente.forms.clienteform import ClienteForm, ClienteFormMin

from tsm.oportunidade.widgets import Widgets

class ClienteList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista
    """
    template_name = 'cliente_list.html'
    
class ClienteData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista
    """
    model = Cliente
    columns = ['cnpj' ,'nome' ,'estado' , 'buttons']
    order_columns = ['cnpj' ,'nome' ,'estado']
    max_display_length = 500
    url_base_form = '/cliente/clientes/'

    def get_initial_queryset(self):
        from tsm.acesso.models.usuario import Usuario

        if not self.model:
            raise NotImplementedError("Need to provide a model or implement get_initial_queryset!")

        filiais = Usuario.objects.get(id=self.request.user.id).filiais.all()
        if self.request.user.has_perm('equipe.list_all_members'):
            qs = self.model.objects.filter(executivo__in=Usuario.objects.filter(filiais__in=filiais).order_by('first_name','last_name'))
        else:
            widget = Widgets(self.request.user, {"id":self.request.user.id,"tipo":"usuario"}, "")
            qs = self.model.objects.filter(executivo__id__in=widget.getMembros())

        return qs
    
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
                q = Q(nome__contains=part)|Q(estado__istartswith=part)|Q(cnpj__istartswith=part)
                qs_params = qs_params | q if qs_params else q
            
            qs = qs.filter(qs_params)

        filiais = Usuario.objects.get(id=self.request.user.id).filiais.all()
        qs = qs.filter(filial__id__in=filiais)
        return qs

class ClienteCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm, CoreMixinPassRequestForm):
    """
    Formulário de criação
    """
    model = Cliente
    template_name = 'cliente_form.html'
    success_url = '/'
    form_class = ClienteForm

    def post(self, request, *args, **kwargs):
        self.object = None

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        produtos = request.POST.getlist('produtos[]')

        if form.is_valid():
            form.cleaned_data['produtos'] = produtos
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        response = super(ClienteCreateForm, self).form_valid(form)
        return self.render_to_json_reponse(context={'success':True, 'message': 'Registro salvo com sucesso...', 'id': self.object.id},status=200)

class ClienteCreateFormMin(CoreMixinLoginRequired, CreateView, CoreMixinForm, CoreMixinPassRequestForm):
    """
    Formulário de criação mínimo utilizado em popups para inclusão rápida
    """
    model = Cliente
    template_name = 'cliente_form_min.html'
    success_url = '/'
    form_class = ClienteFormMin

    def form_valid(self, form):
        response = super(ClienteCreateFormMin, self).form_valid(form)
        return self.render_to_json_reponse(context={'success':True, 'message': 'Registro salvo com sucesso...', 'pk': self.object.id},status=200)

class ClienteUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm, CoreMixinPassRequestForm):
    """
    Formulário de criação
    """
    model = Cliente
    template_name = 'cliente_form.html'
    success_url = '/'
    form_class = ClienteForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        produtos = request.POST.getlist('produtos[]')

        if form.is_valid():
            form.cleaned_data['produtos'] = produtos
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class ClienteDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Cliente
    success_url = '/cliente/clientes/'