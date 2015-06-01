from django.conf.urls import patterns, include, url

from tsm.equipe.views.tipometa import TpMetaList, TpMetaData, TpMetaCreateForm, TpMetaUpdateForm, TpMetaDelete
from tsm.equipe.views.equipe import *
from tsm.equipe.views.membrometa import *
from tsm.equipe.views.historico import *

urlpatterns = patterns('',
    
    #Tipo Meta
    url(r'^tipometa/data/$', TpMetaData.as_view(),name='equipe.list_json_tipometa'),
    url(r'^tipometa/formulario/$', TpMetaCreateForm.as_view(),name='equipe.add_tipometa'),
    url(r'^tipometa/(?P<pk>\d+)/$', TpMetaUpdateForm.as_view(),name='equipe.change_tipometa'),
    url(r'^tipometa/remove/(?P<pk>\d+)/$', TpMetaDelete.as_view(),name='equipe.delete_tipometa'),
    url(r'^tipometa/$', TpMetaList.as_view(), name='equipe.list_tipometa'),

    #Membro
    url(r'^membro/metas/valida/(?P<pk>\d+)/$', MembroMetaValida.as_view(), name='equipe.valida_membrometa'),
    url(r'^membro/metas/formulario/$', MembroMetaForm.as_view(), name='equipe.add_membrometa'),
    url(r'^membro/metas/visivel/(?P<pk>\d+)/$', MembroMetaVisible.as_view(), name='equipe.change_membrometa'),
    url(r'^membro/metas/remove/(?P<pk>\d+)/$', MembroMetaDelete.as_view(), name='equipe.delete_membrometa'),
    url(r'^membro/metas/(?P<pk>\d+)/$', MembroMetaList.as_view(), name='equipe.list_membrometa'),

    #Equipe
    url(r'^membro/(?P<pk>\d+)/$', EquipeMembroChange.as_view(), name='equipe.change_membro'),
    url(r'^membro/getchild/$', EquipeGetChild.as_view(), name='equipe.list_json_membros_by_id'),
    url(r'^addmembro/$', EquipeMembroAdd.as_view(), name='equipe.add_membro'),
    url(r'^delmembro/(?P<pk>\d+)/$', EquipeMembroDel.as_view(), name='equipe.delete_membro'),
    url(r'^getstaff/$', EquipeStaffGet.as_view(), name='equipe.list_staff'),
    url(r'^getmembros/$', EquipeMembrosGet.as_view(), name='equipe.list_membros'),
    url(r'^$', EquipeEstrutura.as_view(), name='equipe.list_equipe'),    

    #Historico
    url(r'^membro/historico/(?P<pk>\d+)/$', MembroHistoricoVisao.as_view(), name='equipe.view_membrohistorico'),
    url(r'^membro/historico/data/$', MembroHistoricoData.as_view(), name='equipe.list_json_membrohistorico'),
    url(r'^membro/historico/$', MembroHistoricoList.as_view(), name='equipe.list_membrohistorico'),

    url(r'^membro/meta/historico/(?P<pk>\d+)/$', MembroMetaHistoricoVisao.as_view(), name='equipe.view_membrometahistorico'),
    url(r'^membro/meta/historico/data/$', MembroMetaHistoricoData.as_view(), name='equipe.list_json_membrometahistorico'),
    url(r'^membro/meta/historico/$', MembroMetaHistoricoList.as_view(), name='equipe.list_membrometahistorico'),
)