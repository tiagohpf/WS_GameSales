from inference import InferenceRule


class consoleTypeInference(InferenceRule):

    def getQueries(self):
        consoleQuery = [('?id', 'Platform','?plat')]
        return [consoleQuery]

    def makeTriples(self, id, plat):
        if plat == 'DS' or plat == 'GB' or plat == 'GBA' or plat == 'PSP':
            return [(id, 'type', 'Portable')]
        else:
            return [(id, 'type', 'Console')]

