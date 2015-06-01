# -*- coding: ISO-8859-1 -*-
from django.template.response import TemplateResponse
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.shortcuts import redirect
from django.db.models import Q

from tsm.acesso.models.usuario import Usuario
from tsm.acesso.forms.usuarioform import UsuarioCreateForm, UsuarioUpdateForm, UsuarioTrocaSenha
from tsm.core.base.core_base_datatable import CoreBaseDatatableView
from tsm.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired

class UsuariosList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista de usuários
    """
    template_name = 'usuario_list.html'
    
class UsuariosData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista de usuários
    """
    model = Usuario
    columns = ['username','name','email','status','buttons']
    order_columns = ['username',['first_name','last_name'],'email','is_active']
    max_display_length = 500
    url_base_form = '/acesso/usuarios/'
    
    def render_column(self, row, column):
        """
        Renderização das colunas
        """

        if column == 'name':
            return '%s %s' % (row.first_name, row.last_name)
        elif column == 'status':
            return 'Ativo' if row.is_active else 'Inativo'
        else:
            return super(UsuariosData, self).render_column(row, column)

    def filter_queryset(self, qs):
        """
        Filtros da query baseado no datatable
        """
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            search_parts = sSearch.split('+')
            qs_params = None
            for part in search_parts:
                if part.lower() == 'ativo':
                    q = Q(is_active=1)
                elif part.lower() == 'inativo':
                    q = Q(is_active=0)
                else:
                    q = Q(username__istartswith=part)|Q(first_name__istartswith=part)|Q(last_name__istartswith=part)|Q(email__istartswith=part)

                qs_params = qs_params | q if qs_params else q

            qs = qs.filter(qs_params)
        return qs

class UsuariosCreateForm(CoreMixinLoginRequired, CoreMixinForm):
    """
    View de formulário de usuários
    """
    template_name = 'usuario_form.html'
    model = Usuario
    form_class = UsuarioCreateForm
    success_url = '/acesso/usuarios/'

    #Retorno caso o formulário seja válido
    def form_valid(self, form):
        response = super(FormView, self).form_valid(form)
        self.object = form.save()
        return self.render_to_json_reponse(context={'success':True, 'message': 'Registro salvo com sucesso...'},status=200)


class UsuariosUpdateForm(UsuariosCreateForm, UpdateView, CoreMixinForm):
    """
    View de formulário de atualização de usuários
    """
    form_class = UsuarioUpdateForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        segmentos = request.POST.getlist('segmentos[]')
        receitas = request.POST.getlist('receitas[]')
        assistentes = request.POST.getlist('assistentes[]')
        permissions = request.POST.getlist('user_permissions[]')
        groups = request.POST.getlist('groups[]')
        filiais = request.POST.getlist('filiais[]')

        if form.is_valid():
            form.cleaned_data['segmentos'] = segmentos
            form.cleaned_data['receitas'] = receitas
            form.cleaned_data['assistentes'] = assistentes
            form.cleaned_data['user_permissions'] = permissions
            form.cleaned_data['groups'] = groups
            form.cleaned_data['filiais'] = filiais
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    #Retorno caso o formulário seja válido
    def form_valid(self, form):
        response = super(UsuariosCreateForm, self).form_valid(form)
        return self.render_to_json_reponse({'success': True, 'message': 'Registro incluido com sucesso.'},status=200)

class UsuariosDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Usuario
    success_url = '/acesso/usuarios/'

    def get(self, request, *args, **kwargs):
        """
        Get da view
        """
        return redirect('/acesso/usuarios/')

class UsuariosSetPassForm(CoreMixinLoginRequired, CoreMixinForm, FormView):
    """
    View para troca de senha
    """
    response_class = TemplateResponse
    template_name = 'usuario_form_change_pass.html'

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        password_change_form = UsuarioTrocaSenha
        usuario = Usuario.objects.get(pk=self.request.user.pk)

        if self.request.method == "POST":
            form = password_change_form(user=self.request.user, data=self.request.POST)
            if form.is_valid():
                #retira a obrigatoriedade de trocar a senha
                usuario.forca_troca_senha = False
                usuario.save()

                form.save()
                return self.render_to_json_reponse({},status=200)
            else:
                return self.render_to_json_reponse(form.errors, status=400)
        else:
            form = password_change_form(user=self.request.user)
        
        context = {
            'form': form,
            'userUpdate': self.request.user,
        }
        return self.response_class(
            request = self.request,
            template = self.template_name,
            context = context,
            **response_kwargs
        )

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)