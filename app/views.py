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

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin'

_graph = Grafo()


def loadGameSalesFile():
    file = input("File Name: ")
    _graph.load('data/' + file)


def saveGameSalesData():
    file = input("File Name: ")
    _graph.save('data/' + file)


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


def addNewGameRecord():
    print("Game Data Triple:")
    sub = input("Subject: ")
    pred = input("Predicate: ")
    obj = input("Object: ")
    _graph.add(sub, pred, obj)


def removetriple():
    print("Remove Triple")
    sub = input("Subject: ")
    if len(sub) == 0: sub = None
    pred = input("Predicate: ")
    if len(pred) == 0: pred = None
    obj = input("Object: ")
    if len(obj) == 0: obj = None
    _graph.remove(sub, pred, obj)


def addTypeInference():
    cType = consoleTypeRule()
    _graph.applyConsoleTypeInference(cType)


def addRegionInference():
    mRegion = mainRegionRule()
    _graph.applyMainRegionInference(mRegion)


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


def add_new_game_record(request):
    template = loader.get_template('add_new_game.html')
    if ('subject' and 'predicate' and 'object') in request.POST:
        sub = request.POST['subject']
        pred = request.POST['predicate']
        obj = request.POST['object']
        if sub and pred and obj:
            _graph.add(sub, pred, obj)
            context = {
                'error': False,
                'message': 'Triple successfully added!'
            }
        else:
            context = {
                'error': True,
                'message': 'Fill all the fields!'
            }
    else:
        context = {
            'error': False
        }
    return HttpResponse(template.render(context, request))
