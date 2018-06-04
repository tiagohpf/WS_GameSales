from inference import InferenceRule
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import json


class mainRegionRule(InferenceRule):
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
            SELECT ?s ?n ?e ?j ?o  
            WHERE 
            {
                ?s pred:na_sales ?n .
                ?s pred:eu_sales ?e .
                ?s pred:jp_sales ?j .
                ?s pred:other_sales ?o .
            }
        """
        payload_query = {"query": query}
        res = self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)
        res = json.loads(res)
        results = ""
        for result in res['results']['bindings']:
            sub = result['s']['value'].replace(self.baseEntity, '')
            NA = float(result['n']['value'])
            EU = float(result['e']['value'])
            JP = float(result['j']['value'])
            OT = float(result['o']['value'])
            region = {'NorthAmerica': NA, 'Europe': EU, 'Japan': JP, 'Others': OT}
            max_value = max(region, key=region.get)
            results += sub + ' Main_Region ' + max_value + ' .\n'
        return results
