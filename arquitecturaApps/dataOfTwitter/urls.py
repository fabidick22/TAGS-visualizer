from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^datos/(?P<key>[a-zA-Z0-9]+)/$', views.datosTwitter, name='dataview'),
    url(r'^datarealtime', views.viewRealTime, name='realtime'),
    url(r'^analisis/(?P<key2>[a-zA-Z0-9]+)/$', views.viewAnalisis, name='analisisDatos'),
    url(r'^estadisticas', views.viewEstadisticas, name='estadisticas'),
    url(r'^informacion', views.viewEstadisticas, name='informacionDatos'),
    url(r'^imagenes', views.viewImagenes, name='images'),
]
