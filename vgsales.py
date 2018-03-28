from grafo import Grafo

# menu
def menu():
    print("*** MENU ***")
    print("1. Load Game Sales File")
    print("2. List all Tuples")
    print("3. Check Games List")
    print("4. Listar jogos por plataforma")
    print("0. Sair")
    return int(input("Opcao: "))

def run(op):
    _funcs[op-1]()

def loadGameSalesFile():
    file = input("File Name: ")
    _graph.load(file)

def listAllTuples():
    _graph.printAllTriples()

def checkGamesList():
    triples = _graph.triples(None, 'Name', None)
    _graph.printTriples(triples)

def checkGamesList():
    triples = _graph.triples(None, 'Name', None)
    _graph.printTriples(triples)

def gamesPerPlatform():
    t = _graph.query([('?id', 'Name', '?games'), ('?id', 'Platform', '?platform')])
    _graph.printList(t)


# inicio do modulo
if __name__ == "__main__":
    # tuplo de referências das funções para cada opção do menu
    _funcs = (loadGameSalesFile, listAllTuples, checkGamesList,gamesPerPlatform)
    _graph = Grafo()
    while(True):
        op = menu()
        if op == 0:
            break
        run(op)
