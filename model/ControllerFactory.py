
from model.SimpleController import SimpleController

class ControllerFactory:
    @staticmethod
    def create(configuration):
        return SimpleController(configuration)





