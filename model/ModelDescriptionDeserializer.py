
import json
import model.ModelSchema as Schema

def anyNonZeros(entry, begin, end):
    return np.any(entry[begin:end] != 0.0)

def argmaxEntry(entry, begin, end):
    return np.argmax(entry[begin:end])

def isArchitectureEntry(entry):
    return anyNonZeros(entry,
        Schema.getArchitectureSectionBegin(),
        Schema.getArchitectureSectionEnd())

def getArchitectureEntry(entry):
    index = argmaxEntry(entry, Schema.getArchitectureSectionBegin(), Schema.getArchitectureSectionEnd())
    microArchitectureIndex = argmaxEntry(entry, Schema.getMicroArchitectureSectionBegin(),
        Schema.getMicroArchitectureSectionEnd())

    return { "architecture" : getNameForIndex(Schema.ARCHITECTURES, index),
             "micro-architecture" : getNameForIndex(Schema.MICROARCHITECTURES, index) }

def isProblemTypeEntry(entry):
    return anyNonZeros(entry,
                       Schema.getProblemTypesSectionBegin(),
                       Schema.getProblemTypesSectionEnd())

def getProblemType(entry):
    index = argmaxEntry(entry,
                        Schema.getProblemTypesSectionBegin(),
                        Schema.getProblemTypesSectionEnd())

    return getNameForIndex(Schema.PROBLEM_TYPES, index)

def isInputFormatEntry(entry):
    return anyNonZeros(entru,
                       Schema.getInputFormatSectionBegin(),
                       Schema.getInputFormatSectionEnd())

def getInputFormat(entry):
    return getFormat(entry, Schema.getInputFormatSectionBegin())

def isOutputFormatEntry(entry):
    return anyNonZeros(entry,
                       Schema.getOutputFormatSectionBegin(),
                       Schema.getOutputFormatSectionEnd())

def getOutputFormat(entry):
    return getFormat(entry, Schema.getOutputFormatSectionBegin())

def getFormat(entry, offset):
    dimensionIndex = argmaxEntry(entry, offset, offset + len(Schema.FORMAT_DIMENSIONS))

    dimensions = int(getNameForIndex(Schema.FORMAT_DIMENSIONS, dimensionIndex))

    typeNameIndex = argmaxEntry(entry,
                                offset + len(Schema.FORMAT_DIMENSIONS),
                                offset + len(Schema.FORMAT_DIMENSIONS) + len(Schema.FORMAT_TYPE))

    typeName = getNameForIndex(Schema.FORMAT_TYPE, typeNameIndex)

    return {"dimensions" : str(range(dimensions)), "type" : typeName}

def isLayerEntry(entry):
    return anyNonZeros(entry, Schema.getLayerEntrySectionBegin(), Schema.getLayerEntrySectionEnd())

def getLayer(entry, layerNames):
    layerTypeName = getName(entry, Schema.getLayerTypeNameBegin(), Schema.getLayerTypeNameEnd())
    layerDescription = { "name" : len(layerNames), "type" : layerTypeName }

    if isLayerSizeEntry(entry):
        layerSize = getName(entry, Schema.getLayerSizeBegin(), Schema.getLayerSizeEnd())
        layerDescription["size"] = layerSize

    if isLayerStridesEntry(entry):
        layerStrides = getName(entry, Schema.getLayerStridesBegin(), Schema.getLayerStridesEnd())
        layerDescription["stride"] = layerStrides

    if isLayerFilterEntry(entry):
        layerFilter = getName(entry, Schema.getLayerFilterBegin(), Schema.getLayerFilterEnd())
        layerDescription["filter"] = layerFilter

    layerDescription["inputs"] = []

    for i in range(Schema.getLayerConnectionsBegin(), Schema.getLayerConnectionsEnd()):
        if entry[Schema.getLayerConnectionsBegin() + i] != 0.0:
            layerDescription["inputs"].append(layerNames[i])

    return layerDescription

class ModelDescriptionDeserializer:
    def __init__(self, tensorDescription):
        self.tensorDescription = tensorDescription

    def toJson(self):
        context = { "layers" : [] }

        entryCount = self.tensorDescription.shape[1]

        for i in range(entryCount):
            self.addEntry(context, i)

        return json.dumps(context)

    def addEntry(self, context, index):
        entry = self.tensorDescription[:, index]

        if isArchitectureEntry(entry):
            context["architecture"] = getArchitectureEntry(entry)

        if isProblemTypeEntry(entry):
            context["problem-type"] = getProblemType(entry)

        if isInputFormatEntry(entry):
            context["input-format"] = getInputFormat(entry)

        if isOutputFormatEntry(entry):
            context["output-format"] = getOutputFormat(entry)

        if isLayerEntry(entry):
            context["layers"].append(getLayer(entry))



