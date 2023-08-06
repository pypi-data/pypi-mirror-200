import numpy as np
from sklearn.metrics import confusion_matrix


class Scorer:
    title = "Segmentbasiert"
    cmScaleByClass = 4

    metricNameMap = {}
    addedMetrics = {}

    def getMetricDefinition(self, name):

        metricDefinition = {
            # init value, useAsBest, biggerIsBetter
            "AUC": [0.5, False, True],
            "AP": [0.0, True, True],
            "accuracy": [0.0, False, True],
            "acc": [0.0, False, True],
            "kappa": [-1, True, True],
            "f1": [-1, True, True],
            "CSI": [0, True, True],
            "loss": [np.inf, True, False],
            "meanSquared": [np.inf, True, False],
            "SNR": [np.inf, False, False],
            "confusion": [np.inf, False, False],
            "auroc": [0.0, False, True],
            "auprc": [0.0, True, True],
            "eventCountDiff": [np.inf, False, False],
            "positiveErrorRatio": [np.inf, True, False],
        }

        if name in Scorer.addedMetrics:
            metric = Scorer.addedMetrics[name]
            return [metric["initValue"], metric["useAsBest"], metric["biggerIsBetter"]]

        return metricDefinition[name]

    @staticmethod
    def registerMetric(metricName, metricFunction, combineFunction, biggerIsBetter=True, useAsBest=True, initValue=None):

        Scorer.addedMetrics[metricName] = {
            "score": metricFunction,
            "combine": combineFunction,
            "biggerIsBetter": biggerIsBetter,
            "useAsBest": useAsBest,
            "initValue": initValue if initValue is not None else 0.0 if biggerIsBetter else np.inf,
        }

    def getMetricName(self, metricName):
        if metricName in Scorer.metricNameMap:
            metricName = Scorer.metricNameMap[metricName]
        return metricName

    def beforeLoss(self, x, y):
        """can be overwritten to tranform for a required format for the loss function"""
        return x, y

    def __init__(self, numClasses=None, classNames=None, trace=False, threshold=None) -> None:
        if numClasses is None and classNames is None:
            raise Exception("number of classes or list of classnames are required for scoring")

        self.metrics = ["kappa", "accuracy"]
        self.ignoreClasses = []
        self.numClasses = numClasses if classNames is None else len(classNames)
        self.classNames = [i for i in range(numClasses)] if classNames is None else classNames
        self.recordResult = {}
        self.recordIndex = 0
        self.trace = trace
        self.possibleValues = None
        self.lossF = None
        self.addEvents = False
        self.mapping = None
        self.threshold = threshold

    def prepareInput(self, inputArray):
        """can be overwritten to tranform tensors to numpy"""
        return inputArray

    def preparePrediction(self, inputArray):
        # for classification task the shape can be (recordcount?, predictions, classCount)
        isOneHotEncode = inputArray.shape[-1] == self.numClasses
        return inputArray.reshape(-1, self.numClasses) if isOneHotEncode else inputArray.reshape(-1, 1)

    def prepareTruth(self, inputArray):
        """flatten and squeeze the truth array"""
        isOneHotEncode = inputArray.shape[-1] == self.numClasses

        if isOneHotEncode:
            maskedIgnored = inputArray.sum(axis=-1) == 0
            inputArray = np.argmax(inputArray, axis=-1)
            inputArray[maskedIgnored] = -1

        return inputArray.reshape(-1)

    def score(self, truth, prediction, recordName=None, trace=True):
        prediction = self.prepareInput(prediction)
        truth = self.prepareInput(truth)
        prediction = self.preparePrediction(prediction)
        truth = self.prepareTruth(truth)

        truthOrg, predictionOrg = truth, prediction
        truth, prediction = self.maskedIgnoredValues(truth, prediction)

        metrics = self.scoreMetrics(truth, prediction)
        if self.trace and trace:
            if recordName is None:
                recordName = self.recordIndex

            self.recordResult[recordName] = self.recordEntry(truthOrg, predictionOrg, self.results, recordName)

            self.recordIndex += 1

        return metrics

    def recordEntry(self, truth, prediction, metrics, recordName=None):

        # prediction = self.flattenPrediction(prediction)

        # if "confusion" in metrics and self.addEvents:
        #     events = self.getValidationEvents(truth, prediction, recordName=recordName)
        # else:
        #     events = None

        entry = {
            "truth": truth,
            "prediction": prediction,
            # "events": events,
        }
        entry.update(metrics)
        return entry

    def getRecords(self):

        return self.recordResult.values()

    def getRecordsAsDataframe(self):
        import pandas as pd

        return pd.DataFrame(
            self.getRecords(),
            index=list(self.recordResult.keys()),
        )

    def combineMetric(self, metricName):

        metricName = self.getMetricName(metricName)

        result = None

        if metricName in self.addedMetrics:
            truth = np.concatenate([self.recordResult[id]["truth"] for id in self.recordResult], axis=0)
            prediction = np.concatenate([self.recordResult[id]["prediction"] for id in self.recordResult], axis=0)
            self.results[metricName] = self.addedMetrics[metricName]["combine"](truth, prediction)
        if metricName in ["kappa", "accuracy"]:  # recalcuate from confusion
            self.combineMetric("confusion")
            self.scoreMetric("kappa", None, None)
        if metricName == "f1":  # recalcuate from confusion
            self.combineMetric("confusion")
            self.scoreMetric("f1", None, None)
        elif metricName == "confusion":  # combine all confusion
            result = np.array(
                [self.recordResult[id]["confusion"] for id in self.recordResult if len(self.recordResult[id]["confusion"]) > 0]
            ).sum(axis=0)
        elif metricName in ["auprc", "auroc"]:

            if self.numClasses != 2:
                raise Exception("Metric auprc, auroc only support binary classification at the moment")

            self.results["all_values"] = np.array([self.recordResult[id]["all_values"] for id in self.recordResult]).sum(axis=0)
            self.results["pos_values"] = np.array([self.recordResult[id]["pos_values"] for id in self.recordResult]).sum(axis=0)
            self.results["ign_values"] = np.array([self.recordResult[id]["ign_values"] for id in self.recordResult]).sum(axis=0)

            # Compute the histogram of probabilities
            # given the above
            self.results["neg_values"] = self.results["all_values"] - self.results["pos_values"] - self.results["ign_values"]
            auroc, auprc, _, _, _ = self._auc(self.results["pos_values"], self.results["neg_values"])
            self.results["auprc"] = np.sum(auprc)
            self.results["auroc"] = np.sum(auroc)
        elif metricName in [
            "meanSquared",
            "loss",
            "rootMeanSquared",
            "prd",
            "eventCountDiff",
            "countTruth",
            "countPred",
            "overlappingCount",
            "positiveErrorRatio",
            "fm",
            "CSI",
            "SNR",
        ]:  # mean over all records
            sum = np.sum([self.recordResult[id][metricName] for id in self.recordResult])
            self.results[metricName] = sum / len(self.recordResult)

        if result is not None:
            self.results[metricName] = result

        return self.results[metricName]

    def combineMetrics(self):
        self.results = {}
        returnMetrics = {}
        for metricName in self.metrics:
            returnMetrics[metricName] = self.combineMetric(metricName)

        return returnMetrics

    def scoreAllRecords(self):
        if self.trace is False:
            raise Exception("The scorer does not keep the scored record, set the scorer.trace to True to keep all the results")
        self.combineMetrics()
        return self.results

    def maskedIgnoredValues(self, truth, prediction):
        for ignore in self.ignoreClasses:
            keep = truth != ignore
            truth = truth[keep]
            prediction = prediction[keep]

        return truth, prediction

    def scoreMetrics(self, truth, prediction):
        self.results = {}
        returnMetrics = {}
        for metricName in self.metrics:
            returnMetrics[metricName] = self.scoreMetric(metricName, truth, prediction)

        return returnMetrics

    def isHotEncoded(self, y):
        return y.shape[-1] == self.numClasses

    def calculateKappaAccFromConfusion(self, confusion):
        # implementation from sklearn
        n_classes = confusion.shape[0]
        sum0 = np.sum(confusion, axis=0)
        sum1 = np.sum(confusion, axis=1)
        if np.sum(sum0) == 0:
            return 0, 0
        expected = np.outer(sum0, sum1) / np.sum(sum0)

        w_mat = np.ones([n_classes, n_classes], dtype=np.int32)
        w_mat.flat[:: n_classes + 1] = 0

        nonDiag = np.sum(w_mat * confusion)
        if nonDiag == 0:
            k = 1
            acc = 1
        else:
            k = 1 - (nonDiag / np.sum(w_mat * expected))
            acc = 1 - (nonDiag / np.sum(confusion))

        return k, acc

    def maskArgMax(self, a, threshold):
        masked = np.ma.MaskedArray(a, a < threshold)
        return np.ma.argmax(masked)

    def getClassLikelyhood(self, prediction):
        max = np.max(prediction, axis=1, keepdims=True)
        if self.isHotEncoded(prediction):
            e_x = np.exp(prediction - max)
            sum = np.sum(e_x, axis=1, keepdims=True)  # returns sum of each row and keeps same dims
            predictionSoftMax = e_x / sum
            classLikelyhood = predictionSoftMax[:, 1]
        else:
            classLikelyhood = max.reshape(-1)
        return classLikelyhood

    def getClassPrediction(self, prediction):
        likelyhood = self.getClassLikelyhood(prediction)
        prediction = np.full(prediction.shape[0], 0)
        prediction[likelyhood > self.threshold] = 1
        return prediction

    def flattenPrediction(self, prediction, binaryLikelyHood=False, threshold=None):
        if binaryLikelyHood and self.numClasses != 2:
            raise Exception("Selected metric only support binary classification at the moment")

        if threshold is not None:
            return self.getClassPrediction(prediction)

        if self.isHotEncoded(prediction):
            prediction = prediction.argmax(-1)
        else:
            threshhold = 0.5 if self.threshold is None else self.threshold
            prediction[prediction >= threshhold] = 1
            prediction[prediction < threshhold] = 0
        return prediction

    def getMetricScorer(self, metricName):
        def score(truth, prediction):
            prediction = self.prepareInput(prediction)
            truth = self.prepareInput(truth)
            prediction = self.preparePrediction(prediction)
            truth = self.prepareTruth(truth)
            self.results = {}
            return self.scoreMetric(metricName, truth, prediction)

        score.__name__ = metricName
        return score

    def scoreMetric(self, metricName, truth, prediction):

        metricName = self.getMetricName(metricName)

        if metricName in self.results:
            return self.results[metricName]

        result = None

        if metricName in self.addedMetrics:
            self.results[metricName] = self.addedMetrics[metricName]["score"](truth, prediction)
        elif metricName in ["kappa", "accuracy"]:
            confusion = self.scoreMetric("confusion", truth, prediction)
            k, acc = self.calculateKappaAccFromConfusion(confusion)
            self.results["accuracy"] = acc
            self.results["kappa"] = k
        elif metricName in ["f1"]:
            (tn, fn), (fp, tp) = self.scoreMetric("confusion", truth, prediction)
            f1 = tp / (tp + 0.5 * (fp + fn))
            self.results["f1"] = f1
        elif metricName == "confusion":
            prediction = self.flattenPrediction(prediction, threshold=self.threshold)
            result = confusion_matrix(
                truth, prediction, labels=range(self.numClasses)
            )  # , labels=range(self.numClasses) # HPC comp
        elif metricName in ["auprc", "auroc"]:
            classLikelyhood = self.getClassLikelyhood(prediction)

            scale = 10 ** 3
            b = scale + 1
            r = (-0.5 / scale, 1.0 + 0.5 / scale)

            self.results["all_values"] = np.histogram(classLikelyhood, bins=b, range=r)[0]

            pred_pos = classLikelyhood[truth > 0]
            self.results["pos_values"] = np.histogram(pred_pos, bins=b, range=r)[0]

            # Compute the histogram of probabilities within unscored regions
            pred_ign = classLikelyhood[truth < 0]
            self.results["ign_values"] = ign_values = np.histogram(pred_ign, bins=b, range=r)[0]

            # Compute the histogram of probabilities in non-arousal regions,
            # given the above
            self.results["neg_values"] = self.results["all_values"] - self.results["pos_values"] - self.results["ign_values"]
            auroc, auprc, _, _, _ = self._auc(self.results["pos_values"], self.results["neg_values"])
            self.results["auprc"] = np.sum(auprc)
            self.results["auroc"] = np.sum(auroc)
        elif metricName in ["loss"]:
            truth, prediction = self.beforeLoss(truth, self.flattenPrediction(prediction))
            self.results["loss"] = self.lossF(truth, prediction)
        elif metricName in ["meanSquared", "rootMeanSquared", "prd"]:
            if len(prediction.shape) > 1:
                diag = np.eye(self.numClasses)
                truth = diag[truth]
            squared = np.square(truth - prediction)
            meanSquared = squared.mean() if len(truth) > 0 else 0
            if metricName == "meanSquared":  # MS
                self.results[metricName] = meanSquared
            elif metricName == "rootMeanSquared":  # RMS
                self.results[metricName] = np.sqrt(meanSquared)
            elif metricName == "prd":  # Percentage RMS Difference
                self.results[metricName] = 100 * np.sqrt(squared.sum() / (np.square(truth).sum()))
        elif metricName in ["countTruth"]:
            truthCount = np.sum(np.diff(truth) > 0)
            self.results[metricName] = truthCount
        elif metricName in ["countPred"]:
            classPrediction = self.flattenPrediction(prediction, threshold=self.threshold)
            predCount = np.sum(np.diff(classPrediction) > 0)
            self.results[metricName] = predCount
        elif metricName in ["eventCountDiff"]:
            classPrediction = self.flattenPrediction(prediction, threshold=self.threshold)
            predCount = np.sum(np.diff(classPrediction) > 0)
            truthCount = np.sum(np.diff(truth) > 0)
            self.results[metricName] = int(np.abs(predCount - truthCount))
        elif metricName in ["overlappingCount"]:
            classPrediction = self.flattenPrediction(prediction, threshold=self.threshold)
            overlap = classPrediction + truth
            count = np.diff(overlap == 2).sum() / 2  # only count every up change
            self.results[metricName] = count
        elif metricName in ["positiveErrorRatio"]:
            confusion = self.scoreMetric("confusion", truth, prediction)
            tp = confusion[-1][-1]
            tn = confusion[0][0]
            f = np.sum(confusion) - tp - tn
            self.results[metricName] = f / tp if tp > 0 else 0
        elif metricName in ["CSI"]:
            confusion = self.scoreMetric("confusion", truth, prediction)
            tp = confusion[-1][-1]
            tn = confusion[0][0]
            f = np.sum(confusion) - tp - tn
            self.results[metricName] = tp / (tp + f)
        elif metricName == "SNR":  # signal to noise ratio
            axis = 0
            ddof = 0
            a = np.asanyarray(prediction)
            m = a.mean(axis)
            sd = a.std(axis=axis, ddof=ddof)
            self.results[metricName] = np.where(sd == 0, 0, m / sd)
        elif metricName == "fm":  # Fowlkes–Mallows index
            confusion = self.scoreMetric("confusion", truth, prediction)
            (tn, fn), (fp, tp) = confusion

            tp = confusion[-1][-1]
            tn = confusion[0][0]
            ppv = tp / (tp + fp)
            tpr = tp / (tp + fn)

            self.results[metricName] = np.sqrt(ppv * tpr)
        if result is not None:
            self.results[metricName] = result

        return self.results[metricName]

    def getValuesFromClasses(self):
        if self.possibleValues is None:
            values = []
            for id in range(self.numClasses ** 2):
                trueValue, preditedValue = (id // self.numClasses, id % self.numClasses)
                values.append("%s as %s" % (self.classNames[trueValue], self.classNames[preditedValue]))
            self.possibleValues = values

        return self.possibleValues

    # def getValidationEvents(self, truth, prediction, recordName=None):

    #     validationSignal = self.numClasses * truth + prediction
    #     validationSignal[truth == -1] = -1

    #     values = self.getValuesFromClasses()

    #     em = EventManager(None)
    #     return em.getEventsFromSignal(validationSignal, values, owner=recordName)

    # def confusionMatrix(self, resultEntry, labels=None, title="confusion matrix"):
    #     confusion = resultEntry["confusion"]
    #     labels = self.classNames

    #     label_list = [labels[i] for i in range(len(labels))]
    #     df_cm = pd.DataFrame(confusion, index=label_list, columns=label_list)

    #     blue = cm.get_cmap("Blues", 256)
    #     darkencolor = blue(np.linspace(0.3, 1, 256))
    #     newcmp = ListedColormap(darkencolor, name="DarkenBlue")
    #     figSize = self.numClasses * Scorer.cmScaleByClass
    #     return pp_matrix(df_cm, title=title, figsize=[figSize, figSize], cmap=newcmp, cbar=False)

    # def confusionMatrixTrailor(self, resultEntry, labels=None, title="sub confusion matrix", rowsSplit=slice(0,2), colSplit=slice(None), colNames = None, rowNames=None):
    #     #remove NoneRow
    #     colNames = self.classNames if colNames is None else colNames
    #     rowNames = self.classNames if rowNames is None else rowNames
    #     confusion = resultEntry["confusion"][colSplit, rowsSplit]
    #     labelsCol = np.array(colNames)[colSplit]
    #     labelsRow = np.array(rowNames)[rowsSplit]
    #     df_cm = pd.DataFrame(confusion, index=labelsCol, columns=labelsRow)

    #     blue = cm.get_cmap("Blues", 256)
    #     darkencolor = blue(np.linspace(0.3, 1, 256))
    #     newcmp = ListedColormap(darkencolor, name="DarkenBlue")
    #     figSizeL = (len(labelsCol) + 1 ) * Scorer.cmScaleByClass
    #     figSizeH = (len(labelsRow) +  1) * Scorer.cmScaleByClass
    #     return pp_matrix(df_cm, title=title, figsize=[figSizeL, figSizeH], cmap=newcmp, cbar=False)

    # def prCurve(self, resultEntry, title="ROC"):
    #     _, _, precision, _, recall = self._auc(resultEntry["pos_values"], resultEntry["neg_values"])
    #     fig = plt.figure(figsize=(6, 6))
    #     lw = 2
    #     plt.plot(
    #         recall,
    #         precision,
    #         color="darkorange",
    #         lw=lw,
    #         label=title,
    #     )
    #     plt.xlim([0.0, 1.0])
    #     plt.ylim([0.0, 1.05])
    #     plt.xlabel("Recall")
    #     plt.ylabel("Precision")
    #     plt.title("Precision/Recall Curve")
    #     plt.legend(loc="lower right")

    #     return fig

    # def rocCurve(self, resultEntry, title="ROC"):
    #     _, _, tpr, fpr, _ = self._auc(resultEntry["pos_values"], resultEntry["neg_values"])

    #     fig = plt.figure(figsize=(6, 6))
    #     lw = 2
    #     plt.plot(
    #         fpr,
    #         tpr,
    #         color="darkorange",
    #         lw=lw,
    #         label=title,
    #     )
    #     plt.plot([0, 1], [0, 1], color="navy", lw=lw, linestyle="--")
    #     plt.xlim([0.0, 1.0])
    #     plt.ylim([0.0, 1.05])
    #     plt.xlabel("False Positive Rate")
    #     plt.ylabel("True Positive Rate")
    #     plt.title("Receiver operating characteristic")
    #     plt.legend(loc="lower right")
    #     return fig

    def _auc(self, pos_values, neg_values):
        # Calculate areas under the ROC and PR curves by iterating
        # over the possible threshold values.

        # At the minimum threshold value, all samples are classified as
        # positive, and thus TPR = 1 and TNR = 0.
        tp = np.sum(pos_values)
        fp = np.sum(neg_values)
        tn = fn = 0
        tpr = 1
        tnr = 0
        if tp == 0 or fp == 0:
            # If either class is empty, scores are undefined.
            return (
                float("nan"),
                float("nan"),
                float("nan"),
                float("nan"),
                float("nan"),
            )
        ppv = float(tp) / (tp + fp)
        auroc = []
        auprc = []
        tpr_arr = []
        fpr_arr = []
        precisions = []

        # As the threshold increases, TP decreases (and FN increases)
        # by pos_values[i], while TN increases (and FP decreases) by
        # neg_values[i].
        for (n_pos, n_neg) in zip(pos_values, neg_values):
            tp -= n_pos
            fn += n_pos
            fp -= n_neg
            tn += n_neg
            tpr_prev = tpr
            tnr_prev = tnr
            ppv_prev = ppv
            tpr = float(tp) / (tp + fn)  # recall
            tnr = float(tn) / (tn + fp)
            fpr = float(fp) / (fp + tn)

            if tp + fp > 0:
                ppv = float(tp) / (tp + fp)  # precision
            else:
                ppv = ppv_prev

            auroc.append((tpr_prev - tpr) * (tnr + tnr_prev) * 0.5)
            auprc.append((tpr_prev - tpr) * ppv_prev)

            tpr_arr.append(tpr)
            fpr_arr.append(fpr)
            precisions.append(ppv)
        return (auroc, auprc, tpr_arr, fpr_arr, precisions)
