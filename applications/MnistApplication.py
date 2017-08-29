
from tensorflow.examples.tutorials.mnist import input_data

from DataProducer import DataProducer

import logging

class MnistApplication:
    def __init__(self, configuration):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Getting mnist training data.")
        self.mnist_data = input_data.read_data_sets(configuration["data_directory"], one_hot=True)


    def getInputData(self):
        return (28, 28)

    def getOutputData(self):
        return (10)

    def getTrainingDataProducer(self):
        return DataProducer(self.mnist.train)

    def getValidationDataProducer(self):
        return DataProducer(self.mnist.test)






