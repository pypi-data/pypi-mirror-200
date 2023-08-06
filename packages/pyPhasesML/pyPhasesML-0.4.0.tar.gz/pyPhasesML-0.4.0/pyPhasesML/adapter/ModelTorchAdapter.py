import gc
import math
import os
import timeit

import numpy as np
import psutil
import torch
import torch.optim as optim
from tqdm import tqdm

from ..DataSet import DataSet, TrainingSet
from ..Model import Model
from ..scorer.ScorerTorch import ScorerTorch


class ModelTorchAdapter(Model):
    model: torch.nn.Module
    useGPU = torch.cuda.is_available()
    useTensorBoard = False
    saveOnlyWeights = True
    findLearningRate = False
    oneCyclicLR = False
    cycleLR = False
    cycleLRFactor = 4
    cycleLRStepsideFactor = 2
    cycleLRMax = 2
    findLearningRatePlot = "data/learningRate.png"

    def _metrics(self, metric):
        return "val_" + metric["name"]

    def prepareX(self, x, validation=False):
        x = x.permute(0, 2, 1)
        return x

    def prepareY(self, y, validation=False):
        return y

    def init(self):
        self.weightTensors = None if self.classWeights is None else torch.from_numpy(np.array(self.classWeights))
        if self.useGPU and self.weightTensors is not None:
            self.weightTensors = self.weightTensors.cuda()

    def prepareDataAdapter(self, datasetOrTuple, validation=False):
        x, y = datasetOrTuple

        if not torch.is_tensor(x):
            x = torch.tensor(x)
        if not torch.is_tensor(y):
            y = torch.tensor(y)

        dataset = DataSet(x, y)

        if self.useGPU:
            dataset.x = dataset.x.cuda()
            dataset.y = dataset.y.cuda()

        return self.prepareData(dataset, validation)

    def remapLabels(self, categorizedArray):
        ones = torch.sparse.torch.eye(len(self.numClasses))
        return ones.index_select(0, categorizedArray)

    def evalValidation(self, validationData):
        model = self.model
        model.eval()
        s = ScorerTorch(self.numClasses, trace=True)
        # s = ScorerTorchEvent(self.numClasses, trace=True) if self.useEventScorer else ScorerTorch(self.numClasses, trace=True)
        s.metrics = self.validationMetrics
        s.trace = True
        s.ignoreClasses = [self.ignoreClassIndex] if self.ignoreClassIndex is not None else []

        validationData.transformToCategorical = 0
        batchCount = len(validationData)
        processList = tqdm(range(batchCount), disable=(not self.showProgress))
        processList.set_description("Validation")
        batchGenerator = iter(validationData)

        lastDimension = self.numClasses if self.oneHotDecoded else 1
        for batchIndex in processList:
            validationBatch = batchGenerator.__next__()
            x, y = self.prepareDataAdapter(validationBatch, validation=True)

            # Run model
            output = model(x)
            batchPredictions = self.mapOutputForPrediction(output)

            if len(s.metrics) > 0:
                y = y.reshape(-1, lastDimension)
                batchPredictions = batchPredictions.reshape(-1, lastDimension)

                results = s.score(y, batchPredictions, trace=True)

                processList.set_postfix({m: results[m] for m in s.metrics})

            del batchPredictions
            del x
            del y
            del output
            gc.collect()

        if len(s.metrics) > 0:
            results = s.scoreAllRecords()

            metrics = {m: results[m] for m in s.metrics}
            justPrint = []

            if "confusion" in s.results:
                justPrint.append(s.results["confusion"])

            return metrics, justPrint

        return None, None

    def prepareTargetsForLoss(self, targets, oneHotDecoded=None):
        oneHotDecoded = self.oneHotDecoded if oneHotDecoded is None else oneHotDecoded
        mask = None
        if oneHotDecoded:
            targets = targets.reshape(-1, self.numClasses)
            if self.ignoreClassIndex is not None:
                mask = targets.eq(0).sum(-1) < self.numClasses
                targets = targets[mask]
        else:
            targets = targets.reshape(-1)

            if self.ignoreClassIndex is not None:
                mask = targets != self.ignoreClassIndex
                targets = targets[mask]

        return targets.float(), mask

    def train(self, dataset: TrainingSet):
        if ModelTorchAdapter.useTensorBoard:
            from torch.utils.tensorboard import SummaryWriter

            self.summarywriter = SummaryWriter()

            for f, title in self.startFigures:
                self.summarywriter.add_figure(title, f)
        else:
            self.summarywriter = None
        self.cleanCsv()

        metrics = self.validationMetrics
        scorer = ScorerTorch(self.numClasses)
        metricDefinitions = {m: scorer.getMetricDefinition(m) for m in metrics}

        model = self.model
        globalBestMetric = self.validationMetrics[0]
        self.batchScheduler = None

        self.log("LR: %s" % self.learningRate)
        if self.optimizer == "adams":
            decay = 0 if self.learningRateDecay is None else self.learningRateDecay
            self.optimizer = optim.Adam(model.parameters(), lr=self.learningRate, weight_decay=decay)
        if self.optimizer == "nadams":
            decay = 0 if self.learningRateDecay is None else self.learningRateDecay
            torch.optim.NAdam(model.parameters(), lr=self.learningRate, momentum_decay=decay)
        elif type(self.optimizer) == str:
            raise Exception("optimizer %s is currently not supported for pytorch implementation" % self.optimizer)

        if self.cycleLR:
            lr = self.learningRate / self.cycleLRFactor
            lrMax = self.learningRate
            stepSize = self.cycleLRStepsideFactor * len(dataset.trainingData)

            self.batchScheduler = torch.optim.lr_scheduler.CyclicLR(
                self.optimizer, base_lr=self.learningRate / lr, max_lr=lrMax, step_size_up=stepSize
            )

        if self.oneCyclicLR:
            lr = self.learningRate / self.cycleLRFactor
            lrMax = self.learningRate
            steps = self.maxEpochs * len(dataset.trainingData)

            self.batchScheduler = torch.optim.lr_scheduler.OneCycleLR(self.optimizer, max_lr=lrMax, total_steps=steps)

        if self.findLearningRate:
            start_lr = self.learningRate
            end_lr = self.cycleLRMax
            lr_lambda = lambda x: math.exp(x * math.log(end_lr / start_lr) / (self.maxEpochs * len(dataset.trainingData)))
            self.batchScheduler = torch.optim.lr_scheduler.LambdaLR(self.optimizer, lr_lambda)
            lr_find_loss = []
            lr_find_lr = []
            smoothing = 0.05

        model = self.model
        lossCriterion = self.getLossFunction()
        i_epoch = self.startEpoch
        notImprovedSince = 0
        lastImprovdModel = None

        stopAfterNotImproving = 0 if self.stopAfterNotImproving is None else self.stopAfterNotImproving

        while self.maxEpochs is None or i_epoch < self.maxEpochs:
            # Put in train mode
            trainingStartTime = timeit.default_timer()

            model.train(True)
            runningStats = {"loss": 0.0}
            batchesPerEpoch = len(dataset.trainingData)
            processList = tqdm(range(batchesPerEpoch), disable=(not self.showProgress))
            processList.set_description("EPOCH {}".format(i_epoch))
            batchGenerator = iter(dataset.trainingData)

            for batchIndex in processList:
                trainBatch = next(batchGenerator)
                batchFeats, targs = self.prepareDataAdapter(trainBatch)
                targs, mask = self.prepareTargetsForLoss(targs)

                self.optimizer.zero_grad()

                # check if there are any targets left
                if len(targs) == 0:
                    continue

                # for batchFeat in batchFeats:
                output = model(batchFeats)
                output = self.mapOutputForLoss(output, mask)
                loss = lossCriterion(output, targs)
                ownStats = hasattr(lossCriterion, "stats")

                if ownStats:
                    processList.set_postfix(ordered_dict=lossCriterion.stats)
                    for stat, value in lossCriterion.stats.items():
                        if stat not in runningStats:
                            runningStats[stat] = value
                        else:
                            runningStats[stat] += value

                # Backpropagation
                loss.backward()
                # torch.nn.utils.clip_grad()
                self.optimizer.step()

                # Perform one optimization step
                currentBatchLoss = loss.data.cpu().numpy()
                if np.isnan(currentBatchLoss):
                    model(batchFeats)
                    lossCriterion(output, targs)
                    raise Exception("batch loss should not be a number")

                if self.batchScheduler is not None:
                    self.batchScheduler.step()

                if self.findLearningRate:
                    lr_step = self.optimizer.state_dict()["param_groups"][0]["lr"]
                    lr_find_lr.append(lr_step)

                    # smooth the loss
                    if batchIndex == 0 and i_epoch == 0:
                        lr_find_loss.append(loss)
                    else:
                        loss = smoothing * loss + (1 - smoothing) * lr_find_loss[-1]
                        lr_find_loss.append(loss)

                runningStats["loss"] += currentBatchLoss

                del output
                del targs
                del loss
                gc.collect()
                currentCount = processList.n + 1
                processList.set_postfix(ordered_dict={n: v / currentCount for n, v in runningStats.items()})

            runningStats = {n: v / batchesPerEpoch for n, v in runningStats.items()}

            i_epoch += 1
            trainingEndTime = timeit.default_timer()

            # Get validation accuracy
            metricsValues, justPrint = self.evalValidation(dataset.validationData)

            metricStrings = []
            metricDiffStrings = []
            metricValuetrings = []
            improved = False
            modelId = "checkpointModel_%i_" % i_epoch

            for metricName, metricVal in metricsValues.items():
                bestValue, useAsBest, biggerIsBetter = metricDefinitions[metricName]
                diff = metricVal - bestValue
                metricStrings.append(metricName + ": " + "{:.3f}".format(metricVal) + " [best: {:.3f}]".format(bestValue))
                metricDiffStrings.append(metricName + ": " + "{:.3f}".format(diff))
                metricValuetrings.append("{:.3f}".format(metricVal))

                if self.summarywriter is not None:
                    self.summarywriter.add_scalar(metricName, metricVal, global_step=self.fullEpochs)

                isBigger = metricVal > bestValue

                if (biggerIsBetter and isBigger) or (not biggerIsBetter and not isBigger):
                    metricDefinitions[metricName][0] = metricVal
                    if useAsBest:
                        improved = True

            validationEndTime = timeit.default_timer()

            self.log(
                "Validation-Epoch Number: "
                + str(i_epoch)
                + "  Training Time: "
                + str(trainingEndTime - trainingStartTime)
                + "  Validation Time: "
                + str(validationEndTime - trainingEndTime)
            )
            for p in justPrint:
                self.log(p)

            trainingStats = " | ".join(["%s:%s" % (n, v) for n, v in runningStats.items()])
            self.log("Training Stats: %s " % (trainingStats))
            self.log(" ".join(metricStrings))
            # acc_train = correct / total
            # self.summarywriter.add_scalar("train_loss", runningLoss, global_step=self.fullEpochs)
            # self.summarywriter.add_scalar("train_acc", acc_train, global_step=self.fullEpochs)

            process = psutil.Process(os.getpid())
            self.log("memory usage: %sM" % (process.memory_info().rss / 1024 / 1024))

            csvRow = {
                "epoch": i_epoch,
            }
            csvRow.update(runningStats)

            for metricName in metricsValues:
                csvRow["val_%s" % metricName] = metricsValues[metricName]

            self.addCsvRow(csvRow)
            self.bestMetric = max(self.bestMetric, metricsValues[globalBestMetric])

            # If the validation accuracy improves, print out training and validation accuracy values and checkpoint the model
            if improved:
                self.log("Model Improved: " + " ".join(metricDiffStrings))
                f = open(
                    self.getModelPath() + "/" + modelId + "_".join(metricValuetrings) + ".pkl",
                    "wb",
                )
                # self.trigger("modelImproved", model)
                torch.save(model.state_dict() if ModelTorchAdapter.saveOnlyWeights else model, f)
                f.close()
                notImprovedSince = 0
                lastImprovdModel = model
            else:
                notImprovedSince += 1
                self.log("Model not improving since %i epochs" % (notImprovedSince))

            if stopAfterNotImproving > 0 and notImprovedSince >= stopAfterNotImproving:
                break

        if self.findLearningRate:
            lr_find_loss = [l.data.cpu().numpy() for l in lr_find_loss]
            from matplotlib import pyplot as plt
            plt.ylabel("loss")
            plt.xlabel("loss")
            plt.xscale("log")
            plt.plot(lr_find_lr, lr_find_loss)
            plt.savefig(self.findLearningRatePlotPath)
            minLr = lr_find_lr[np.argmin(lr_find_loss)]
            print("Lowest Loss LR: %f" % minLr)
            print("Suggested LR range max bound: %f" % minLr)
            self.lr_find_lr = lr_find_lr
            self.lr_find_loss = lr_find_loss

        self.csvClose()
        self.fullEpochs = i_epoch
        return lastImprovdModel

    def getModelPath(self):
        return self.logPath

    def build(self):
        torchSeed = 2
        torch.manual_seed(torchSeed)

        if self.useGPU:
            torch.cuda.manual_seed(torchSeed)
            self.model.cuda()

    def summary(self):
        pytorch_total_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        self.log("Total trainable Parameters: %i" % (pytorch_total_params))
        self.parameter = pytorch_total_params

        return str(self.model)

    def cleanUp(self):
        if self.useGPU:
            torch.cuda.empty_cache()

    def save(self, path):
        torch.save(self.model.state_dict(), path)

    def load(self, path):
        return torch.load(path, map_location=torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    def loadState(self, state):
        if isinstance(state, torch.nn.Module):
            state = state.state_dict()
        return self.model.load_state_dict(state)

    def mapOutputForLoss(self, output, mask=None):
        output = output.reshape(-1, self.numClasses) if self.oneHotDecoded else output.flatten()
        return output[mask] if mask is not None else output

    def predict(self, input, get_likelihood=False, returnNumpy=True):
        with torch.no_grad():
            if not torch.is_tensor(input):
                input = torch.tensor(input)

            batchSize, _, _ = input.shape

            if self.useGPU:
                input = input.cuda()

            input = self.prepareX(input)
            model = self.getModelEval()
            out = model(input)

            predictions = self.mapOutputForPrediction(out)

            if self.numClasses > 0 and self.oneHotDecoded:
                predictions = predictions.reshape(batchSize, -1, self.numClasses)

                if not get_likelihood:
                    predictions = torch.argmax(predictions, dim=2)

            if returnNumpy:
                predictions = predictions.detach().cpu().numpy()

            return predictions
