
class ModelDescriptionSerializer:
    def __init__(self, jsonDescription):
        self.jsonDescription = jsonDescription

    def toTensor(self):
        entryCount = self.getEntryCount()

        tensorDescription = numpy.zeros((Schema.TOTAL_FEATURES, entryCount))

        self.writeSystemDescription(tensorDescription)
        self.writeProblemDescription(tensorDescription)
        self.writeInputFormatDescription(tensorDescription)
        self.writeOutputFormatDescription(tensorDescription)
        self.writeLayerDescriptions(tensorDescription)

        return tensorDescription

    def getEntryCount(self):
        headerEntryCount = int(2 + # 2 for the system description
                   1 + # 1 for the problem type
                   2 + # 2 for the input description
                   2) # 2 for the output description

        layerEntryCount = 0

        for layerDescription : self.jsonDescription["layers"]:
            layerEntryCount += self.getLayerEntryCount(layerDescription)

        return headerEntryCount + layerEntryCount

    def getLayerEntryCount(self, layerDescription):
        layerEntryCount = 2 # 1 for type, 1 for connections

        if "size" in layerDescription:
            layerEntryCount += 1

        if "stride" in layerDescription:
            layerEntryCount += 1

        if "filter" in layerDescription:
            layerEntryCount += 1

        return layerEntryCount

    def writeSystemDescription(self, tensorDescription):
        architecture = self.jsonDescription["system"]["architecture"]

        tensorDescrition[Schema.getArchitectureSectionBegin() +
            Schema.getOffset(Schema.ARCHITECTURES, architecture), 0] = 1.0

        microarchitecture = self.jsonDescription["system"]["microarchitecture"]

        tensorDescrition[Schema.getMicroArchitectureSectionBegin() +
            Schema.getOffset(Schema.MICROARCHITECTURES, microarchitecture), 1] = 1.0

    def writeProblemDescription(self, tensorDescription):
        problemType = self.jsonDescription["problem-type"]["black-white-pixels"]

        tensorDescrition[Schema.getProblemTypeSectionBegin() +
            Schema.getOffset(Schema.PROBLEM_TYPE, problemType), 2] = 1.0

    def writeInputFormatDescription(self, tensorDescription):
        self.writeFormatDescription(tensorDescription, 3)

    def writeOutputFormatDescription(self, tensorDescription)
        self.writeFormatDescription(tensorDescription, "input-", 5)

    def writeFormatDescription(self, tensorDescription, prefix, index)
        dimensions = self.jsonDescription[prefix + "format"]["dimensions"]

        tensorDescrition[Schema.getFormatDimensionsSectionBegin() +
            Schema.getOffset(Schema.FORMAT_DIMENSION, dimensions), index] = 1.0

        typeName = self.jsonDescription[prefix + "format"]["type"]

        tensorDescrition[Schema.getFormatDimensionsSectionBegin() +
            Schema.getOffset(Schema.FORMAT_TYPE, typeName), index + 1] = 1.0

    def writeLayerDescriptions(self, tensorDescription):
        nextIndex = 7
        existingLayers = {}

        for layerDescription in self.jsonDescription["layers"]:
            self.writeLayerDescription(tensorDescrition, existingLayers,
                layerDescription, nextIndex)
            nextIndex += self.getLayerEntryCount(layerDescription)


    def writeLayerDescription(self, tensorDescription, existingLayers,
        layerDescription, nextIndex):

        typeName = layerDescription["type"]

        tensorDescrition[Schema.getLayerTypesSectionBegin() +
            Schema.getOffset(Schema.LAYER_TYPES, typeName), nextIndex] = 1.0

        nextIndex += 1

        if "size" in layerDescription:
            size = layerDescription["size"]

            tensorDescrition[Schema.getLayerSizesSectionBegin() +
                Schema.getOffset(Schema.LAYER_SIZES, size), nextIndex] = 1.0

            nextIndex += 1

        if "stride" in layerDescription:
            stride = layerDescription["stride"]

            tensorDescrition[Schema.getLayerStridesSectionBegin() +
                Schema.getOffset(Schema.LAYER_STRIDES, stride), nextIndex] = 1.0

            nextIndex += 1

        if "filter" in layerDescription:
            filterSize = layerDescription["filter"]

            tensorDescrition[Schema.getLayerFilterSectionBegin() +
                Schema.getOffset(Schema.LAYER_FILTER, filterSize), nextIndex] = 1.0

            nextIndex += 1

        for inputName in layerDescription["inputs"]:
            assert inputName in existingLayers
            tensorDescrition[Schema.getConnectionsSectionBegin() + existingLayers[inputName]] = 1.0

        existingLayers[layerName] = len(existingLayers)



