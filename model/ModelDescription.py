
from model.ModelDescriptionSerializer   import ModelDescriptionSerializer
from model.ModelDescriptionDeserializer import ModelDescriptionDeserializer

class ModelDescription:
    def __init__(self):
        self.json = None

    def setFromJSON(self, json):
        self.json = json

    def setFromTensor(self, description):
        self.json = ModelDescriptionSerializer(description).toJson()

    def getJSON(self):
        return self.json

    def getTensor(self):
        return ModelDescriptionDeserializer(self.json).toTensor()


