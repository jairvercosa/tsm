# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView

from tsm.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired
from tsm.core.mixins.core_mixin_base import CoreMixinDispatch
from tsm.core.mixins.core_mixin_json import JSONResponseMixin

from tsm.acesso.models.usuario import Usuario
from tsm.equipe.models.membro import Membro
from tsm.equipe.models.membrometa import MembroMeta
from tsm.equipe.forms.membrometaform import MembroMetaForm

class MembroMetaForm(CoreMixinLoginRequired, CreateView, CoreMixinForm):
    """
    Formulário para adição de metas
    """
    model = MembroMeta
    form_class = MembroMetaForm
    template_name = 'membro_meta_form.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('equipe.add_self_membrometa'):
            membro = Membro.objects.get(id=request.POST['membro'])
            if membro:
                if membro.usuario.id == request.user.id:
                    return self.render_to_json_reponse(
                        context={
                            'success':False, 
                            'message': 'Você não pode atribuir metas para você mesmo.',
                        },
                        status=400
                    )
                else:
                    userMembro = Membro.objects.get(usuario__id=request.user.id)
                    if userMembro:
                        if membro.id == userMembro.lider.id:
                            return self.render_to_json_reponse(
                                context={
                                    'success':False, 
                                    'message': 'Você não pode atribuir metas para seu lider.',
                                },
                                status=400
                            )

        return super(MembroMetaForm, self).post(request, *args, **kwargs)

    def get_form_kwargs(self, **kwargs):
        kwargs = super(MembroMetaForm, self).get_form_kwargs(**kwargs)
        usuario = Usuario.objects.get(id=self.request.user.id)
        kwargs['initial']['criador'] = usuario
        return kwargs    

    #Retorno caso o formulário seja válido
    def form_valid(self, form):
        response = super(MembroMetaForm, self).form_valid(form)
        return self.render_to_json_reponse(context={'success':True, 'message': 'Registro salvo com sucesso...', 'id':self.object.id},status=200)

class MembroMetaDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = MembroMeta
    success_url = '/equipe/'

class MembroMetaList(CoreMixinLoginRequired, JSONResponseMixin, TemplateView):
    """
    Retorna em json as metas de um membro
    """
    def get(self, request, *args, **kwargs):
        from datetime import date
        metas = MembroMeta.objects.filter(membro_id=self.kwargs.get('pk', None)) \
                                  .exclude(anoVigencia__lt=date.today().year) \
                                  .exclude(mesVigencia__lt=str(date.today().month).zfill(2))
        
        data = []
        if metas:
            for meta in metas:
                if not request.user.has_perm('equipe.add_self_membrometa'):
                    if not meta.is_Visible:
                        continue

                data.append({
                    'id'            : meta.id,
                    'tipometa'      : meta.tipometa.nome,
                    'receita'       : meta.receita.nome,
                    'valor'         : meta.valor,
                    'mesVigencia'   : meta.mesVigencia,
                    'anoVigencia'   : meta.anoVigencia,
                    'isVisible'     : meta.is_Visible,
                })
        
        context = data
        return self.render_to_response(context)

class MembroMetaValida(CoreMixinLoginRequired, JSONResponseMixin, TemplateView):
    """
    Esta classe valida se um membro atribuiu todas as metas aos seus liderados baseado
    nas metas atribuidas para ele.
    """
    def get(self, request, *args, **kwargs):
        from datetime import date
        from django.db.models import Sum
        
        year = date.today().year
        month = str(date.today().month).zfill(2)
        membro_filter = self.kwargs.get('pk')
        msgReturn = 'As metas dos liderados deste membro não estão totalmente atribuidas.'

        if not request.user.has_perm('equipe.add_self_membrometa'):
            me = Membro.objects.get(usuario__id=request.user.id)
            if me:
                if me.id != int(membro_filter):
                    """
                    Se não tem permissão para atribuir meta para si, então
                    não pode ver erros de metas dos outros membros
                    """
                    return self.render_to_response({'result':True})
        
        #Busca total por meta do membro
        metasMembro = MembroMeta.objects.filter(
                                            membro__id=membro_filter, 
                                            mesVigencia__gte=month, 
                                            anoVigencia__gte=year,
                                            is_Visible=True
                                        ).values('tipometa_id', 'receita_id', 'mesVigencia', 'anoVigencia') \
                                         .annotate(valorMeta=Sum('valor'))

        if not metasMembro:
            #Membro não tem metas então está ok
            return self.render_to_response({'result':True})

        #Busca metas dos liderados
        metasLiderados = MembroMeta.objects.filter(
                            membro__id__in = Membro.objects.filter(lider_id=membro_filter) \
                                                           .values_list('id', flat=True),
                            mesVigencia__gte=month, 
                            anoVigencia__gte=year
                        ).values('tipometa_id', 'receita_id', 'mesVigencia', 'anoVigencia') \
                         .annotate(valorMeta=Sum('valor'))

        if not metasLiderados:
            liderados = Membro.objects.filter(lider__id=membro_filter)
            if not liderados:
                #Não existem liderados para atribuir meta, por isso está ok
                return self.render_to_response({'result':True})
            else:
                return self.render_to_response({
                            'result':False, 
                            'message': msgReturn
                        })

        for item in metasMembro:
            for child in metasLiderados:
                if child['tipometa_id'] == item['tipometa_id'] and \
                   child['receita_id']  == item['receita_id']  and \
                   child['mesVigencia'] == item['mesVigencia'] and \
                   child['anoVigencia'] == item['anoVigencia']:
                    if child['valorMeta'] < item['valorMeta']:
                        return self.render_to_response({
                            'result':False, 
                            'message': msgReturn
                        })  

        return self.render_to_response({'result':True})

class MembroMetaVisible(CoreMixinLoginRequired, JSONResponseMixin, TemplateView, CoreMixinDispatch):
    """
    View para alteração da visibilidade das metas
    """
    def get(self, request, *args, **kwargs):
        return self.render_to_response({})

    def post(self, request, *args, **kwargs):
        meta = MembroMeta.objects.get(id=self.kwargs.get('pk'))

        if not meta:
            return self.render_to_response({})

        if request.POST['isVisible'] == "true":
            meta.is_Visible = True
        else:
            meta.is_Visible = False
        
        meta.save()

        return self.render_to_response({})


    def render_to_response(self, context):
        return JSONResponseMixin.render_to_response(self, context)