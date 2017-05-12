from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout, password_change, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.views.generic import RedirectView
from verifica_news import views

router = SimpleRouter()
router.register(r'news', views.NewsAPIViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
