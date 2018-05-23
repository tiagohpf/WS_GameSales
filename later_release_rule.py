from inference import InferenceRule


class laterReleaseRule(InferenceRule):

    def getQueries(self):
        sales = [('?id', 'Year', '?year'), ('?id2', 'Year', '?year2')]
        return [sales]

    def makeTriples(self, id1, id2, year1, year2):
        print(id1, id2, year1, year2)
        if (id1 != id2 and int(year1) > int(year2)):
            return [(id1, 'Earlier', id2)]
        elif (id1 != id2 and int(year1) < int(year2)):
            return [(id1, 'Later', id2)]
        elif (id1 != id2 and int(year1) == int(year2)):
            return [(id1, 'Same', id2)]
        return []
