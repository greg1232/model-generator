
import tensorflow as tf

import model.ModelSchema as Schema

def getDataType(configuration):
    return tf.float16 if configuration["data_type"] == "float16" else tf.float32

def controllerLoopCondition(networkDescription, inputNetworkDescription, stopCondition,
    configuration):

    return tf.less(stopCondition, 0.0)

def buildNetworkEmbedding(networkDescription, configuration):
    layerSize = int(configuration["network_embedding_size"])
    cell = tf.nn.rnn_cell.LSTMCell(layerSize)

    initialState = cell.zero_state(batch_size=tf.shape(networkDescription)[0],
        dtype=networkDescription.dtype)

    # project the network
    projection = tf.contrib.layers.fully_connected(networkDescription, layerSize)

    outputs, state = tf.nn.dynamic_rnn(cell, networkDescription,
        initial_state = initialState)

    return state.h

def buildLayerEmbedding(networkEmbedding, configuration):
    layerSize = int(configuration["layer_embedding_size"])

    return tf.contrib.layers.fully_connected(networkEmbedding, layerSize)

def layerLoopCondition(layerDescription, layerEmbedding, cellState):
    layerFields = tf.constant(2)

    return tf.less(layerDescription.size(), layerFields)

def layerLoopBody(layerDescription, layerEmbedding, cellState):
    layerSize = layerEmbedding.shape[1].value

    cell = tf.nn.rnn_cell.LSTMCell(layerSize)

    print "layerDescription ", layerDescription
    print "layerEmbedding ", layerEmbedding
    print "cellState ", cellState

    cellOutput, cellState = cell(layerEmbedding, cellState)

    layerDescription.write(layerDescription.size(), cellOutput)

    return layerDescription, layerEmbedding, cellState

def buildLayer(layerEmbedding, configuration):
    layerSize = layerEmbedding.shape[1].value

    print "layerSize ", layerSize

    cellState = tf.nn.rnn_cell.LSTMCell(layerSize).zero_state(
        batch_size=tf.shape(layerEmbedding)[0],
        dtype=layerEmbedding.dtype)

    layerDescription = tf.TensorArray(getDataType(configuration), (0), dynamic_size=True)

    layerDescription, _, _ = tf.while_loop(layerLoopCondition, layerLoopBody,
        [layerDescription, layerEmbedding, cellState])

    return layerDescription.stack()

def buildLayerConnections(networkDescription, networkEmbedding, layerEmbedding, configuration):
    previousLayerDescriptionCount = networkDescription.size()
    previousLayerDescriptions = networkDescription.stack()

    print " layerEmbedding ", layerEmbedding
    print " networkEmbedding ", networkEmbedding

    batchSize = tf.shape(networkEmbedding)[0]

    layerAndNetworkEmbedding = tf.concat([networkEmbedding, layerEmbedding], axis=1)

    combinedLayerFeatures = tf.tile(tf.reshape(layerAndNetworkEmbedding,
        (1, batchSize, layerAndNetworkEmbedding.shape[1].value)),
        [previousLayerDescriptionCount, 1, 1])

    combinedFeatures = tf.concat([combinedLayerFeatures, previousLayerDescriptions], axis=1)

    connections = tf.contrib.layers.fully_connected(combinedFeatures, Schema.MAXIMUM_LAYERS)

    return connections


def controllerLoopBody(networkDescription, inputNetworkDescription, stopCondition, configuration):
    # generate network embedding
    networkEmbedding = buildNetworkEmbedding(inputNetworkDescription, configuration)
    print " networkEmbedding ", networkEmbedding

    # generate layer embedding
    layerEmbedding = buildLayerEmbedding(networkEmbedding, configuration)
    print " layerEmbedding ", layerEmbedding

    # generate layer
    newLayerDescription = buildLayer(layerEmbedding, configuration)

    # generate connections
    connections = buildLayerConnections(networkDescription,
        layerEmbedding, networkEmbedding, configuration)

    # update the stop condition
    stopCondition = buildStopCondition(networkEmbedding, layerEmbedding, configuration)

    completeLayerDescription = tf.concat([newLayerDescription, connections], dim=1)

    networkDescription.write(networkDescription.size(), completeLayerDescription)

    return networkDescription, inputNetworkDescription, stopCondition, configuration

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
        stopCondition = tf.constant(0.0)

        networkDescription = tf.TensorArray(self.getDataType(), (Schema.TOTAL_FEATURES))

        networkDescription, _, _ = tf.while_loop(
            self.getControllerLoopCondition(),
            self.getControllerLoopBody(),
            [networkDescription, self.getControllerInput(), stopCondition])

        self.controllerOperation = networkDescription

    def getControllerLoopBody(self):
        return lambda x, y, z : controllerLoopBody(x, y, z, self.configuration)

    def getControllerLoopCondition(self):
        return lambda x, y, z : controllerLoopCondition(x, y, z, self.configuration)

    def buildControllerInput(self):
        return tf.placeholder(self.getDataType(), shape=[None, None, Schema.TOTAL_FEATURES])

    def getDataType(self):
        return getDataType(self.configuration)

    def getControllerInput(self):
        return self.controllerInput

    def trainOnBatch(self, originalModel, newModel, reward):
        self.session.run(self.getUpdateRule(), feed_dict=
            {
                self.getControllerInput() : self.getFeatures(originalModel),
                self.getControllerOutput() : self.getFeatures(newModel),
                self.getReward() : reward
            })




