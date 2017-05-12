# -*- coding: utf-8 -*- 
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.db.models import Avg, Q
from django.views.decorators.clickjacking import xframe_options_exempt
from django.template import RequestContext

from rest_framework import generics
from rest_framework import permissions
from rest_framework import filters
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import detail_route, list_route, api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoModelPermissions
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import authentication
from rest_framework.reverse import reverse as rest_reverse

from verifica_news import serializers
from verifica_news import models

import requests, json
import datetime
import locale

class NewsAPIViewSet(viewsets.ModelViewSet):
    queryset = models.AppEntry.objects.all()
    serializer_class = serializers.AppEntryListSerializer
    renderer_classes = (renderers.JSONRenderer,)
    def list(self, request):
        params = request.GET
        if 'breaking' in params:
            breaking = True
        else:
            breaking = False
        if 'platform' in params:
            platform = params.get('platform')
        else:
            platform = ''
        if breaking:
            news = [models.AppEntry.objects.latest('id')]
            if platform == 'ios':
                news = [models.AppEntry.objects.filter(platform_ios=True).latest('id')]
            if platform == 'android':
                news = [models.AppEntry.objects.filter(platform_android=True).latest('id')]
        else:
            if platform == 'ios':
                news = models.AppEntry.objects.filter(platform_ios=True)
            elif platform == 'android':
                news = models.AppEntry.objects.filter(platform_android=True)
            else:
                news = models.AppEntry.objects.all()
        serializer = serializers.AppEntryListSerializer(news, many=True)
        return Response(serializer.data)
