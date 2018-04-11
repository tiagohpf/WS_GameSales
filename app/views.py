from django.shortcuts import render
from django.http import HttpRequest
from django.template import loader
from django.http import HttpResponse

from consoleTypeRule import consoleTypeRule
from grafo import Grafo
# from graphviz import Source
import re
import os

from mainRegionRule import mainRegionRule

#os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin'

_graph = Grafo()

"""def listAllTuples():
    _graph.printAllTriples()
    triples = _graph.triples(None, None, None)
    dot = triples2dot(triples)
    g = Source(dot, "relations.gv", "dotout", "pdf", "neato")
    g.render(view=True)


def checkGamesList():
    triples = _graph.triples(None, 'Name', None)
    _graph.printTriples(triples)
    dot = triples2dot(triples)
    g = Source(dot, "relations.gv", "dotout", "pdf", "neato")
    g.render(view=True)"""


def gamesPerPlatform():
    platform = input("Platform Tag: ")
    t = _graph.query([('?id', 'Name', '?games'), ('?id', 'Platform', platform)])
    _graph.printResults(t)


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
def file_manager(request):
    if 'load_file' in request.POST:
        file = request.POST['load_file']
        _graph.load('clean_data/' + file)
        _graph.printAllTriples()
    elif 'save_file' in request.POST:
        file = request.POST['save_file']
        _graph.save('clean_data/' + file)
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def list_all_tuples(request):
    template = loader.get_template('all_tuples.html')
    context = {
        'triples': _graph.triples(None, None, None)
    }
    return HttpResponse(template.render(context, request))


def check_games_list(request):
    template = loader.get_template('games_list.html')
    context = {}
    return HttpResponse(template.render(context, request))


def check_games_platform(request):
    template = loader.get_template('games_platform.html')
    context = {}
    return HttpResponse(template.render(context, request))


def add_new_game_record(request):
    template = loader.get_template('add_new_game.html')
    if ('subject' and 'predicate' and 'object') in request.POST:
        sub = request.POST['subject']
        pred = request.POST['predicate']
        obj = request.POST['object']
        if sub and pred and obj:
            if len(_graph.triples(sub, pred, obj)) > 0:
                context = {
                    'error': True,
                    'message': 'Tuple already exists'
                }
            else:
                _graph.add(sub, pred, obj)
                context = {
                    'error': False,
                    'message': 'Triple successfully added'
                }
        else:
            context = {
                'error': True,
                'message': 'Fill all the fields'
            }
    else:
        context = {'error': False}
    return HttpResponse(template.render(context, request))


def remove_game(request):
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
            context = {
                'error': False,
                'message': str(number) + ' tuples were removed'
            }
        else:
            context = {
                'error': True,
                'message': 'Fill all the fields'
            }
    else:
        context = {'error': False}
    return HttpResponse(template.render(context, request))


def add_console_inference(request):
    template = loader.get_template('console_type_inference.html')
    cType = consoleTypeRule()
    context = {'triples': _graph.applyConsoleTypeInference(cType)}
    return HttpResponse(template.render(context, request))


def add_region_inference(request):
    template = loader.get_template('main_region_inference.html')
    rType = mainRegionRule()
    context = {'triples': _graph.applyMainRegionInference(rType)}
    return HttpResponse(template.render(context, request))
