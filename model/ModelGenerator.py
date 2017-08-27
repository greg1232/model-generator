

import tensorflow as tf

#
class ModelGenerator:
    def __init__(self, modelDescription, modelInput, modelOutput):
        self.modelDescription = modelDescription

        self.input  = modelInput
        self.output = modelOutput

    def getModelDescription(self):
        return self.modelDescription

    def buildModel(self):
        self.checkInput()
        self.checkOutput()





