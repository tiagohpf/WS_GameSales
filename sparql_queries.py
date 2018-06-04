import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient


class SparqlQueries():
    def __init__(self):
        self.baseEntity = "http://www.games.com/entity/"
        self.baseProperty = "http://www.games.com/pred/"
        self.endpoint = "http://localhost:7200"
        self.repo_name = "games"
        self.client = ApiClient(endpoint=self.endpoint)
        self.accessor = GraphDBApi(self.client)

    def list_all_triples(self):
        query = """
            PREFIX pred: <http://www.games.com/pred/>
            SELECT ?s ?p ?o
            WHERE 
            {
                ?s ?p ?o .
                FILTER (strstarts(str(?p), "http://www.games.com/pred/")) 
            }
        """
        payload_query = {"query": query}
        res = self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)
        res = json.loads(res)
        triples = []
        for e in res['results']['bindings']:
            sub = e['s']['value']
            pred = e['p']['value']
            obj = e['o']['value']
            triples.append((sub, pred, obj))
        return triples

    def check_games_list(self):
        query = """
            PREFIX pred: <http://www.games.com/pred/>
            SELECT ?s ?o
            WHERE {
                ?s pred:name ?o .        
                }
        """
        payload_query = {"query": query}
        res = self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)
        res = json.loads(res)
        triples = []
        for e in res['results']['bindings']:
            sub = e['s']['value'].replace(self.baseEntity, '').title()
            pred = 'Name'
            obj = e['o']['value'].replace(self.baseEntity, '').title()
            triples.append((sub, pred, obj))
        return triples

    def check_games_platform(self, platform):
        query = """
            PREFIX pred: <http://www.games.com/pred/>
            PREFIX obj:  <http://www.games.com/entity/>
            SELECT ?s ?o
            WHERE 
            {
                ?s pred:platform obj:""" + platform.lower() + """ .
                ?s pred:name ?o .
            }
        """
        payload_query = {"query": query}
        res = self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)
        res = json.loads(res)
        triples = []
        for e in res['results']['bindings']:
            sub = e['s']['value'].replace(self.baseEntity, '').title()
            pred = 'Platform'
            obj = e['o']['value'].replace(self.baseEntity, '').title()
            triples.append((sub, pred, obj))
        return triples

    def add_new_game_record(self, sub, pred, obj):
        sub = sub.lower().replace(' ', '_')
        pred = pred.lower().replace(' ', '_')
        obj = obj.lower().replace(' ', '_')
        if pred == 'platform' or pred == 'publisher':
            update = """
                PREFIX pred: <http://www.games.com/pred/>
                PREFIX entity: <http://www.games.com/entity/>
                INSERT DATA
                {
                    entity:""" + sub + """ pred:""" + pred + """ entity:""" + obj + """ .
                }
            """
        else:
            update = """
                PREFIX pred: <http://www.games.com/pred/>
                PREFIX entity: <http://www.games.com/entity/>
                INSERT DATA
                {
                    entity:""" + sub + """ pred:""" + pred + """ \"""" + obj + """\" .
                }
            """
        payload_query = {"update": update}
        self.accessor.sparql_update(body=payload_query, repo_name=self.repo_name)

    def remove_game_record(self, sub, pred, obj):
        before_remove = len(self.list_all_triples())
        if sub is None:
            sub = '?s'
        else:
            sub = str('<' + self.baseEntity + sub + '>').lower().replace(' ', '_')
        if obj is None:
            obj = '?o'
        else:
            if pred == 'platform' or pred == 'publisher':
                obj = str('<' + self.baseEntity + obj + '>').lower().replace(' ', '_')
            else:
                obj = str('"' + obj + '"')
        if pred is None:
            pred = '?p'
        else:
            pred = str('<' + self.baseProperty + pred + '>').lower().replace(' ', '_')
        update = """
            DELETE WHERE
            {
                """ + sub + """ """ + pred + """ """ + obj + """ .
            }
        """
        payload_query = {"update": update}
        self.accessor.sparql_update(body=payload_query, repo_name=self.repo_name)
        after_remove = len(self.list_all_triples())
        return before_remove - after_remove

    def release_date(self):
        query = """
            PREFIX pred: <http://www.games.com/pred/>
            SELECT ?year1 ?year2 ?id1 ?id2
            WHERE
            {
                ?id1 pred:year ?year1 .       
                ?id2 pred:year ?year2 .
            }
            """
        payload_query = {"query": query}
        res = self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)
        res = json.loads(res)
        for e in res['results']['bindings']:
            print(e['year1']['value'] + ", " + e['year2']['value'] + ", " +
                  e['id1']['value'] + ", " + e['id2']['value'])

    def main_region(self):
        query = """
            PREFIX pred: <http://www.games.com/pred/>
            SELECT ?id ?NA ?EU ?JP ?Other
            WHERE
            {
                ?id pred:na_sales ?NA .       
                ?id pred:eu_sales ?EU .       
                ?id pred:jp_sales ?JP .       
                ?id pred:other_sales ?Other .       
             }
            """
        payload_query = {"query": query}
        res = self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)
        res = json.loads(res)
        for e in res['results']['bindings']:
            print(e['id']['value'] + ", " + e['NA']['value'] + ", " + e['EU']['value'] + ", "
                  + e['JP']['value'] + ", " + e['Other']['value'])

    def triple_already_exists(self, sub, pred, obj=None):
        sub = sub.lower().replace(' ', '_')
        pred = pred.lower().replace(' ', '_')
        if obj is not None:
            obj = obj.lower().replace(' ', '_')
            query = """
                PREFIX pred: <http://www.games.com/pred/>
                PREFIX entity: <http://www.games.com/entity/>
                ASK
                {
                    entity:""" + sub + """ pred:""" + pred + """ entity:""" + obj + """ .
                } 
            """
        else:
            query = """
                PREFIX pred: <http://www.games.com/pred/>
                PREFIX entity: <http://www.games.com/entity/>
                ASK
                {
                    entity:""" + sub + """ pred:""" + pred + """ ?o """ + """ .
                } 
                """
        payload_query = {"query": query}
        res = self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)
        res = json.loads(res)
        return res['boolean']

    def get_all_predicates(self):
        triples = self.list_all_triples()
        predicates = []
        for sub, pred, obj in triples:
            if pred not in predicates:
                predicates.append(pred)
        return predicates

    def insert_inferences(self, sub):
        update = """
            PREFIX pred: <http://www.games.com/pred/>
            PREFIX entity: <http://www.games.com/entity/>
            INSERT DATA
            {
                """ + sub + """
            }
        """
        payload_query = {"update": update}
        self.accessor.sparql_update(body=payload_query, repo_name=self.repo_name)