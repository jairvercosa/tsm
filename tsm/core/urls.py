from django.conf.urls import patterns, include, url

from views.index import Index
from views.configuracoes import Configuracoes, Cadastros, Historico

from views.parametros import *
from views.feriado import *
from views.filiais import *

urlpatterns = patterns('',
    url(r'^configuracoes/', Configuracoes.as_view(), name='core.core_configurations'),
    url(r'^historico/', Historico.as_view(), name='core.core_historico'),
    url(r'^$', Index.as_view(), name='core_index'),

    #Cadastros basicos
    url(r'^cadastros/', Cadastros.as_view(), name='cadastros_basicos'),

    #Parametros
    url(r'^parametros/data/$', ParametrosData.as_view(),name='core.list_json_parametro'),
    url(r'^parametros/formulario/$', ParametrosCreateForm.as_view(),name='core.add_parametro'),
    url(r'^parametros/(?P<pk>\d+)/$', ParametrosUpdateForm.as_view(),name='core.change_parametro'),
    url(r'^parametros/remove/(?P<pk>\d+)/$', ParametrosDelete.as_view(),name='core.delete_parametro'),
    url(r'^parametros/$', ParametrosList.as_view(), name='core.list_parametros'),

    #Feriados
    url(r'^feriados/data/$', FeriadoData.as_view(),name='core.list_json_feriado'),
    url(r'^feriados/formulario/$', FeriadoCreateForm.as_view(),name='core.add_feriado'),
    url(r'^feriados/(?P<pk>\d+)/$', FeriadoUpdateForm.as_view(),name='core.change_feriado'),
    url(r'^feriados/remove/(?P<pk>\d+)/$', FeriadoDelete.as_view(),name='core.delete_feriado'),
    url(r'^feriados/$', FeriadoList.as_view(), name='core.list_feriados'),

    #Filiais
    url(r'^filiais/data/$', FiliaisData.as_view(),name='core.list_json_filial'),
    url(r'^filiais/formulario/$', FiliaisCreateForm.as_view(),name='core.add_filial'),
    url(r'^filiais/(?P<pk>\d+)/$', FiliaisUpdateForm.as_view(),name='core.change_filial'),
    url(r'^filiais/remove/(?P<pk>\d+)/$', FiliaisDelete.as_view(),name='core.delete_filial'),
    url(r'^filiais/$', FiliaisList.as_view(), name='core.list_filial'),
)
