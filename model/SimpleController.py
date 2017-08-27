

def loopCondition(networkDescription, stopCondition):
    return tf.less(stopCondition, 0.0)

def buildNetworkEmbedding(networkDescription, configuration):
    layerSize = configuration["network_embedding_size"]
    cell = tf.nn.rnn_cell.LSTMCell(layerSize)

    outputs, state = tf.nn.dynamic_rnn(cell, networkDescription)

    return state

def buildLayerEmbedding(networkEmbedding, configuration):
    layerSize = configuration["layer_embedding_size"]

    return tf.contrib.layers.fully_connected(networkEmbedding, layerSize)

def layerLoopCondition(layerDescription, layerEmbedding, stopCondition):
    return tf.less(stopCondition, 1.0)

def layerLoopBody(layerDescription, layerEmbedding, stopCondition):


def buildLayer(layerEmbedding, configuration):

    stopCondition = tf.Constant(0.0)

    layerDescription = tf.TensorArray(self.getDataType(), (Schema.TOTAL_FEATURES))

    layerDescription, _, _ = tf.while_loop(layerLoopCondition, layerLoopBody,
        [layerDescription, layerEmbedding, stopCondition])

    return layerDescription

def loopBody(networkDescription, stopCondition):
    # generate network embedding
    networkEmbedding = buildEmbeddingNetwork(networkDescription, configuration)

    # generate layer embedding
    layerEmbedding = buildLayerEmbedding(networkEmbedding, configuration)

    # generate layer
    newLayerDescription = buildLayer(layerEmbedding, configuration)

    # generate connections
    connections = buildLayerConnections(layerEmbedding, configuration)

    # update the stop condition
    stopCondition = buildStopCondition(networkEmbedding, layerEmbedding, configuration)

    networkDescription = tf.concat([networkDescription, newLayerDescription, connections], dim=1)

    return networkDescription, stopCondition

class SimpleController:
    def __init__(self, configuration):
        self.configuration = configuration
        self.controllerInput = self.buildControllerInput()
        self.controllerOperation = self.buildControllerOperation()

    def getNextModel(self, modelDescription):
        modelDescriptionFeatures = self.getFeatures(modelDescription)

        newModelDescriptionFeatures = self.getSession().run(
            self.getControllerOperation(),
            feed_dict={self.getControllerInput(), modelDescriptionFeatures})

        descriptionManipulator = ModelDescription()
        descriptionManipulator.setFromTensor(newModelDescriptionFeatures)

        return descriptionManipulator.getJSON()

    def getFeatures(self, modelDescription):
        descriptionManipulator = ModelDescription()
        descriptionManipulator.setFromJSON(modelDescription)

        return descriptionManipulator.getTensor()

    def getControllerOperation(self):
        return self.controllerOperation

    def buildControllerOperation(self):

        # loop until max steps or until hit stop condition
        stopCondition = tf.Constant(0.0)

        networkDescription = tf.TensorArray(self.getDataType(), (Schema.TOTAL_FEATURES))

        networkDescription, _, _ = tf.while_loop(controllerLoopCondition, controllerLoopBody,
            [networkDescription, getControllerInput(), stopCondition])

        self.controllerOperation = networkDescription

    def buildControllerInput(self):
        return tf.placeholder(self.getDataType(), shape=[Schema.TOTAL_FEATURES, None])

    def getDataType(self):
        return tf.float16 if self.configuration["data_type"] == "float16" else tf.float32

    def getControllerInput(self):
        return self.controllerInput


