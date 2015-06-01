from django.conf.urls import patterns, include, url

from tsm.relatorio.views.core import RelatorioMenu
from tsm.relatorio.views.rtc import *

urlpatterns = patterns('',
    
    #oportunidade - rtc gerencial
    url(r'^oportunidade/rtcgerencial/$', RtcGerencial.as_view(),name='oportunidade.rtc_gerencial'),
    url(r'^oportunidade/rtcgerencial/header/$', RtcHeader.as_view(),name='oportunidade.rtc_gerencial_header'),
    url(r'^oportunidade/rtcgerencial/data/$', RtcData.as_view(),name='oportunidade.rtc_gerencial_json_data'),

    #menu
    url(r'^$', RelatorioMenu.as_view(),name='relatorio.relatorio_menu'),
)