from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from rest_framework import viewsets, routers
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework import permissions
from rest_framework import serializers
from rest_framework import generics

from verifica import views
from verifica import interesse_views
from verifica.models import Client

from axes.decorators import watch_login
from django.contrib.auth.views import login, logout, password_change
from django.views.i18n import javascript_catalog

from dashboard import views as dashboard_views

from servicios import views as servicios_views
from drivemee import views as drivemee_views

admin.autodiscover()

js_info_dict = {
    'packages': ('django.conf',),
}

##start auth
class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.email=validated_data['username']
        user.set_password(validated_data['password'])
        user.save()
        return user
    class Meta:
        model = User
        fields = ('username', 'password')

class IsAuthenticatedOrCreate(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super(IsAuthenticatedOrCreate, self).has_permission(request, view)

class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (IsAuthenticatedOrCreate,)

##end auth


# Create a router and register our viewsets with it.
router = DefaultRouter()
# router = SimpleRouter()
router.register(r'clients', views.ClientViewSet)
router.register(r'vehiculos', views.VehiculoViewSet)
router.register(r'aseguradoras', views.AseguradoraViewSet)
router.register(r'versiones', views.AppVersionViewSet)
router.register(r'cotizaciones', views.CotizadorViewSet)
router.register(r'servicios', servicios_views.ServicioViewSet)
router.register(r'tarifas', views.TarifaViewSet)

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url(r'^accounts/login/$', login),
    url(r'^jsi18n$', javascript_catalog, js_info_dict),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^poliza_status/$', interesse_views.PolizaStatusView.as_view()),
    url(r'^imecas/$', views.ImecasView.as_view()),
    url(r'^verificacion/$', views.VerificacionView.as_view()),
    url(r'^multas/$', views.MultaParserView.as_view()),
    url(r'^cotizador/$', views.CotizadorView.as_view()),
    url(r'^config/$', views.ConfigView.as_view()),
    url(r'^feriados/$', views.FeriadosView.as_view()),
    url(r'^', include(router.urls)),
    url(r'^api/auth/', include('djoser.urls')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^sign_up/$', SignUpView.as_view(), name="sign_up"),
    url(r'^login/$', watch_login(login), {'template_name': 'auth/login.html'}),
    url(r'^selectable/', include('selectable.urls')),
    url(r'^drivemee/', include('drivemee.urls', namespace='drivemee')),
    url(r'^verifica/', include('verifica.urls', namespace='verifica')),
    url(r'^news/', include('verifica_news.urls', namespace='news')),
]