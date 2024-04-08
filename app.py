import base64
import io

import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, render_template, request

from ObjectFactory import ObjectFactory

app = Flask(__name__)


def savePlotToBase64(data: pd.Series,
                     plot: int,
                     **kwargs) -> str:
    figSize = (30, 15)
    if plot == 1:
        firstValidIdx = kwargs['firstValidIdx']
        title = f"{kwargs['pairName']} standardized spread"
        xLabel = "Date"
        yLabel = "Spread"
        data = data[firstValidIdx:]
        plt.figure(figsize=figSize)
        plt.plot(data, label="spread")
        plt.plot(kwargs['exitThreshold'].index, kwargs['exitThreshold'].values,
                 color="black",
                 label="model predicted exit")
        plt.axhline(kwargs['entryThreshold'], color="red", label="short entry threshold")
        plt.axhline(-kwargs['entryThreshold'], color="green", label="long entry threshold")
        plt.legend()
    elif plot == 2:
        title = "Profit / Loss"
        xLabel = "Trades"
        yLabel = "PnL"
        plt.figure(figsize=figSize)
        plt.plot(data.index, data.values)
    elif plot == 3:
        title = "Residuals"
        xLabel = "Date"
        yLabel = "Distance from model prediction"
        plt.figure(figsize=figSize)
        plt.scatter(data.index, data.values)
    else:
        title = "None"
        xLabel = "None"
        yLabel = "None"

    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()

    return image_base64


@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        try:
            dataSource = request.form.get('dataSource')
            instrument1 = request.form.get('instrument1')
            instrument2 = request.form.get('instrument2')
            startDate = request.form.get('startDate')
            endDate = request.form.get('endDate')
            timeframe = request.form.get('timeframe')
            entryThreshold = request.form.get('entryThreshold')
            window = request.form.get('window')

            values = {"dataSource": dataSource,
                      "instrument1": instrument1,
                      "instrument2": instrument2,
                      "startDate": startDate,
                      "endDate": endDate,
                      "timeframe": timeframe,
                      "entryThreshold": entryThreshold,
                      "window": window
                      }

            objectFactory = ObjectFactory(name="web")
            objectFactory.run(values=values)

            modelAccuracy = objectFactory.getModelTestResults().to_html(header=True,
                                                                        index=False)

            spread = objectFactory.getStrategy().getStandardizedSpread()
            tradesToday = objectFactory.getStrategy().getTradesToday(date=endDate,
                                                                     spread=spread)

            plot1Data = objectFactory.getPlot1Data()
            plot2Data = objectFactory.getPlot2Data()
            residualsData = objectFactory.getResiduals()

            firstValidIdx = objectFactory.getStrategy().getExitThreshold().first_valid_index()
            plot1Img = savePlotToBase64(plot1Data,
                                        plot=1,
                                        pairName=f"{instrument1}_{instrument2}",
                                        entryThreshold=objectFactory.getEntryThreshold(),
                                        exitThreshold=objectFactory.getStrategy().getExitThreshold()
                                        [firstValidIdx:],
                                        firstValidIdx=firstValidIdx)
            plot2Img = savePlotToBase64(plot2Data, 2)
            plot3Img = savePlotToBase64(residualsData, 3)
            closedTradesInfo = objectFactory.getStrategy().getClosedTradesInfo().to_html(header=True,
                                                                                         classes="table-container")

            return render_template('index.html',
                                   tradesToday=tradesToday,
                                   plot1Img=plot1Img,
                                   plot2Img=plot2Img,
                                   plot3Img=plot3Img,
                                   closedTradesInfo=closedTradesInfo,
                                   modelAccuracy=modelAccuracy,
                                   error=error)
        except Exception as e:
            error = str(e)
            return render_template('index.html', error=error)
    return render_template('index.html',
                           closedTradesInfo=None, error=error)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
