from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter, SimpleRouter

from verifica import views, oauth_views
from verifica import interesse_views
from servicios import views as servicios_views

# Create a router and register our viewsets with it.
# router = DefaultRouter()
router = SimpleRouter()
router.register(r'clients', views.ClientViewSet)
router.register(r'vehiculos', views.VehiculoViewSet)
router.register(r'aseguradoras', views.AseguradoraViewSet)
router.register(r'versiones', views.AppVersionViewSet)
router.register(r'cotizaciones', views.CotizadorViewSet)
router.register(r'servicios', servicios_views.ServicioViewSet)
router.register(r'tarifas', views.TarifaViewSet)

oa_router = DefaultRouter()
# oa_router = SimpleRouter()
oa_router.register(r'clients', oauth_views.ClientViewSet)
oa_router.register(r'vehiculos', oauth_views.VehiculoViewSet)
oa_router.register(r'aseguradoras', oauth_views.AseguradoraViewSet)
oa_router.register(r'versiones', oauth_views.AppVersionViewSet)
oa_router.register(r'cotizaciones', oauth_views.CotizadorViewSet)
# oa_router.register(r'servicios', servicios_views.ServicioViewSet)
oa_router.register(r'tarifas', oauth_views.TarifaViewSet)
oa_router.register(r'devices', oauth_views.DeviceViewSet)

oauth_urls = [
    url(r'^v2/poliza_status/$', interesse_views.PolizaStatusView.as_view()),
    url(r'^v2/imecas/$', oauth_views.ImecasView.as_view()),
    url(r'^v2/placa/$', oauth_views.PlacaDetectorView.as_view()),
    url(r'^v2/verificacion/$', oauth_views.VerificacionView.as_view()),
    url(r'^v2/multas/$', oauth_views.MultaParserView.as_view()),
    url(r'^v2/cotizador/$', oauth_views.CotizadorView.as_view()),
    url(r'^v2/config/$', oauth_views.ConfigView.as_view()),
    url(r'^v2/feriados/$', oauth_views.FeriadosView.as_view()),
    url(r'^v2/contingencia/$', oauth_views.ContingenciaView.as_view()),
    url(r'^v2/programa/$', oauth_views.ProgramaView.as_view()),
    url(r'^v2/', include(oa_router.urls)),
]

urlpatterns = [
    url(r'^v1/poliza_status/$', interesse_views.PolizaStatusView.as_view()),
    url(r'^v1/imecas/$', views.ImecasView.as_view()),
    url(r'^v1/verificacion/$', views.VerificacionView.as_view()),
    url(r'^v1/multas/$', views.MultaParserView.as_view()),
    url(r'^v1/cotizador/$', views.CotizadorView.as_view()),
    url(r'^v1/config/$', views.ConfigView.as_view()),
    url(r'^v1/feriados/$', views.FeriadosView.as_view()),
    url(r'^v1/contingencia/$', views.ContingenciaView.as_view()),
    url(r'^v1/programa/$', views.ProgramaView.as_view()),
    url(r'^v1/', include(router.urls)),
]+oauth_urls
