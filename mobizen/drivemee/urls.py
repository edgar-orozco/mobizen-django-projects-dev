from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter, SimpleRouter
from drivemee import views, frontend_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout, password_change, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.views.generic import RedirectView

router = DefaultRouter()
router.register(r'valet', views.SolicitudAPIViewSet)
router.register(r'tarifas', views.TarifasAPIViewSet)
router.register(r'costos', views.CostosAPIViewSet)
router.register(r'cupones', views.CuponesAPIViewSet)

frontend_patterns = [
    url(r'^public/aviso-privacidad$', frontend_views.aviso_privacidad, name='aviso-privacidad'),
    url(r'^public/solicitar-servicio$', frontend_views.create_solicitud, name='crear-solicitud'),
    url(r'^public/confirmar-solicitud/(?P<token>[0-9A-Za-z_\-=/]+)/$', frontend_views.thanks_solicitud, name='confirmar-solicitud'),
    url(r'^public/confirmar-servicio/(?P<token>[0-9A-Za-z_\-=/]+)/$', frontend_views.confirm_solicitud, name='confirmar-servicio'),
    url(r'^verifica/solicitar-servicio$', frontend_views.create_solicitud_verifica, name='verifica-crear-solicitud'),
    url(r'^verifica/confirmar-solicitud/(?P<token>[0-9A-Za-z_\-=/]+)/$', frontend_views.thanks_solicitud_verifica, name='verifica-confirmar-solicitud'),
#     url(r'^operadores/search/$', login_required(views.SolicitudSearchView), name='operador-search'),
#     url(r'^operadores/(?P<status>\w+)/$', views.SolicitudIndexView.as_view(), name='operadores'),
#     url(r'^operador/create/$', views.OperadorCreateModal.as_view(), name='operador-create'),
#     url(r'^operador/(?P<pk>[0-9]+)/$', views.OperadorDetailView.as_view(), name='operador-detail'),
#     url(r'^operador/(?P<pk>[0-9]+)/edit/$', views.OperadorUpdateModal.as_view(), name='operador-edit'),
#     url(r'^operador/(?P<pk>[0-9]+)/delete/$', views.OperadorDeleteModal.as_view(), name='operador-delete'),
]

operador_patterns = [
    url(r'^operadores/$', views.OperadorListView.as_view(), name='operadores'),
    url(r'^operadores/search/$', login_required(views.SolicitudSearchView), name='operador-search'),
    url(r'^operadores/(?P<status>\w+)/$', views.SolicitudIndexView.as_view(), name='operadores'),
    url(r'^operador/create/$', views.OperadorCreateModal.as_view(), name='operador-create'),
    url(r'^operador/(?P<pk>[0-9]+)/$', views.OperadorDetailView.as_view(), name='operador-detail'),
    url(r'^operador/(?P<pk>[0-9]+)/edit/$', views.OperadorUpdateModal.as_view(), name='operador-edit'),
    url(r'^operador/(?P<pk>[0-9]+)/delete/$', views.OperadorDeleteModal.as_view(), name='operador-delete'),
]

