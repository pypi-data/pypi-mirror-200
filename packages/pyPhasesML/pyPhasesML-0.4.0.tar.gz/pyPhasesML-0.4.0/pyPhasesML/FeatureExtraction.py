from pyPhases import classLogger
from pyPhasesRecordloader import RecordSignal, Signal


@classLogger
class FeatureExtraction:

    def step(self, stepname, recordSignal, **options):
        if hasattr(self, stepname):
            # call method
            return getattr(self, stepname)(recordSignal, **options)
        else:
            raise Exception(f"FeatureExtraction '{stepname}' not found")

    def __call__(self, recordSignal, config=None):
        return self.extractChannelsByConfig(recordSignal, config)

    def extractChannelsByConfig(self, recordSignal, config):

        for c in config:
            self.extractChannelByConfig(recordSignal, c)

    def addSingle(self, name, recordSignal: RecordSignal, signalOrArray):
        if not isinstance(signalOrArray, Signal):
            signalOrArray = Signal(name, signalOrArray, frequency=recordSignal.targetFrequency)
        signalOrArray.name = name
        recordSignal.addSignal(signalOrArray, name)

    def extractChannelByConfig(self, recordSignal, config):
        config = config.copy()
        name = config["name"]
        channels = config["channels"]
        del config["name"]
        del config["channels"]

        ret = self.step(name, recordSignal, **config)

        if len(channels) > 1:
            for index, signal in enumerate(ret):
                self.addSingle(channels[index], recordSignal, signal)
        elif ret is not None:
            self.addSingle(channels[0], recordSignal, ret)
        
