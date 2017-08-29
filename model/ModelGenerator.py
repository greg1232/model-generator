

import tensorflow as tf

class ModelGenerator:
    def __init__(self, modelDescription, modelInput):
        self.modelDescription = modelDescription

        self.input  = modelInput

    def getModelDescription(self):
        return self.modelDescription

    def buildModel(self):
        # build the graph of layers
        layers = {}

        layerDescriptions = self.modelDescription["layers"]

        for layerDescription : layerDescriptions:
            self.buildLayer(layers, layerDescription)

        # return the output of the network
        lastLayerName = layerDescriptions[-1]["name"]

        return layers[lastLayerName]

    def buildLayer(self, layers, layerDescription):
        layerType = layerDescription["type"]
        layerName = layerDescription["name"]

        output = None

        if layerType == "fully-connected":
            inputs = self.getSimpleInputs(layers, layerDescription)
            layerSize = int(layerDescription["size"])
            output = tf.nn.fully_connected(inputs, layerSize)
        else if layerType == "relu":
            inputs = self.getSimpleInputs(layers, layerDescription)
            output = tf.nn.relu(inputs)
        else if layerType == "tanh":
            inputs = self.getSimpleInputs(layers, layerDescription)
            output = tf.nn.tanh(inputs)
        else if layerType == "sigmoid":
            inputs = self.getSimpleInputs(layers, layerDescription)
            output = tf.nn.sigmoid(inputs)
        else if layerType == "mul":
            inputs = self.getBinaryInputs(layers, layerDescription)
            output = tf.mul(inputs[0], inputs[1])
        else if layerType == "add":
            inputs = self.getBinaryInputs(layers, layerDescription)
            output = tf.add(inputs[0], inputs[1])
        else if layerType == "ones":
            layerSize = int(layerDescription["size"])
            output = tf.ones(layerSize)
        else if layerType == "zeros":
            layerSize = int(layerDescription["size"])
            output = tf.zeros(layerSize)
        else if layerType == "conv2d":
            layerSize = int(layerDescription["size"])
            layerStride = int(layerDescription["stride"])
            layerFilterSize = int(layerDescription["filter"])
            inputs, padding = self.getSimple2DInputsAndPadding(layers,
                layerDescription, layerFilterSize)
            self.fixInputsForConv2d(inputs)
            filterWeights = self.makeConv2dFilterWeights(inputs, layerSize,
                layerStride, layerFilterSize)
            output = tf.conv2d(inputs, filterWeights, self.getConv2dStrides(layerStride), padding)

        layer[layerName] = output

    def getSimpleInputs(self, layers, layerDescription):
        inputName = layerDescription[""]

        if inputName == "network-input":
            return self.input

        return layers[inputName]

