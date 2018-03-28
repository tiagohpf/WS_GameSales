# -*- coding: utf-8 -*-

# simplegraph.py

import csv

class Grafo:

    # inicialização
    def __init__(self):
        self._spo = []

    # adiciona um triplo aos 3 índices
    def add(self, sub, pred, obj):
        self._addToIndex(self._spo, sub, pred, obj)


    # adiciona os termos ao índice
    def _addToIndex(self, index, sub, pred, obj):
        triple = (sub,pred,obj)
        if triple not in index:
            index.append(triple)

    def remove(self, sub, pred, obj):
        triples = list(self.triples((sub, pred, obj)))
        for (delSub, delPred, delObj) in triples:
            self._removeFromIndex(self._spo, delSub, delPred, delObj)

    # remove os termos do índice
    def _removeFromIndex(self, index, sub, pred, obj):
        index.remove((sub, pred, obj))


    def triples(self, sub, pred, obj):
        triplesList = []
        if sub != None:
            if pred != None:
                if obj != None:
                    for triple in self._spo:
                        if triple == (sub,pred,obj):
                            triplesList.append(triple);
                else:
                    for triple in self._spo:
                        if triple[0] == sub and triple[1] == pred:
                            triplesList.append(triple);
            else:
                if obj != None:
                    for triple in self._spo:
                        if triple[0] == sub and triple[2] == obj:
                            triplesList.append(triple);
                else:
                    for triple in self._spo:
                        if triple[0] == sub:
                            triplesList.append(triple);
        else:
            if pred != None:
                if obj != None:
                    for triple in self._spo:
                        if triple[1] == pred and triple[2] == obj:
                            triplesList.append(triple);
                else:
                    for triple in self._spo:
                        if triple[1] == pred:
                            triplesList.append(triple);
            else:
                # None None obj
                if obj != None:
                    for triple in self._spo:
                        if triple[2] == obj:
                            triplesList.append(triple);
                else:
                    for triple in self._spo:
                        return self._spo;
        return triplesList


    # lê triplos de um ficheiro csv e adiciona-os aos índices
    def load(self, filename):
        f = open(filename, 'r', encoding='utf-8')
        reader = csv.reader(f)
        for sub, pred, obj in reader:
            self.add(sub, pred, obj)
        f.close()

    # guarda os triplos num ficheiro csv
    def save(self, filename):
        f = open(filename, "w", encoding='utf-8')
        writer = csv.writer(f)
        for sub, pred, obj in self.triples(None, None, None):
            writer.writerow([sub, pred, obj])
        f.close()

    def query(self, clauses):
        bindings = None  # resultado a devolver
        for clause in clauses:  # para cada triplo
            bpos = []
            qc = []  # lista de elementos a passar ao método triples
            for pos, x in enumerate(clause):  # enumera o triplo, para poder ir buscar cada elemento e sua posição
                if x.startswith('?'):  # para as variáveis
                    qc.append(None)  # adiciona o valor None à lista de elementos a pssar ao método triples
                    bpos.append((x[1:], pos))
                else:
                    qc.append(x)  # adiciona o valor dado à lista de elementos a pssar ao método triples
            rows = list(self.triples(qc[0], qc[1], qc[2]))  # faz a pesquisa com o triplo acabado de construir

            if bindings == None:
                bindings = []
                for row in rows:
                    binding = []
                    for duple in bpos:
                        binding.append((duple[0], row[duple[1]]))
                    bindings.append(binding)
            else:  # triplos pesquisa seguintes, eliminar resultados que não servem
                newb = []  # cria nova lista a devolver
                for binding in bindings:  # para cada dicionario da lista de dicionarios
                    for row in rows:  # para cada triplo resultado
                        validmatch = True  # começa por assumir que o dicionario serve
                        tempbinding = binding.copy()  # faz copia temporaria do dicionario
                        # for var, pos in bpos.items(): # para cada variavel em sua posição
                        for duple in bpos:
                            # if var in tempbinding: # caso a variavel esteja presente no dicionario
                            for tmp in tempbinding:
                                if duple[0] in tmp:
                                    # if tempbinding[var] != row[pos]: # se o valor da variavel diferente do valor na sua posicao no triplo
                                    print(tempbinding, duple, tmp)
                                    if tmp[0] != row[duple[1]]:
                                        print('enter')
                                        validmatch = False  # o dicionário não serve
                                else:
                                    tmp[0] = row[duple[1]]
                                    # tempbinding[var] = row[pos] # associa à variável o valor do elemento do triplo na sua posição
                        if validmatch:
                            newb.append(tempbinding)  # se dicionario serve, inclui-o na nova lista
                bindings = newb  # sbstituiu lista por nova
        return bindings

    # aplica inferencia ao grafo
    def applyinference(self,rule):
        queries = rule.getQueries()
        bindings=[]
        for query in queries:
            bindings += self.query(query)
        for b in bindings:
            new_triples = rule.makeTriples(b['person'], b['enemy'], b['rel'], b['partner']);
            for s, p, o in new_triples:
                self.add(s, p, o)



    # imprime todos os triplos
    def printAllTriples(self):
        t = self.triples(None, None, None)
        self.printTriples(t)


    # método estático para imprimir conjuntos de triplos num iterador
    @staticmethod
    def printTriples(t):
        for triple in t:
            print("'{0}' --> '{1}' --> '{2}" .format(triple[0], triple[1], triple[2]))