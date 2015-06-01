# -*- coding: ISO-8859-1 -*-
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q

from tsm.core.base.core_base_datatable import CoreBaseDatatableView
from tsm.core.mixins.core_mixin_base import CoreMixinDispatch
from tsm.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired
from tsm.core.mixins.core_mixin_json import JSONResponseMixin

from tsm.acesso.models.usuario import Usuario
from tsm.equipe.models.membro import Membro
from tsm.cliente.models.carteira import Carteira
from tsm.oportunidade.models.oportunidade import Oportunidade

class EquipeEstrutura(CoreMixinLoginRequired, TemplateView):
    """
    View para visão da estrutura
    """
    template_name = 'equipe_estrutura.html'

    def get(self, request, *args, **kwargs):
        """
        Realiza validação se o usuário pode incluir meta para si. Caso positivo, retorna
        o idMemberUser igual a zero para que o front-end não faça validações e libere acesso
        total a tela
        """
        context = { 'idMemberUser' : 0 }
        if not request.user.has_perm('equipe.add_self_membrometa'):
            membro = get_object_or_404(Membro,usuario__id=request.user.id)
            if membro:
                context = { 'idMemberUser' : membro.id }

        return self.render_to_response(context)

class EquipeStaffGet(CoreMixinLoginRequired, JSONResponseMixin, TemplateView):
    """
    Retorna em json os staffs disponíveis para este grupo
    """
    def get(self, request, *args, **kwargs):
        """
        Só envia usuários que estejam nas filiais que o usuário logado tem acesso
        """
        users = Usuario.objects \
                    .filter(filiais__id__in = Usuario.objects.filter(id=request.user.id).values_list('filiais__id', flat=True)) \
                    .filter(showToTeam=True) \
                    .filter(is_active=True) \
                    .exclude(funcao__isnull=True) \
                    .exclude(id__in = Membro.objects.all().values_list('usuario_id', flat=True)) \
                    .distinct()
        
        data = []
        for user in users:
            data.append({
                'user_id' : user.id,
                'first_name': user.first_name,
                'last_name' : user.last_name,
                'funcao'    : user.funcao.nome,
            })

        context = data
        
        return self.render_to_response(context)

class EquipeMembrosGet(CoreMixinLoginRequired, JSONResponseMixin, TemplateView):
    """
    Retorna os níveis do grupo
    """
    def get(self, request, *args, **kwargs):
        """
        Retorna apenas os membros que o usuário pode ver
        """
        if not request.user.has_perm('equipe.list_all_members'):
            userMembers = Membro.objects.filter(usuario__id=request.user.id)
            assitMembers = Membro.objects.filter(
                usuario__id__in=Usuario.objects.filter(
                    assistentes=request.user.id
                )
            )

            qs_params = Q(id__in=userMembers)| \
                        Q(lider__id__in=userMembers)| \
                        Q(id__in=assitMembers)| \
                        Q(lider__id__in=assitMembers)
            if userMembers:
                userMember = userMembers[0]
                if userMember.lider:
                    qs_params = qs_params | Q(id=userMember.lider.id)

            members = Membro.objects.filter(qs_params)
        else:
            filiais = Usuario.objects.get(id=request.user.id).filiais.all()
            members = Membro.objects.filter(usuario__id__in=Usuario.objects.filter(filiais__in=filiais))

        data = []
        for member in members:
            data.append({
                'user_id' : member.usuario.id,
                'membro_id': member.id,
                'lider_id': member.lider.id if member.lider else None,
                'first_name': member.usuario.first_name,
                'last_name': member.usuario.last_name,
                'funcao': member.usuario.funcao.nome,
                'metas' : [],
                'carteiras' : [],
            })

        context = data
        return self.render_to_response(context)

class EquipeMembroAdd(CoreMixinLoginRequired, JSONResponseMixin, TemplateView, CoreMixinDispatch):
    """
    Grava um membro em uma equipe
    """
    def post(self, request, *args, **kwargs):
        usuario = get_object_or_404(Usuario,pk=request.POST['usuario_id'])
        
        if usuario:
            membro = Membro.objects.create(criador=request.user, usuario=usuario)
            membro.save()

            if request.POST['lider_id'] and not request.POST['lider_id'] == None:
                lider = get_object_or_404(Membro,pk=request.POST['lider_id'])
                membro.lider = lider

                #Adiciona carteiras do líder
                for carteira in lider.carteiras.all():
                    membro.carteiras.add(carteira.id)

            membro.save()

            context = { 'success': True, 'membro_id': membro.id }
        else:
            context = { 'success': False }
        
        return self.render_to_response(context)

class EquipeMembroChange(CoreMixinLoginRequired, UpdateView, CoreMixinForm):
    """
    Formulário de membros
    """
    model = Membro
    template_name = 'membro_form.html'
    success_url = '/'

    #Retorno caso o formulário seja válido
    def form_valid(self, form):
        oportunidades = Oportunidade.objects.filter(responsavel=self.object.usuario,dtFechado__isnull=True)
        for oportunidade in oportunidades:
            oportunidade.lider = self.object.lider.usuario
            oportunidade.save()

        return super(EquipeMembroChange, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        carteiras = request.POST.getlist('carteiras[]')

        if form.is_valid():
            form.cleaned_data['carteiras'] = carteiras
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
class EquipeMembroDel(CoreMixinLoginRequired, CoreMixinDel, CoreMixinDispatch):
    """
    Remove um membro de uma equipe
    """
    model = Membro
    success_url = '/equipe/equipes/'

class EquipeGetChild(CoreMixinLoginRequired, JSONResponseMixin, TemplateView):
    """
    Retorna um membro e seus subordinados
    """

    def get(self, request, *args, **kwargs):
        #importa pacote de widget
        from tsm.oportunidade.widgets import Widgets

        data = []
        if request.user.has_perm('equipe.list_all_members'):
            userLogged = Usuario.objects.get(id=request.user.id)
            usuarios = Usuario.objects.filter(filiais__in=userLogged.filiais.all()).order_by('first_name','last_name').distinct()
        else:
            membro = get_object_or_404(Membro,usuario__id=request.user.id)
            widget = Widgets(request.user, {"id":membro.usuario.id,"tipo":"usuario"}, "")
            
            membros = widget.getMembros()
            usuarios = Usuario.objects.filter(id__in=membros).order_by('first_name','last_name')

        for usuario in usuarios:
            data.append({
                'id':usuario.id,
                'nome': usuario.first_name+' '+usuario.last_name
            })

        return self.render_to_response(data)

class EquipeMembroMudaLider(CoreMixinLoginRequired, JSONResponseMixin, TemplateView, CoreMixinDispatch):
    """
    Muda o lider de um membro na estrutura
    """

    def get(self, request, *args, **kwargs):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()

    def post(self, request, *args, **kwargs):
        membro = get_object_or_404(Membro,pk=self.kwargs.get('pk', None))

        liderId = request.POST.get('lider',None)
        changeOportunidades = request.POST.get('changeop',False)

        if not liderId:
            context = { 'success': False, 'message': 'Lider não enviado.' }
            return self.render_to_response(context)

        membroLider = get_object_or_404(Membro,pk=liderId)
        if not membroLider:
            context = { 'success': False, 'message': 'Lider não encontrado.' }
            return self.render_to_response(context)

        membro.lider = membroLider
        membro.save()

        if changeOportunidades:
            oportunidades = Oportunidade.objects.filter(responsavel=membro.usuario,dtFechado__isnull=True)
            for item in oportunidade:
                item.lider = membroLider.usuario
                item.save()

        context = { 'success': True }
        return self.render_to_response(context)
