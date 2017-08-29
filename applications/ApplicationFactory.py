
from applications.MnistApplication import MnistApplication

class ApplicationFactory:
    @staticmethod
    def create(name, configuration):
        if name == "mnist":
            return MnistApplication(configuration)

        return None


