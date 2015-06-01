from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('tsm.core.urls'),name="App-Principal"),

    url(r'^core/', include('tsm.core.urls')),
    url(r'^acesso/', include('tsm.acesso.urls')),
    url(r'^oportunidade/', include('tsm.oportunidade.urls')),
    url(r'^cliente/', include('tsm.cliente.urls')),
    url(r'^equipe/', include('tsm.equipe.urls')),
    url(r'^relatorio/', include('tsm.relatorio.urls')),
    # Examples:
    # url(r'^$', 'tsm.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
)

handler403 = 'tsm.core.views.core.error403'
handler404 = 'tsm.core.views.core.error404'
handler500 = 'tsm.core.views.core.error500'