from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter, SimpleRouter
from drivemee import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout, password_change

router = DefaultRouter()
router.register(r'valet', views.SolicitudAPIViewSet)
router.register(r'tarifas', views.TarifasAPIViewSet)
router.register(r'cupones', views.CuponesAPIViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/evaluaciones/$', views.EvaluacionesView.as_view()),
    url(r'^login/$', login, {'template_name':'registration/drivemee-login.html'}, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^$', views.index, name='index'),
    url(r'^solicitudes/$', login_required(views.SolicitudIndexView.as_view()), name='solicitudes'),
    url(r'^solicitudes/(?P<status>\w+)/$', login_required(views.SolicitudIndexView.as_view()), name='solicitudes'),
    url(r'^solicitud/create/$', views.SolicitudCreateModal.as_view(), name='solicitud-create'),
    url(r'^solicitud/(?P<pk>[0-9]+)/$', login_required(views.SolicitudDetailView.as_view()), name='solicitud-detail'),
    url(r'^solicitud/(?P<pk>[0-9]+)/editar/$', views.SolicitudClientUpdateModal.as_view(), name='solicitud-edit-client'),
    url(r'^solicitud/(?P<pk>[0-9]+)/cancel/$', views.SolicitudCancelModal.as_view(), name='solicitud-cancel'),
    url(r'^solicitud/(?P<pk>[0-9]+)/schedule/$', views.SolicitudScheduleModal.as_view(), name='solicitud-schedule'),
#     url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
#     url(r'^solicitud/(?P<pk>[0-9]+)/editar/$', views.editar, name='editar'),
#     url(r'^solicitudes/add/$', views.SolicitudCreate.as_view(), name='solicitud_add'),
#     url(r'^solicitud/(?P<pk>[0-9]+)/$', views.SolicitudUpdate.as_view(), name='solicitud_update'),
    url(r'^solicitud/(?P<pk>[0-9]+)/delete/$', views.cancel_solicitud, name='confirm-cancel-solicitud'),
]
