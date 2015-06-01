from django.conf.urls import patterns, include, url

from tsm.oportunidade.views.situacao import *
from tsm.oportunidade.views.tipotemperatura import *
from tsm.oportunidade.views.receita import *
from tsm.oportunidade.views.origem import *
from tsm.oportunidade.views.questao import *
from tsm.oportunidade.views.oportunidade import *
from tsm.oportunidade.views.visaogerencial import *
from tsm.oportunidade.views.core import OportunidadeMenu
from tsm.oportunidade.views.historico import *
from tsm.oportunidade.views.dashboard import *
from tsm.oportunidade.views.rtc import *

urlpatterns = patterns('',
    
    #Situcacao
    url(r'^situacao/data/$', SituacaoData.as_view(),name='oportunidade.list_json_situacao'),
    url(r'^situacao/formulario/$', SituacaoCreateForm.as_view(),name='oportunidade.add_situacao'),
    url(r'^situacao/(?P<pk>\d+)/$', SituacaoUpdateForm.as_view(),name='oportunidade.change_situacao'),
    url(r'^situacao/remove/(?P<pk>\d+)/$', SituacaoDelete.as_view(),name='oportunidade.delete_situacao'),
    url(r'^situacao/$', SituacaoList.as_view(), name='oportunidade.list_situacao'),

    #Tipo Temperatura
    url(r'^tipotemperatura/data/$', TpTemperaturaData.as_view(),name='oportunidade.list_json_tipotemperatura'),
    url(r'^tipotemperatura/formulario/$', TpTemperaturaCreateForm.as_view(),name='oportunidade.add_tipotemperatura'),
    url(r'^tipotemperatura/(?P<pk>\d+)/$', TpTemperaturaUpdateForm.as_view(),name='oportunidade.change_tipotemperatura'),
    url(r'^tipotemperatura/remove/(?P<pk>\d+)/$', TpTemperaturaDelete.as_view(),name='oportunidade.delete_tipotemperatura'),
    url(r'^tipotemperatura/$', TpTemperaturaList.as_view(), name='oportunidade.list_tipotemperatura'),

    #Receita
    url(r'^receita/data/$', ReceitaData.as_view(),name='oportunidade.list_json_receita'),
    url(r'^receita/formulario/$', ReceitaCreateForm.as_view(),name='oportunidade.add_receita'),
    url(r'^receita/(?P<pk>\d+)/$', ReceitaUpdateForm.as_view(),name='oportunidade.change_receita'),
    url(r'^receita/remove/(?P<pk>\d+)/$', ReceitaDelete.as_view(),name='oportunidade.delete_receita'),
    url(r'^receita/$', ReceitaList.as_view(), name='oportunidade.list_receita'),

    #Origem
    url(r'^origem/data/$', OrigemData.as_view(),name='oportunidade.list_json_origem'),
    url(r'^origem/formulario/$', OrigemCreateForm.as_view(),name='oportunidade.add_origem'),
    url(r'^origem/(?P<pk>\d+)/$', OrigemUpdateForm.as_view(),name='oportunidade.change_origem'),
    url(r'^origem/remove/(?P<pk>\d+)/$', OrigemDelete.as_view(),name='oportunidade.delete_origem'),
    url(r'^origem/$', OrigemList.as_view(), name='oportunidade.list_origem'),

    #Questoes
    url(r'^questoes/data/$', QuestaoData.as_view(),name='oportunidade.list_json_questao'),
    url(r'^questoes/formulario/$', QuestaoCreateForm.as_view(),name='oportunidade.add_questao'),
    url(r'^questoes/(?P<pk>\d+)/$', QuestaoUpdateForm.as_view(),name='oportunidade.change_questao'),
    url(r'^questoes/remove/(?P<pk>\d+)/$', QuestaoDelete.as_view(),name='oportunidade.delete_questao'),
    url(r'^questoes/$', QuestaoList.as_view(), name='oportunidade.list_questao'),

    #RTC
    url(r'^rtc/$', RtcAgenda.as_view(),name='oportunidade.agenda_rtc'),
    url(r'^rtc/data/$', RtcAgendaData.as_view(),name='oportunidade.agenda_rtc_data'),
    url(r'^rtc/evento/(?P<pk>\d+)/$', RtcMinView.as_view(),name='oportunidade.report_rtc_evento'),
    url(r'^lista/(?P<op>\d+)/rtc/data/$', RtcData.as_view(),name='oportunidade.list_json_rtc'),
    url(r'^lista/(?P<op>\d+)/rtc/formulario/$', RtcCreateForm.as_view(),name='oportunidade.add_rtc'),
    url(r'^lista/(?P<op>\d+)/rtc/(?P<pk>\d+)/$', RtcUpdateForm.as_view(),name='oportunidade.change_rtc'),
    url(r'^lista/(?P<op>\d+)/rtc/remove/(?P<pk>\d+)/$', RtcDelete.as_view(),name='oportunidade.delete_rtc'),
    url(r'^lista/(?P<op>\d+)/rtc/$', RtcList.as_view(), name='oportunidade.list_rtc'),

    #Oportunidade
    url(r'^calculatemp/$', OportunidadeTemperatura.as_view(),name='oportunidade.calc_temperatura'),
    url(r'^formulario/$', OportunidadeCreateForm.as_view(),name='oportunidade.add_oportunidade'),
    url(r'^formulario/getlider/(?P<pk>\d+)/$', OportunidadeGetLider.as_view(),name='oportunidade.get_lider_oportunidade'),
    url(r'^remove/(?P<pk>\d+)/$', OportunidadeDelete.as_view(),name='oportunidade.delete_oportunidade'),
    url(r'^lista/(?P<pk>\d+)/$', OportunidadeUpdateForm.as_view(),name='oportunidade.change_oportunidade'),
    url(r'^lista/edicaorapida/(?P<pk>\d+)/$', OportunidadeFastUpdate.as_view(),name='oportunidade.change_fast_oportunidade'),
    url(r'^lista/ckeck/(?P<pk>\d+)/$', OportunidadeCheck.as_view(),name='oportunidade.can_change_mw_bc'),
    url(r'^lista/data/$', OportunidadeData.as_view(),name='oportunidade.list_json_oportunidade'),
    url(r'^lista/$', OportunidadeList.as_view(), name='oportunidade.list_oportunidade'),

    #Visao Gerencial
    url(r'^visaogerencial/indicadores/(?P<pk>\d+)/$', VisaoGerencialIndicador.as_view(),name='oportunidade.list_indicador'),
    url(r'^visaogerencial/indicadorestop/$', VisaoGerencialIndicadorTop.as_view(),name='oportunidade.list_indicador_top'),
    url(r'^visaogerencial/data/$', VisaoGerencialData.as_view(),name='oportunidade.list_json_visaogerencial'),
    url(r'^visaogerencial/$', VisaoGerencial.as_view(),name='oportunidade.list_visaogerencial'),    

    #Historico
    url(r'^historico/data/$', HistoricoData.as_view(),name='oportunidade.list_json_historico'),
    url(r'^historico/(?P<pk>\d+)/$', HistoricoVisao.as_view(),name='oportunidade.view_historico'),
    url(r'^historico/$', HistoricoList.as_view(),name='oportunidade.list_historico'),

    #Dashboard
    url(r'^dashboard/$', DashboardIndex.as_view(),name='oportunidade.index_dashboard'),    
    url(r'^dashboard/data/$', DashboardGetData.as_view(),name='oportunidade.json_data_dashboard'),

    #menu
    url(r'^$', OportunidadeMenu.as_view(),name='oportunidade.oportunidade_menu'),
)