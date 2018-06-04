from inference import InferenceRule
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import json


class consoleTypeRule(InferenceRule):
    def __init__(self):
        self.baseEntity = "http://www.games.com/entity/"
        self.baseProperty = "http://www.games.com/pred/"
        self.endpoint = "http://localhost:7200"
        self.repo_name = "games"
        self.client = ApiClient(endpoint=self.endpoint)
        self.accessor = GraphDBApi(self.client)

    def get_inference_triples(self):
        query = """
            PREFIX pred: <http://www.games.com/pred/>
            SELECT ?s ?o 
            WHERE 
            {
                ?s pred:platform ?o .
            }
        """
        payload_query = {"query": query}
        res = self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)
        res = json.loads(res)
        results = ""
        for result in res['results']['bindings']:
            sub = result['s']['value'].replace('http://www.games.com/entity/', '')
            obj = result['o']['value'].replace('http://www.games.com/entity/', '')
            if obj == 'ds' or obj == 'gb' or obj == 'gba' or obj == 'psp':
                results += sub + ' Console_Type ' + 'Portable .\n'
            else:
                results += sub + ' Console_Type ' + 'Console .\n'
        return results
