
import json
import model.ModelSchema as Schema


def getArchitectureSectionBegin():
    return 0

def getArchitectureSectionEnd():
    return getArchitectureSectionBegin() + len(Schema.architectures)

def isArchitectureEntry(entry):
    anyNonZeros(entry, getArchitectureSectionBegin(), getArchitectureSectionEnd())

def getArchitectureEntry(entry):
    index = argmaxEntry(entry, getArchitectureSectionBegin(), getArchitectureSectionEnd())
    microArchitectureIndex = argmaxEntry(entry, getMicroArchitectureSectionBegin(),
        getMicroArchitectureSectionEnd())

    return { "architecture" : getNameForIndex(Schema.architectures, index),
             "micro-architecture" : getNameForIndex(Schema.microarchitectures) }

class ModelDescriptionDeserializer:
    def __init__(self, tensorDescription):
        self.tensorDescription = tensorDescription

    def toJson(self):
        context = { "layers" : [] }

        entryCount = self.tensorDescription.shape[0]

        for i in entryCount:
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



