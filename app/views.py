from django.template import loader
from django.http import HttpResponse
from console_type_rule import consoleTypeRule
from grafo import Grafo
from graphviz import Source
from sparql_queries import SparqlQueries
import re
import os
from main_region_rule import mainRegionRule
from later_release_rule import laterReleaseRule

# os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin'
os.environ["PATH"] += os.pathsep + '/usr/local/lib/python3.6/dist-packages/graphviz'
_graph = Grafo()
_sparql = SparqlQueries()
baseEntity = "http://www.games.com/entity/"
baseProperty = "http://www.games.com/pred/"
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

def file_status(request):
    context = {}
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def list_all_tuples(request):
    template = loader.get_template('all_tuples.html')
    tuples = _sparql.list_all_triples()
    tuples = get_objects_type(tuples)
    context = {'tuples': tuples}
    return HttpResponse(template.render(context, request))


def check_games_list(request):
    template = loader.get_template('games_list.html')
    triples = _sparql.check_games_list()
    if 'download_graph' in request.POST:
        g = Source(triples2dot(triples), "games_list.gv", "dotout", "pdf", "neato")
        g.render(view=True)
        with open('dotout/games_list.gv.pdf', 'rb') as pdf:
            response = HttpResponse(pdf.read())
            response['content_type'] = 'application/pdf'
            response['Content-Disposition'] = 'attachment;filename=games_list.pdf'
            return response
    context = {'triples': triples}
    return HttpResponse(template.render(context, request))


def check_games_platform(request):
    template = loader.get_template('games_platform.html')
    if 'platform' in request.POST:
        platform = request.POST['platform']
        if platform:
            triples_platform.clear()
            query = _sparql.check_games_platform(platform)
            for sub, pred, obj in query:
                triples_platform.append((sub, pred, obj))
            context = {'error': False, 'triples': triples_platform}
        else:
            context = {'error': True, 'message': 'Insert the platform'}
    elif 'download_graph' in request.POST:
        g = Source(triples2dot(triples_platform), "games_platform.gv", "dotout", "pdf", "neato")
        g.render(view=True)
        with open('dotout/games_platform.gv.pdf', 'rb') as pdf:
            response = HttpResponse(pdf.read())
            response['content_type'] = 'application/pdf'
            response['Content-Disposition'] = 'attachment;filename=games_platform.pdf'
            return response
    else:
        context = {'error': False}
    return HttpResponse(template.render(context, request))


def add_new_game_record(request):
    context = {'predicates': _sparql.get_all_predicates()}
    template = loader.get_template('add_new_game.html')
    if ('subject' and 'predicate' and 'object') in request.POST:
        sub = request.POST['subject']
        pred = request.POST['predicate']
        obj = request.POST['object']
        if sub and pred and obj:
            if _sparql.triple_already_exists(sub, pred):
                context.update({'error': True, 'message': 'Triple already exists'})
            else:
                _sparql.add_new_game_record(sub, pred, obj)
                context.update({'error': False, 'message': 'Triple successfully added'})
        else:
            context.update({'error': True, 'message': 'Fill all the fields'})
    else:
        context.update({'error': False})
    return HttpResponse(template.render(context, request))


def remove_game(request):
    template = loader.get_template('remove_game.html')
    if ('subject' and 'predicate' and 'object') in request.POST:
        sub = request.POST['subject']
        pred = request.POST['predicate']
        obj = request.POST['object']
        if sub and pred and obj:
            if sub.lower() == 'none':
                sub = None
            if pred.lower() == 'none':
                pred = None
            if obj.lower() == 'none':
                obj = None
            number = _sparql.remove_game_record(sub, pred, obj)
            context = {'error': False, 'message': str(number) + ' triples were removed'}
        else:
            context = {'error': True, 'message': 'Fill all the fields'}
    else:
        context = {'error': False}
    return HttpResponse(template.render(context, request))


def add_console_inference(request):
    template = loader.get_template('console_type_inference.html')
    if 'download_graph' in request.POST:
        g = Source(triples2dot(triples_platform), "console_inference.gv", "dotout", "pdf", "neato")
        g.render(view=True)
        with open('dotout/console_inference.gv.pdf', 'rb') as pdf:
            response = HttpResponse(pdf.read())
            response['content_type'] = 'application/pdf'
            response['Content-Disposition'] = 'attachment;filename=console_inference.pdf'
            return response
    else:
        triples_platform.clear()
        cType = consoleTypeRule()
        triples = cType.get_inference_triples()
        _sparql.insert_inferences(triples)
        for triple in triples.split('\n'):
            triple = triple.split(' ')
            if len(triple) >= 3:
                triples_platform.append((triple[0], triple[1], triple[2]))
        context = {'triples': triples_platform}
        return HttpResponse(template.render(context, request))


def add_region_inference(request):
    template = loader.get_template('main_region_inference.html')
    if 'download_graph' in request.POST:
        g = Source(triples2dot(triples_platform), "region_inference.gv", "dotout", "pdf", "neato")
        g.render(view=True)
        with open('dotout/region_inference.gv.pdf', 'rb') as pdf:
            response = HttpResponse(pdf.read())
            response['content_type'] = 'application/pdf'
            response['Content-Disposition'] = 'attachment;filename=region_inference.pdf'
            return response
    else:
        triples_platform.clear()
        rType = mainRegionRule()
        triples = rType.get_inference_triples()
        _sparql.insert_inferences(triples)
        for triple in triples.split('\n'):
            triple = triple.split(' ')
            if len(triple) >= 3:
                triples_platform.append((triple[0], triple[1], triple[2]))
        context = {'triples': triples_platform}
        return HttpResponse(template.render(context, request))


def add_release_inference(request):
    template = loader.get_template('release_year_inference.html')
    if 'download_graph' in request.POST:
        g = Source(triples2dot(triples_platform), "release_year_inference.gv", "dotout", "pdf", "neato")
        g.render(view=True)
        with open('dotout/release_year_inference.gv.pdf', 'rb') as pdf:
            response = HttpResponse(pdf.read())
            response['content_type'] = 'application/pdf'
            response['Content-Disposition'] = 'attachment;filename=release_year_inference.pdf'
            return response
    else:
        triples_platform.clear()
        lType = laterReleaseRule()
        triples = lType.get_inference_triples()
        _sparql.insert_inferences(triples)
        for triple in triples.split('\n'):
            triple = triple.split(' ')
            if len(triple) >= 3:
                triples_platform.append((triple[0], triple[1], triple[2]))
        context = {'triples': triples_platform}
        return HttpResponse(template.render(context, request))


def get_objects_type(triples):
    res = []
    for sub, pred, obj in triples:
        if baseEntity in obj:
            res.append((sub, pred, obj, 'entity'))
        else:
            res.append((sub, pred, obj, 'literal'))
    return res
