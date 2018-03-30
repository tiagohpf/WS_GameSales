from inference import InferenceRule

class mainRegionRule(InferenceRule):

    def getQueries(self):
        sales = [('?id', 'NA_Sales','?NA'), ('?id', 'EU_Sales','?EU'), ('?id', 'JP_Sales','?JP'), ('?id', 'Other_Sales','?Other')]
        return [sales]

    def makeTriples(self, id, Na, Eu, Jp, Other):
        region = {'NA': Na, 'EU': Eu, 'JP': Jp, 'Other': Other}
        maxValue = max(region, key=region.get)
        return [(id, 'Main Region', maxValue)]