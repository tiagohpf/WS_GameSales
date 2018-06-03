from inference import InferenceRule
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import json


class laterReleaseRule(InferenceRule):
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
        results = ""
        for result in res['results']['bindings']:
            first_year = int(result['year1']['value'])
            second_year = int(result['year2']['value'])
            id1 = result['id1']['value'].replace(self.baseEntity, '')
            id2 = result['id2']['value'].replace(self.baseEntity, '')
            if id1 != id2:
                if first_year < second_year:
                    results += id1 + ' Earlier ' + id2 + ' .\n'
                elif first_year == second_year:
                    results += id1 + ' Same ' + id2 + ' .\n'
                else:
                    results += id1 + ' Later ' + id2 + ' .\n'
        return results
