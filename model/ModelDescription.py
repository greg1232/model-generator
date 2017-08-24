
#
# Schema
#
# {
#   "input-format" : { "dimensions": [], "type": "float32"}
#   "output-format": { "dimensions": [], "type": "float32"}
#
#
#   "layers" : [ { "name" : "fc0",  "type" : "fully-connected", "size" : "32", "input" : "network-input", "output" : "nonlinear0"  },
#                { "name" : "nonlinear0",  "type" : "relu", "output" : "conv0" },
#                { "name" : "conv0", "type" : "conv2d", size : "32", stride : "2", filter : "3" },
#                { "name" : "nonlinear1",  "type" : "relu", "output" : "network-output"  } ]
# }
#
# feature space
#  0. architecture
#       1. [gpu, cpu, fpga, asic]
#           1. gpu [invalid, kepler, maxwell, pascal, volta, vega, knl, knm]
#           2. cpu [skylake, coffee lake]
#  1. problem type
#       1. class [color-pixels, black-white-pixels, waveform, spectogram, characters]
#  2. input format
#       1. dimensions: [1, 2, 3, 4]
#       2. type: [float16, float32]
#  3. output format
#       1. dimensions: [1, 2, 3, 4]
#  4. layer
#       1. type [invalid, gemm, relu, tanh, sigmoid, mul, add, conv2d, lstm, one, zero]
#       2. size [32, 256, 1024, 4096]
#       3. stride [1, 2, 4, 8]
#       3. filter [1, 3, 5, 7]
#       4. connections [0...max-layers]

from model.ModelDescriptionSerializer   import ModelDescriptionSerializer
from model.ModelDescriptionDeserializer import ModelDescriptionDeserializer

class ModelDescription:
    def __init__(self):
        self.json = None

    def setFromJSON(self, json):
        self.json = json

    def setFromTensor(self, description):
        self.json = ModelDescriptionSerializer(description).toJson()

    def getJSON(self):
        return self.json

    def getTensor(self):
        return ModelDescriptionDeserializer(self.json).toTensor()


