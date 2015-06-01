# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.shortcuts import redirect

from tsm.core.util import get_filiais
from tsm.core.base.core_base_datatable import CoreBaseDatatableView
from tsm.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel, CoreMixinPassRequestForm
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired
from tsm.oportunidade.models.questao import Questao
from tsm.oportunidade.forms.questaoform import QuestaoForm

class QuestaoList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista de questoes
    """
    template_name = 'questao_list.html'
    
class QuestaoData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista de questoes
    """
    model = Questao
    columns = ['ordem','pergunta','buttons']
    order_columns = ['ordem','pergunta']
    max_display_length = 500
    url_base_form = '/oportunidade/questoes/'
    
    def filter_queryset(self, qs):
        """
        Filtros da query baseado no datatable
        """
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            search_parts = sSearch.split('+')
            qs_params = None
            for part in search_parts:
                q = Q(pergunta__istartswith=part)
                qs_params = qs_params | q if qs_params else q

            qs = qs.filter(qs_params)

        qs = qs.filter(Q(filial__id__in=get_filiais(self.request.user.id))|Q(filial__isnull=True))
        return qs

class QuestaoCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm, CoreMixinPassRequestForm):
    """
    Formulário de criação de questoes
    """
    model = Questao
    template_name = 'questao_form.html'
    success_url = '/'
    form_class= QuestaoForm

class QuestaoUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm, CoreMixinPassRequestForm):
    """
    Formulário de criação de questoes
    """
    model = Questao
    template_name = 'questao_form.html'
    success_url = '/'
    form_class= QuestaoForm

class QuestaoDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Questao
    success_url = '/oportunidade/questoes/'