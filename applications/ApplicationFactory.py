
from applications.MnistApplication import MnistApplication

class ApplicationFactory
    @staticmethod
    def create(name):
        if name == "mnist":
            return MnistApplication()

        return None


