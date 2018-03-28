class InferenceRule:

    def getQueries(self):
        return None

    def makeTriples(self, binding):
        return self._maketriples(**binding)