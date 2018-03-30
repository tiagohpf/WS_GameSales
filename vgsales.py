from grafo import Grafo
from consoleTypeInference import consoleTypeInference


# menu
def menu():
    print("*** MENU ***")
    print("1. Load Game Sales File")
    print("2. List all Tuples")
    print("3. Check Games List")
    print("4. Check Games per Platform")
    print("5. Add new Game Record")
    print("6. Remove Game Record")
    print("7. Add Type Inference")
    print("0. Sair")
    return int(input("Option: "))


def run(op):
    _funcs[op - 1]()


def loadGameSalesFile():
    file = input("File Name: ")
    _graph.load('data/' + file)


def listAllTuples():
    _graph.printAllTriples()


def checkGamesList():
    triples = _graph.triples(None, 'Name', None)
    _graph.printTriples(triples)


def checkGamesList():
    triples = _graph.triples(None, 'Name', None)
    _graph.printTriples(triples)


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
    cType = consoleTypeInference()
    _graph.applyinference(cType)


# inicio do modulo
if __name__ == "__main__":
    # tuplo de referências das funções para cada opção do menu
    _funcs = (loadGameSalesFile, listAllTuples, checkGamesList, gamesPerPlatform, addNewGameRecord, removetriple,
              addTypeInference)
    _graph = Grafo()
    while (True):
        op = menu()
        if op == 0:
            break
        run(op)
