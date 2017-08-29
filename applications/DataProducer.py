
class DataProducer:
    def __init__(self, dataset, configuration):
        self.dataset       = dataset
        self.configuration = configuration

    def getIterationsPerEpoch(self):
        return self.dataset.num_examples() / self.getBatchSize()

    def getBatchSize(self):
        return int(self.configuration["mini-batch-size"])

    def nextBatch(self):
        return self.dataset.next_batch(self.getBatchSize())

    def nextEpoch(self):
        #TODO
        pass

