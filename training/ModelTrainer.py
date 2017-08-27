
class ModelTrainer:
    def __init__(self, modelDescription, application, configuration):
        self.modelDescription = modelDescription
        self.application = application
        self.configuration = configuration

        self.modelResults = []

    def train(self):
        inputData = self.application.getInputData()
        outputData = self.application.getOutputData()

        model = ModelGenerator(self.modelDescription, inputData, outputData).buildModel()

        results = self.trainModel(model)

        return self.getModelAccuracy(results)

    def trainModel(self, model):
        # initialize the model
        initializer = model.getInitializer()

        self.session.run(initializer)

        # start training
        epochs = self.configuration['model-training-epochs']

        producer = self.application.getTrainingDataProducer(self.configuration)

        iterations = producer.getIterationsPerEpoch()

        results = []

        for e in range(epochs):
            for i in range(iterations):
                batchInputs, batchOutputs = producer.nextBatch()

                self.session.run(model.getUpdateOperation(), feed_dict=
                    {
                        model.getInput()  : batchInputs,
                        model.getOutput() : batchOutputs
                    })

            result.append(self.runValidation(model))

            producer.nextEpoch()

        return results

    def runValidation(self, model):
        producer = self.application.getValidationDataProducer(self.configuration)

        iterations = producer.getIterationsPerEpoch()

        loss = 0.0

        for i in range(iterations):
            batchInputs, batchOutputs = producer.nextBatch()

            loss += self.session.run(model.getLossOperation(), feed_dict=
                {
                    model.getInput()  : batchInputs,
                    model.getOutput() : batchOutputs
                })

        return loss / (iterations * producer.getBatchSize())

    def getModelAccuracy(self, results):
        return min(results)


