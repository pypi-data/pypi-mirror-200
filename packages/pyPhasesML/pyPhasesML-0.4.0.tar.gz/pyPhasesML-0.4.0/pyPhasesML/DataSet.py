import math
from collections.abc import Iterable
from dataclasses import astuple, dataclass

import numpy as np


class ValidDataset:
    pass


@dataclass
class DataSet:
    x: np.array
    y: np.array
    numClasses: int = None
    catMatrix = None

    def __len__(self):
        return 2

    @staticmethod
    def fromTuple(data, numClasses=None):
        x, y = data
        return DataSet(x, y, numClasses)

    def asTuple(self):
        return astuple(self)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        if index == 2:
            raise StopIteration
        raise TypeError("Datset can only be split in x and y, try to get index %i" % (index))


class DataSetContinous(ValidDataset):
    def __len__(self):
        return self.recordCount if self.recordWise else self.batchCount

    def __init__(
        self,
        batchFunction,
        batchCount=None,
        recordCount=None,
        numClasses=None,
        getSingleRecord=None,
    ) -> None:
        self.batchFunction = batchFunction
        self.batchCount = batchCount
        self.recordCount = recordCount
        self.numClasses = numClasses
        self.continous = True
        self.index = 0
        self.recordWise = False
        self.getSingleRecord = getSingleRecord
        self.augmentation = True
        self.function = None
        self.distinct = True
        if self.recordWise and self.recordCount is None:
            self.recordCount = len(batchFunction)
        if not self.recordWise and self.batchCount is None:
            self.batchCount = len(batchFunction)

    def getFunction(self):
        if self.function is None:
            if callable(self.batchFunction):
                self.function = self.batchFunction(recordWise=self.recordWise, augmentation=self.augmentation)
            else:
                self.function = iter(self.batchFunction)
        return self.function

    def nonContinous(self):
        self.continous = False

    def __next__(self):
        if not self.continous and self.index == len(self):
            raise StopIteration

        dataTuple = self.getFunction().__next__()
        batch = DataSet.fromTuple(dataTuple, numClasses=self.numClasses)
        self.index += 1
        return batch

    def __iter__(self):
        self.function = None
        self.getFunction().__iter__()
        self.index = 0
        return self

    def generator(self, wrapper=None):
        while True:
            ret = self.__next__()
            wrapper = (lambda x: x) if wrapper is None else wrapper
            yield wrapper(ret)

    def __getitem__(self, index):
        dataTuple = self.getSingleRecord(index)
        batch = DataSet.fromTuple(dataTuple, numClasses=self.numClasses)
        return batch


class TrainingSetLoader:
    def __init__(self, trainingData=None, validationData=None):
        self.trainingData: DataSet = trainingData
        self.validationData: DataSet = validationData


class TrainingSet:
    def __init__(
        self,
        trainingData=None,
        validationData=None,
        numClasses=None,
        useContinous=True,
        distinct=True,
    ) -> None:

        self.trainingData: DataSet = None
        self.validationData: DataSet = None
        self.transformChannelLast = False

        if isinstance(trainingData, ValidDataset):
            self.trainingData = trainingData
        elif isinstance(trainingData, Iterable) and useContinous:
            self.trainingData = DataSetContinous(trainingData)
        else:
            self.trainingData = DataSet.fromTuple(trainingData, len(trainingData))

        if isinstance(validationData, ValidDataset):
            self.validationData = validationData
        elif isinstance(validationData, Iterable) and useContinous:
            self.validationData = DataSetContinous(validationData, len(validationData))
        else:
            self.validationData = DataSet.fromTuple(validationData)

        self.trainingData.distinct = distinct
        self.validationData.distinct = distinct

        self.trainingData.numClasses = numClasses
        self.validationData.numClasses = numClasses

    def toCategorical(self):
        self.trainingData.toCategorical()
        self.validationData.toCategorical()

    def getNextTrainingBatch(self):
        dataTuple = self.trainingData.__next__()
        batch = DataSet.fromTuple(dataTuple)
        return batch


class DatasetWrap(DataSetContinous):
    def __getitem__(self, index):
        return self.dataset[index]

    def __len__(self):
        return len(self.dataset)

    def __init__(self, dataset) -> None:
        self.dataset = dataset

    def nonContinous(self):
        self.continous = False

    def __next__(self):
        return self.dataset.__next__()

    def __iter__(self):
        return self.dataset.__iter__()

    def asTuple(self):
        return self


class DatasetWrapXY(ValidDataset):
    def __init__(self, dataset, batchSize=1) -> None:
        self.x, self.y = dataset
        self.batchSize = batchSize
        self.length = math.ceil(len(self.x) / self.batchSize)

    def __getitem__(self, index):
        if index >= self.length:
            raise IndexError
        s = slice(index * self.batchSize, (index + 1) * self.batchSize)
        return self.x[s], self.y[s]

    def __len__(self):
        return self.length

    def nonContinous(self):
        self.continous = False

    def generator(self, wrapper=None):
        while True:
            for d in self:
                wrapper = (lambda x: x) if wrapper is None else wrapper
                yield wrapper(DataSet.fromTuple(d))


class DatasetWrapItemGenerator(ValidDataset):
    def __init__(self, generator, lengths, batchSize=1) -> None:
        self.generator = generator
        self.length = lengths
        self.batchSize = batchSize

    def __len__(self):
        return self.length

    def nonContinous(self):
        self.continous = False

    def generator(self, wrapper=None):
        wrapper = (lambda x: x) if wrapper is None else wrapper
        yield wrapper(self.generator.__next__())

        batch = []
        curRecordsInBatch = 0

        while True:
            r = self.generator.__next__()
            batch.append(r)
            curRecordsInBatch += 1
            if curRecordsInBatch == self.batchSize:
                yield r
                batch = []
                curRecordsInBatch = 0


class DatasetWrapBatchGenerator(ValidDataset):
    def __init__(self, generator, length) -> None:
        self.generatorFunction = generator
        self.length = length
        self.index = 0

    def __len__(self):
        return self.length

    def generator(self, wrapper=None):
        if wrapper is None:
            while 1:
                yield next(self.generatorFunction)
        else:
            while 1:
                yield wrapper(next(self.generatorFunction))

    def __iter__(self):
        self.generatorFunction.__iter__()
        self.index = 0
        return self

    def __next__(self):
        if self.index == self.length:
            raise StopIteration
        self.index += 1
        return next(self.generatorFunction)
