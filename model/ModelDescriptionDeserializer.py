
import json
import model.ModelSchema as Schema

def getArchitectureSectionBegin():
    return 0

def getArchitectureSectionEnd():
    return getArchitectureSectionBegin() + len(Schema.ARCHITECTURES)

def getProblemTypesSectionBegin():
    return getArchitectureSectionEnd()

def getProblemTypesSectionEnd():
    return getProblemTypesSectionBegin + len(Schema.PROBLEM_TYPES)

def isArchitectureEntry(entry):
    return anyNonZeros(entry, getArchitectureSectionBegin(), getArchitectureSectionEnd())

def getArchitectureEntry(entry):
    index = argmaxEntry(entry, getArchitectureSectionBegin(), getArchitectureSectionEnd())
    microArchitectureIndex = argmaxEntry(entry, getMicroArchitectureSectionBegin(),
        getMicroArchitectureSectionEnd())

    return { "architecture" : getNameForIndex(Schema.ARCHITECTURES, index),
             "micro-architecture" : getNameForIndex(Schema.MICROARCHITECTURES, index) }

def isProblemTypeEntry(entry):
    return anyNonZeros(entry, getProblemTypesSectionBegin(), getProblemTypesSectionEnd())

def getProblemType(entry):
    index = argmaxEntry(entry, getProblemTypesSectionBegin(), getProblemTypesSectionEnd())

    return getNameForIndex(Schema.PROBLEM_TYPES, index)

def isInputFormatEntry(entry):
    return anyNonZeros(entru, getInputFormatSectionBegin(), getInputFormatSectionEnd())

def getInputFormat(entry):
    return getFormat(entry, getInputFormatSectionBegin())

def isOutputFormatEntry(entry):
    return anyNonZeros(entru, getOutputFormatSectionBegin(), getOutputFormatSectionEnd())

def getOutputFormat(entry):
    return getFormat(entry, getOutputFormatSectionBegin())

def isLayerEntry(entry):


class ModelDescriptionDeserializer:
    def __init__(self, tensorDescription):
        self.tensorDescription = tensorDescription

    def toJson(self):
        context = { "layers" : [] }

        entryCount = self.tensorDescription.shape[1]

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



