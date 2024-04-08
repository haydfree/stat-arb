from sklearn import linear_model
from Pair import Pair
from ErrorHandler import ErrorHandler
import pandas as pd
import numpy as np


class Model:
    __fairMarketValue: pd.Series
    __model: linear_model.LinearRegression
    __pair: Pair

    def __init__(self,
                 pair: Pair):
        self.__model = linear_model.LinearRegression()
        self.__pair = pair

    def predict(self,
                trainSet: pd.Series) -> None:
        df: pd.DataFrame = pd.DataFrame(trainSet)
        pair: Pair = self.getPair()
        model: linear_model.LinearRegression = self.getModel()

        df.index = pd.to_datetime(df.index).astype('int64') // 10 ** 9
        trainSetX: pd.DataFrame = df.index.values.reshape(-1, 1)
        trainSetY: pd.DataFrame = df[f"{pair.getPairName()}"].bfill().values.reshape(-1, 1)

        trainTestSplit = int(0.3 * len(trainSetX))
        x_train, x_test, y_train, y_test = trainSetX[:-trainTestSplit], trainSetX[-trainTestSplit:], \
            trainSetY[:-trainTestSplit], trainSetY[-trainTestSplit:]
        model.fit(x_train, y_train)
        predictions = model.predict(x_test)

        predictions = pd.DataFrame(predictions)

        predictions = pd.concat([pd.DataFrame({f"{pair.getPairName()}":
                                [np.nan] * (len(trainSet) - len(predictions))}), predictions])
        predictions.index = trainSet.index
        predictions = pd.Series(predictions[0], index=predictions.index, name=f"{pair.getPairName()}")

        self.setModel(model)
        self.setFairMarketValue(predictions.dropna())

    def getFairMarketValue(self) -> pd.Series:
        return self.__fairMarketValue

    def setFairMarketValue(self,
                           fairMarketValue: pd.Series) -> None:
        ErrorHandler.validateSeries(fairMarketValue)
        self.__fairMarketValue = fairMarketValue

    def getModel(self) -> linear_model.LinearRegression:
        return self.__model

    def setModel(self,
                 model: linear_model.LinearRegression) -> None:
        self.__model = model

    def getPair(self) -> Pair:
        return self.__pair

    def setPair(self,
                pair: Pair) -> None:
        ErrorHandler.validatePairName(pair.getPairName())
        self.__pair = pair
