# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q

from tsm.core.util import get_filiais
from tsm.core.mixins.core_mixin_base import CoreMixinDispatch
from tsm.core.base.core_base_datatable import CoreBaseDatatableView
from tsm.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel, CoreMixinPassRequestForm
from tsm.core.mixins.core_mixin_login import CoreMixinLoginRequired
from tsm.equipe.models.tipometa import TipoMeta
from tsm.equipe.forms.tipometaform import TipoMetaForm

class TpMetaList(CoreMixinLoginRequired, TemplateView, CoreMixinDispatch):
    """
    View para renderização da lista de tipo_metas
    """
    template_name = 'tipo_meta_list.html'
    
class TpMetaData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista de tipo_metas
    """
    model = TipoMeta
    columns = ['id','nome','buttons']
    order_columns = ['id','nome']
    max_display_length = 500
    url_base_form = '/equipe/tipometa/'
    
    def filter_queryset(self, qs):
        """
        Filtros da query baseado no datatable
        """
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            search_parts = sSearch.split('+')
            qs_params = None
            for part in search_parts:
                q = Q(nome__istartswith=part)
                qs_params = qs_params | q if qs_params else q

            qs = qs.filter(qs_params)

        qs = qs.filter(filial__id__in=get_filiais(self.request.user.id))
        return qs

class TpMetaCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm, CoreMixinPassRequestForm):
    """
    Formulário de criação de tipo_metas
    """
    model = TipoMeta
    template_name = 'tipo_meta_form.html'
    success_url = '/'
    form_class = TipoMetaForm

class TpMetaUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm, CoreMixinPassRequestForm):
    """
    Formulário de criação de tipo_metas
    """
    model = TipoMeta
    template_name = 'tipo_meta_form.html'
    success_url = '/'
    form_class = TipoMetaForm

class TpMetaDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = TipoMeta
    success_url = '/equipe/tipometa/'