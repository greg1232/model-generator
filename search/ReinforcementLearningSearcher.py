
from history.ModelHistory import ModelHistory
from model.ControllerFactory import ControllerFactory

from training.ModelTrainer import ModelTrainer
from performance.PerformanceModel import PerformanceModel

class ReinforcementLearningSearcher:
    def __init__(self, application, configuration):
        self.application = application
        self.configuration = configuration
        self.controller  = ControllerFactory.create()
        self.modelHistory = ModelHistory()

    def run(self):
        iterations = self.configuration["iterations"]

        for i in iterations:
            # create a new model
            model = self.modelHistory.sampleModel()

            newModel = self.controller.getNextModel(model)

            # determine the reward
            reward = self.evaluateModel(newModel)

            # record the result
            self.modelHistory.addModel(model, newModel, reward)

            # train the controller
            self.updateController()

    def evaluateModel(self, newModel):
        trainer = ModelTrainer(newModel, self.application, self.configuration)
        performanceModel = PerformanceModel(newModel)

        time = performanceModel.getTime()
        error = trainer.train()

        return self.evaluateReward(time, error)

    def evaluateReward(self, time, error):
        # TODO
        if time < self.configuration["minimum_time"]:
            time = 0.0

        return time + error

    def updateController(self):
        iterations = self.configuration["controller_update_iterations"]

        for i in range(iterations):
            batch = self.modelHistory.getBatch()

            self.controller.trainOnBatch(batch)



