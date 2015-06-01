from django.conf.urls import patterns, include, url

from tsm.cliente.views.carteira import *
from tsm.cliente.views.cliente import *
from tsm.cliente.views.produto import *
from tsm.cliente.views.fabricante import *
from tsm.cliente.views.contato import *
from tsm.cliente.views.segmento import *
from tsm.cliente.views.core import ClienteMenu

urlpatterns = patterns('',
    #Carteira
    url(r'^carteiras/data/$', CarteiraData.as_view(),name='cliente.list_json_carteira'),
    url(r'^carteiras/formulario/$', CarteiraCreateForm.as_view(),name='cliente.add_carteira'),
    url(r'^carteiras/(?P<pk>\d+)/$', CarteiraUpdateForm.as_view(),name='cliente.change_carteira'),
    url(r'^carteiras/remove/(?P<pk>\d+)/$', CarteiraDelete.as_view(),name='cliente.delete_carteira'),
    url(r'^carteiras/$', CarteiraList.as_view(), name='cliente.list_carteira'),

    #Clientes
    url(r'^clientes/data/$', ClienteData.as_view(),name='cliente.list_json_cliente'),
    url(r'^clientes/formulario/min/$', ClienteCreateFormMin.as_view(),name='cliente.add_cliente_min'),
    url(r'^clientes/formulario/$', ClienteCreateForm.as_view(),name='cliente.add_cliente'),
    url(r'^clientes/(?P<pk>\d+)/$', ClienteUpdateForm.as_view(),name='cliente.change_cliente'),
    url(r'^clientes/remove/(?P<pk>\d+)/$', ClienteDelete.as_view(),name='cliente.delete_cliente'),
    url(r'^clientes/$', ClienteList.as_view(), name='cliente.list_cliente'),

    #Produtos
    url(r'^produtos/data/$', ProdutoData.as_view(),name='cliente.list_json_produto'),
    url(r'^produtos/formulario/$', ProdutoCreateForm.as_view(),name='cliente.add_produto'),
    url(r'^produtos/(?P<pk>\d+)/$', ProdutoUpdateForm.as_view(),name='cliente.change_produto'),
    url(r'^produtos/remove/(?P<pk>\d+)/$', ProdutoDelete.as_view(),name='cliente.delete_produto'),
    url(r'^produtos/$', ProdutoList.as_view(), name='cliente.list_produto'),

    #Fabricantes
    url(r'^fabricantes/data/$', FabricanteData.as_view(),name='cliente.list_json_fabricante'),
    url(r'^fabricantes/formulario/$', FabricanteCreateForm.as_view(),name='cliente.add_fabricante'),
    url(r'^fabricantes/(?P<pk>\d+)/$', FabricanteUpdateForm.as_view(),name='cliente.change_fabricante'),
    url(r'^fabricantes/remove/(?P<pk>\d+)/$', FabricanteDelete.as_view(),name='cliente.delete_fabricante'),
    url(r'^fabricantes/$', FabricanteList.as_view(), name='cliente.list_fabricante'),

    #Contatos
    url(r'^contatos/data/$', ContatoData.as_view(),name='cliente.list_json_contato'),
    url(r'^contatos/formulario/$', ContatoCreateForm.as_view(),name='cliente.add_contato'),
    url(r'^contatos/(?P<pk>\d+)/$', ContatoUpdateForm.as_view(),name='cliente.change_contato'),
    url(r'^contatos/remove/(?P<pk>\d+)/$', ContatoDelete.as_view(),name='cliente.delete_contato'),
    url(r'^contatos/$', ContatoList.as_view(), name='cliente.list_contato'),

    #Segmentos
    url(r'^segmentos/data/$', SegmentoData.as_view(),name='cliente.list_json_segmento'),
    url(r'^segmentos/formulario/$', SegmentoCreateForm.as_view(),name='cliente.add_segmento'),
    url(r'^segmentos/(?P<pk>\d+)/$', SegmentoUpdateForm.as_view(),name='cliente.change_segmento'),
    url(r'^segmentos/remove/(?P<pk>\d+)/$', SegmentoDelete.as_view(),name='cliente.delete_segmento'),
    url(r'^segmentos/$', SegmentoList.as_view(), name='cliente.list_segmento'),

    #menu
    url(r'^$', ClienteMenu.as_view(),name='cliente.cliente_menu'),
)