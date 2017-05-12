from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from verifica import models as verifica_models
from dashboard import models
# from chartit import DataPool, Chart

# Create your views here.
# class IndexView(generic.ListView):
#     template_name = 'dashboard/home.html'
#     context_object_name = 'client_list'
# 
#     def get_queryset(self):
#         """Return the last five published questions."""
#         return verifica_models.Client.objects.all()[:10]        
    
# def home(request):
#     ds = DataPool(
#            series=
#             [{'options': {
#                 'source': models.DailyActiveUser.objects.all()},
#               'terms': [
#                 'timestamp',
#                 'number_of_users']}
#              ])
#     cht = Chart(
#             datasource = ds, 
#             series_options = 
#               [{'options':{
#                   'type': 'line',
#                   'stacking': False},
#                 'terms':{
#                   'timestamp': [
#                     'number_of_users']
#                   }}],
#             chart_options = 
#               {'title': {
#                    'text': 'Active Users'},
#                'xAxis': {
#                     'title': {
#                        'text': 'Day'}}})
#     return render_to_response('charts/index.html', {'chart_list': cht})