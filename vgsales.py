from grafo import Grafo
from consoleTypeRule import consoleTypeRule
from mainRegionRule import mainRegionRule
from graphviz import Source
import re
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin'

# menu
def menu():
    print("*** MENU ***")
    print("1. Load Game Sales File")
    print("2. List all Tuples")
    print("3. Check Games List")
    print("4. Check Games per Platform")
    print("5. Add new Game Record")
    print("6. Remove Game Record")
    print("7. Add Console Type Inference")
    print("8. Add Main Region Inference")
    print("9. Save Triples in File")
    print("0. Sair")
    return int(input("Option: "))


def run(op):
    _funcs[op - 1]()


def loadGameSalesFile():
    file = input("File Name: ")
    _graph.load('data/' + file)

def saveGameSalesData():
    file = input("File Name: ")
    _graph.save('data/' + file)

def listAllTuples():
    _graph.printAllTriples()
    triples = _graph.triples(None,None,None)
    dot = triples2dot(triples)
    g = Source(dot, "relations.gv", "dotout", "pdf", "neato")
    g.render(view=True)

def checkGamesList():
    triples = _graph.triples(None, 'Name', None)
    _graph.printTriples(triples)
    dot = triples2dot(triples)
    g = Source(dot, "relations.gv", "dotout", "pdf", "neato")
    g.render(view=True)


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
        dot = dot + ('%s -- %s [label=%s]\n' % (re.sub('[^A-Za-z0-9]+', '', s), re.sub('[^A-Za-z0-9]+', '', o), re.sub('[^A-Za-z0-9]+', '', p)))
    dot = dot + "}"
    return dot

# inicio do modulo
if __name__ == "__main__":
    # tuplo de referências das funções para cada opção do menu
    _funcs = (loadGameSalesFile, listAllTuples, checkGamesList, gamesPerPlatform, addNewGameRecord, removetriple,
              addTypeInference, addRegionInference, saveGameSalesData)
    _graph = Grafo()
    while (True):
        op = menu()
        if op == 0:
            break
        run(op)
