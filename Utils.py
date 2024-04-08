from Model import Model
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


class Utils:

    @staticmethod
    def testModelAccuracy(model: Model) -> (pd.DataFrame, pd.Series):
        fmv: pd.Series = model.getFairMarketValue()
        firstValidIdx = fmv.first_valid_index()
        predictedData: pd.Series = fmv[firstValidIdx:]
        actualData: pd.Series = model.getPair().getStandardizedSpread()
        actualData = actualData[len(actualData) - len(predictedData):]

        mse = mean_squared_error(actualData, predictedData)
        mae = mean_absolute_error(actualData, predictedData)
        r2 = r2_score(actualData, predictedData)
        rmse = np.sqrt(mse)

        residuals = actualData - predictedData
        plt.scatter(predictedData, residuals)
        plt.xlabel('Predicted Values')
        plt.ylabel('Residuals')
        plt.title('Residual Plot')
        # plt.show()

        actualDataRollingIdx = actualData.rolling(window=50).mean().first_valid_index()
        baselineMse = mean_squared_error(actualData[actualDataRollingIdx:],
                                         actualData.rolling(window=50).mean()[actualDataRollingIdx:])
        improvement = (baselineMse - mse) / baselineMse * 100

        accuracyMetrics: pd.DataFrame = pd.DataFrame({
            'Mean Squared Error (MSE)': [mse],
            'Root Mean Squared Error (RMSE)': [rmse],
            'Mean Absolute Error (MAE)': [mae],
            'R-squared (R2)': [r2],
            'Baseline MSE': [baselineMse],
            'Improvement over Baseline (%)': [improvement]
        })
        return accuracyMetrics, predictedData, residuals
