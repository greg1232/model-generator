
from random import Random

class ModelHistory:
    def __init__(self):
        self.history = []
        self.generator = Random()
        self.generator.seed(777)

    def addModel(self, model, newModel, reward):
        self.history.append((model, newModel, reward))

    def sampleModel(self):
        return self.getBatch()[0]

    def getBatch(self):
        return self.history[self.generator.randrange(len(self.history))]




