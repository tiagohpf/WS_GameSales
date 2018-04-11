from django.shortcuts import render
from django.http import HttpRequest
from django.template import loader
from django.http import HttpResponse
from graphviz import Source

from consoleTypeRule import consoleTypeRule
from grafo import Grafo
from graphviz import Source
import re
import os

from mainRegionRule import mainRegionRule

# os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin'
os.environ["PATH"] += os.pathsep + '/usr/local/lib/python3.6/dist-packages/graphviz'

_graph = Grafo()
triples_platform = []


def triples2dot(triples):
    dot = \
        """ 
        graph "grafo" { 
        overlap = "scale"; 
        """
    for s, p, o in triples:
        dot = dot + ('%s -- %s [label=%s]\n' % (
            re.sub('[^A-Za-z0-9]+', '', s), re.sub('[^A-Za-z0-9]+', '', o), re.sub('[^A-Za-z0-9]+', '', p)))
    dot = dot + "}"
    return dot


# Create your views here.
def manage_file(request):
    context = {}
    if 'load_file' in request.POST and len(request.POST['load_file']) > 0:
        file = request.POST['load_file']
        _graph.load('clean_data/' + file)
    elif 'save_file' in request.POST:
        file = request.POST['save_file']
        if file:
            _graph.save('clean_data/' + file)
    else:
        context = {'save_error': False}
    return context


def file_status(request):
    context = manage_file(request)
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def list_all_tuples(request):
    context = manage_file(request)
    template = loader.get_template('all_tuples.html')
    context.update({
        'triples': _graph.triples(None, None, None)
    })
    return HttpResponse(template.render(context, request))


def check_games_list(request):
    context = manage_file(request)
    template = loader.get_template('games_list.html')
    triples = _graph.triples(None, 'Name', None)
    if 'download_graph' in request.POST:
        g = Source(triples2dot(triples), "games_list.gv.pdf", "dotout", "pdf", "neato")
        g.render(view=True)
        with open('dotout/games_list.gv.pdf', 'rb') as pdf:
            response = HttpResponse(pdf.read())
            response['content_type'] = 'application/pdf'
            response['Content-Disposition'] = 'attachment;filename=games_list.pdf'
            return response
    context.update({'triples': triples})
    return HttpResponse(template.render(context, request))


def check_games_platform(request):
    context = manage_file(request)
    template = loader.get_template('games_platform.html')
    if 'platform' in request.POST:
        platform = request.POST['platform']
        if platform:
            triples_platform.clear()
            query = _graph.query([('?id', 'Name', '?games'), ('?id', 'Platform', platform)])
            for q in query:
                triples_platform.append((q['id'], 'Name', q['games']))
            context.update({
                'error': False,
                'triples': triples_platform
            })
        else:
            context.update({
                'error': True,
                'message': 'Insert the platform'
            })
    elif 'download_graph' in request.POST:
        g = Source(triples2dot(triples_platform), "games_platform.gv.pdf", "dotout", "pdf", "neato")
        g.render(view=True)
        with open('dotout/games_platform.gv.pdf', 'rb') as pdf:
            response = HttpResponse(pdf.read())
            response['content_type'] = 'application/pdf'
            response['Content-Disposition'] = 'attachment;filename=games_platform.pdf'
            return response
    else:
        context.update({'error': False})
    return HttpResponse(template.render(context, request))


def add_new_game_record(request):
    context = manage_file(request)
    template = loader.get_template('add_new_game.html')
    if ('subject' and 'predicate' and 'object') in request.POST:
        sub = request.POST['subject']
        pred = request.POST['predicate']
        obj = request.POST['object']
        if sub and pred and obj:
            if len(_graph.triples(sub, pred, obj)) > 0:
                context.update({
                    'error': True,
                    'message': 'Tuple already exists'
                })
            else:
                _graph.add(sub, pred, obj)
                context.update({
                    'error': False,
                    'message': 'Triple successfully added'
                })
        else:
            context.update({
                'error': True,
                'message': 'Fill all the fields'
            })
    else:
        context.update({'error': False})
    return HttpResponse(template.render(context, request))


def remove_game(request):
    context = manage_file(request)
    template = loader.get_template('remove_game.html')
    if ('subject' and 'predicate' and 'object') in request.POST:
        sub = request.POST['subject']
        pred = request.POST['predicate']
        obj = request.POST['object']
        if sub and pred and obj:
            if sub == 'None':
                sub = None
            if pred == 'None':
                pred = None
            if obj == 'None':
                obj = None
            number = len(_graph.triples(sub, pred, obj))
            _graph.remove(sub, pred, obj)
            context.update({
                'error': False,
                'message': str(number) + ' tuples were removed'
            })
        else:
            context.update({
                'error': True,
                'message': 'Fill all the fields'
            })
    else:
        context.update({'error': False})
    return HttpResponse(template.render(context, request))


def add_console_inference(request):
    context = manage_file(request)
    template = loader.get_template('console_type_inference.html')
    cType = consoleTypeRule()
    _graph.applyConsoleTypeInference(cType)
    context.update({'triples': _graph.triples(None, 'type', None)})
    return HttpResponse(template.render(context, request))


def add_region_inference(request):
    context = manage_file(request)
    template = loader.get_template('main_region_inference.html')
    rType = mainRegionRule()
    _graph.applyMainRegionInference(rType)
    context.update({'triples': _graph.triples(None, 'Main Region', None)})
    return HttpResponse(template.render(context, request))