solicitud_patterns = [
    url(r'^solicitudes/$', RedirectView.as_view(pattern_name='drivemee:index')),
    url(r'^solicitudes/(?P<source>\w+)/(?P<status>\w+)/$', views.SolicitudIndexView.as_view(), name='solicitudes'),
    url(r'^solicitudes/(?P<source>\w+)/(?P<status>\w+)/(?P<pk>[0-9]+)/$', login_required(views.SolicitudDetailView.as_view()), name='solicitud-detail'),
    url(r'^solicitudes/search/$', login_required(views.SolicitudSearchView), name='solicitud-search'),
#     url(r'^solicitudes/(?:(?P<source>\w+)/)?$', views.SolicitudIndexView.as_view(), name='solicitudes'),
#     url(r'^solicitudes/(?P<source>\w+)/(?P<status>\w+)/(?P<pk>[0-9]+)/$', login_required(views.SolicitudDetailView.as_view()), name='solicitud-detail'),
#     url(r'^solicitudes-agencia/$', views.SolicitudAgenciaIndexView.as_view(), name='solicitudes-agencia'),
#     url(r'^solicitudes/(?P<source>\w+)/(?P<status>\w+)/(?P<pk>[0-9]+)/$', login_required(views.SolicitudDetailView.as_view()), name='solicitud-detail'),
#     url(r'^solicitudes/(?P<source>\w+)/$', views.SolicitudIndexView.as_view(), name='solicitudes'),
#     url(r'^solicitudes/(?P<status>\w+)/$', views.SolicitudIndexView.as_view(), name='solicitudes'),
#     url(r'^solicitudes-agencia/(?P<status>\w+)/$', views.SolicitudAgenciaIndexView.as_view(), name='solicitudes-agencia'),
    url(r'^solicitud/create/$', views.SolicitudCreateModal.as_view(), name='solicitud-create'),
    url(r'^solicitud/(?P<pk>[0-9]+)/$', RedirectView.as_view(pattern_name='drivemee:index')),
    url(r'^solicitud/(?P<source>\w+)/(?P<status>\w+)/(?P<pk>[0-9]+)/editar/$', views.SolicitudClientUpdateModal.as_view(), name='solicitud-edit-client'),
    url(r'^solicitud/(?P<source>\w+)/(?P<status>\w+)/(?P<pk>[0-9]+)/cancel/$', views.SolicitudCancelModal.as_view(), name='solicitud-cancel'),
    url(r'^solicitud/(?P<source>\w+)/(?P<status>\w+)/(?P<pk>[0-9]+)/schedule/$', views.SolicitudScheduleModal.as_view(), name='solicitud-schedule'),
    url(r'^solicitud/(?P<source>\w+)/(?P<status>\w+)/(?P<pk>[0-9]+)/schedule_nopay/$', views.SolicitudScheduleNoPaymentModal.as_view(), name='solicitud-schedulenopay'),
    url(r'^solicitud/(?P<source>\w+)/(?P<status>\w+)/(?P<pk>[0-9]+)/reschedule/$', views.SolicitudRescheduleModal.as_view(), name='solicitud-reschedule'),
    url(r'^solicitud/(?P<source>\w+)/(?P<status>\w+)/(?P<pk>[0-9]+)/snooze/$', views.SolicitudSnoozeModal.as_view(), name='solicitud-snooze'),
    url(r'^solicitud/(?P<source>\w+)/(?P<status>\w+)/(?P<pk>[0-9]+)/notes/$', views.SolicitudNotesModal.as_view(), name='solicitud-notes'),
    url(r'^solicitud/(?P<source>\w+)/(?P<status>\w+)/(?P<pk>[0-9]+)/preagendar/$', views.SolicitudPreagendarModal.as_view(), name='solicitud-preagendar'),
    url(r'^solicitud/(?P<source>\w+)/(?P<status>\w+)/(?P<pk>[0-9]+)/verificar/$', views.SolicitudVerificarModal.as_view(), name='solicitud-verificar'),
    url(r'^solicitud/(?P<source>\w+)/(?P<status>\w+)/(?P<pk>[0-9]+)/cerrar/$', views.SolicitudCloseModal.as_view(), name='solicitud-cerrar'),
    url(r'^solicitud/(?P<source>\w+)/(?P<status>\w+)/(?P<pk>[0-9]+)/retirar/$', views.SolicitudRetirarModal.as_view(), name='solicitud-retirar'),
    url(r'^solicitud/(?P<source>\w+)/(?P<status>\w+)/(?P<pk>[0-9]+)/iniciar/$', views.SolicitudIniciarModal.as_view(), name='solicitud-iniciar'),
    url(r'^solicitud/(?P<source>\w+)/(?P<status>\w+)/(?P<pk>[0-9]+)/error-domicilio/$', views.SolicitudNagModal.as_view(), name='solicitud-error'),
    url(r'^solicitud/(?P<source>\w+)/(?P<status>\w+)/(?P<pk>[0-9]+)/domicilio-edit/(?P<domicilio>[0-9]+)/$', views.SolicitudDomicilioEditModal.as_view(), name='solicitud-domicilio-edit'),
    url(r'^solicitud/(?P<source>\w+)/(?P<status>\w+)/(?P<pk>[0-9]+)/domicilio/$', views.SolicitudDomicilioCreateModal.as_view(), name='solicitud-domicilio-create'),
    url(r'^solicitud/(?P<source>\w+)/(?P<status>\w+)/(?P<pk>[0-9]+)/operador/$', views.SolicitudSelectOperadorModal.as_view(), name='solicitud-operador'),
]

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/evaluaciones/$', views.EvaluacionesView.as_view()),
    url(r'^login/$', login, {'template_name':'registration/drivemee-login.html'}, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^password_reset/$', password_reset, {'post_reset_redirect':'drivemee:password_reset_done', 'template_name':'registration/drivemee-password_reset_form.html', 'email_template_name':'registration/drivemee-password_reset_email.html'}, name='password_reset'),
    url(r'^password_reset/done/$', password_reset_done, {'template_name':'registration/drivemee-password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, {'template_name':'registration/drivemee-password_reset_confirm.html','post_reset_redirect':'drivemee:password_reset_complete'}, name='password_reset_confirm'),
    url(r'^reset/done/$', password_reset_complete, {'template_name':'registration/drivemee-password_reset_complete.html'}, name='password_reset_complete'),
    url(r'^$', views.index, name='index'),
]+solicitud_patterns+operador_patterns+frontend_patterns
