from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.conf import settings
from edu import views
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

   (r'^$', "edu.views.index"),
   (r'^login/', "django.contrib.auth.views.login", { "template_name": "login.html" }),
   (r'^logout/', "django.contrib.auth.views.logout_then_login", {'login_url': '/login/'}),

   #(r'^gerar_codigo/', "edu.views.gerar_codigo"),
   (r'^resgatar_codigo/', "edu.views.resgatar_codigo"),
   (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
   (r'^cadastrar_aluno/', "edu.views.cadastrar_aluno"),
   (r'^ranking/', "edu.views.ranking_view"),
   (r'^turma/(?P<nome_colegio>\w+)/$', 'edu.views.get_turmas'),

    # Examples:
    # url(r'^$', 'InovEdu.views.home', name='home'),
    # url(r'^InovEdu/', include('InovEdu.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

