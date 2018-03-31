from django.shortcuts import render
from django.http import HttpRequest
from django.template import loader
from django.http import HttpResponse


# Create your views here.
def hello(request):
    template = loader.get_template('index.html')
    context = {'msg': 'App is ok'}
    return HttpResponse(template.render(context, request))
