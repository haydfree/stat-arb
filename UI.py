import datetime
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ObjectFactory import ObjectFactory
import pandas as pd


class UI:
    __objectFactory: ObjectFactory

    def __init__(self,
                 objectFactory: ObjectFactory):
        self.__objectFactory = objectFactory
        self.table_added = False
        self.accuracyTableAdded = False

        self.layout = None
        self.updateLayout()

        self.window = None
        self.windowWidth = 1800
        self.windowHeight = 1000

        self.closedTradesInfo = None
        self.sortColumn = None
        self.sortAsc = True

        self.createLoginWindow()
        # self.createWindow()

    def getObjectFactory(self) -> ObjectFactory:
        return self.__objectFactory

    def setObjectFactory(self,
                         objectFactory: ObjectFactory) -> None:
        self.__objectFactory = objectFactory

    def getLayout(self) -> list:
        return self.layout

    def setLayout(self,
                  layout: list) -> None:
        self.layout = layout

    def updateLayout(self) -> list:
        labels = ['Data source', 'Instrument 1', 'Instrument 2', 'Start Date in format YYYY-MM-DD',
                  'End Date in format YYYY-MM-DD', 'Timeframe', 'Entry threshold', 'Window size']
        keys = ['-DATASOURCE-', '-INSTRUMENT1-', '-INSTRUMENT2-', '-START_DATE-', '-END_DATE-',
                '-TIMEFRAME-', '-ENTRY_THRESHOLD-', '-WINDOW-']
        default_values = ['yahoo', 'AAPL', 'MSFT', '1990-01-01', '2024-01-01', '1d', '2', '50']

        input_layout = []
        size = (30, 1)
        for label, key, default_value in zip(labels, keys, default_values):
            if "INSTRUMENT" in key:
                input_layout.append([sg.Text(label, size=size),
                                     sg.DropDown(values=["AAPL", "MSFT", "GOOG",
                                                         "META", "SPY", "QQQ"],
                                                 default_value=default_value,
                                                 size=size,
                                                 key=key)])
            elif key == "-DATASOURCE-":
                input_layout.append([sg.Text(label, size=size),
                                     sg.DropDown(values=["yahoo"],
                                                 default_value=default_value,
                                                 size=size,
                                                 key=key)])
            elif key == "-TIMEFRAME-":
                input_layout.append([sg.Text(label, size=size),
                                     sg.DropDown(values=["1m", "5m", "15m",
                                                         "1h", "1d"],
                                                 default_value=default_value,
                                                 size=size,
                                                 key=key)])
            else:
                input_layout.append([sg.Text(label, size=size),
                                     sg.InputText(default_text=default_value,
                                                  size=size,
                                                  key=key)])

        button_layout = [[sg.Button('Run'), sg.Button('Test Model Accuracy'), sg.Button('Restart')]]

        canvas = sg.Canvas(size=(800, 400), key='-CANVAS1-')
        trades_text = sg.Text('', size=(500, 24), key='-TRADES-')
        train_test_split_text = sg.Text('', size=(500, 22), key='-TRAIN_TEST_SPLIT-')
        layout = [
            [sg.Column(input_layout, size=(600, 220), justification='center')],
            [sg.Column([[train_test_split_text]], size=(300, 22), justification='center')],
            [sg.Column(button_layout, size=(350, 50), justification='center')],
            [sg.Column([[trades_text]], size=(700, 24), justification='center')],
            [sg.Column([[canvas]], size=(1700, 410), justification='center')]
        ]

        self.setLayout(layout)
        return self.getLayout()

    def createLoginWindow(self):
        loginLayout = [
            [sg.Text('Login')],
            [sg.Text('Username'), sg.InputText(key='-USERNAME-')],
            [sg.Text('Password'), sg.InputText(key='-PASSWORD-', password_char='*')],
            [sg.Button('Login')]
        ]

        self.window = sg.Window(title='Login', layout=loginLayout)

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == 'Login':
                username = values['-USERNAME-']
                password = values['-PASSWORD-']
                if self.authenticate(username, password):
                    self.window.close()
                    self.createWindow()
                    break
                else:
                    sg.popup('Invalid username or password')

    @staticmethod
    def authenticate(username, password):
        return username == 'admin' and password == 'password'

    def createWindow(self) -> None:
        self.window = sg.Window(title='Statistical Arbitrage Tool',
                                layout=self.layout,
                                size=(self.windowWidth,
                                      self.windowHeight))

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event == "Run":
                try:
                    self.getObjectFactory().run(values=values)
                except Exception as e:
                    pass
                    sg.popup(e)
                    self.restart()
                self.updateFrame(values)
            elif event == "Restart":
                self.restart()
            elif event == "Test Model Accuracy":
                self.testModelAccuracy()
                self.createAccuracyTable()
            elif isinstance(event, tuple) and event[0] == "-TABLE-" and event[2][0] == -1 and event[2][1] != -1:
                col = self.closedTradesInfo.columns[event[2][1]]
                self.sortTable(col)
                self.createTable()
                self.window["-TABLE-"].update(self.closedTradesInfo.values.tolist())

    def sortTable(self,
                  column) -> None:
        if self.sortColumn == column:
            self.sortAsc = not self.sortAsc
        else:
            self.sortColumn = column
            self.sortAsc = True

    def createTable(self):
        objectFactory: ObjectFactory = self.getObjectFactory()
        closedTradesInfo: pd.DataFrame = objectFactory.getStrategy().getClosedTradesInfo()

        if self.sortColumn is not None:
            closedTradesInfo = closedTradesInfo.sort_values(by=self.sortColumn, ascending=self.sortAsc)
        self.closedTradesInfo = closedTradesInfo

        tableHeaders = closedTradesInfo.columns.tolist()
        tableValues = closedTradesInfo.values.tolist()
        table = sg.Table(values=tableValues,
                         headings=tableHeaders,
                         key='-TABLE-',
                         enable_click_events=True)
        if not self.table_added:
            self.window.extend_layout(self.window,
                                      rows=[[table]])
            self.table_added = True

    def createAccuracyTable(self) -> None:
        accuracyTableDf: pd.DataFrame = self.testModelAccuracy()
        accuracyTableHeaders = accuracyTableDf.columns.tolist()
        accuracyTableValues = accuracyTableDf.values.tolist()
        accuracyTable = sg.Table(values=accuracyTableValues,
                                 headings=accuracyTableHeaders,
                                 key="-ACCURACY_TABLE-",
                                 size=(len(accuracyTableValues), len(accuracyTableHeaders)),
                                 num_rows=1,
                                 row_height=20)
        if not self.accuracyTableAdded:
            self.window.extend_layout(self.window,
                                      rows=[[accuracyTable]])
            self.accuracyTableAdded = True

    def updateFrame(self,
                    values):
        objectFactory: ObjectFactory = self.getObjectFactory()
        plot1Data: pd.Series = objectFactory.getPlot1Data()
        plot2Data: pd.Series = objectFactory.getPlot2Data()

        startDate: str = values["-START_DATE-"]
        endDate: str = values["-END_DATE-"]
        startDateDt: datetime = datetime.datetime.strptime(startDate, "%Y-%m-%d")
        endDateDt: datetime = datetime.datetime.strptime(endDate, "%Y-%m-%d")
        spread: pd.Series = objectFactory.getStrategy().getStandardizedSpread()

        entriesToday, exitsToday = objectFactory.getStrategy().getTradesToday(date=endDate,
                                                                              spread=spread)
        self.window["-TRADES-"].update(f"{entriesToday} {exitsToday}")

        trainTestSplitStart = startDateDt + ((endDateDt - startDateDt) * 0.7)
        self.window["-TRAIN_TEST_SPLIT-"].update(f"Test split starts: {trainTestSplitStart}")

        self.createTable()

        firstValidIdx = objectFactory.getStrategy().getExitThreshold().first_valid_index()
        fig, (ax1, ax2, ax3) = plt.subplots(nrows=1,
                                            ncols=3,
                                            figsize=(17, 4))
        ax1.plot(plot1Data[firstValidIdx:], label="spread")
        ax1.plot(objectFactory.getStrategy().getExitThreshold()[firstValidIdx:], label="model predicted exit threshold",
                 color="black")
        ax1.axhline(objectFactory.getStrategy().getEntryThreshold(), label="short entry threshold", color="red")
        ax1.axhline(-objectFactory.getStrategy().getEntryThreshold(), label="long entry threshold", color="green")
        ax1.set_title(f"{objectFactory.getPair().getPairName()} standardized spread")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Spread")

        ax2.plot(plot2Data)
        ax2.set_title("Profit / Loss")
        ax2.set_xlabel("Trades")
        ax2.set_ylabel("PnL")

        predictedData, residuals = (objectFactory.getPredictedData(),
                                    objectFactory.getResiduals())
        ax3.scatter(predictedData, residuals)
        ax3.set_xlabel('Predicted Values')
        ax3.set_ylabel('Residuals')
        ax3.set_title('Residual Plot')

        canvas = FigureCanvasTkAgg(fig, self.window["-CANVAS1-"].TKCanvas)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=1)

    def restartObjectFactory(self) -> ObjectFactory:
        objectFactory: ObjectFactory = ObjectFactory(name="of1")
        self.setObjectFactory(objectFactory)
        return self.getObjectFactory()

    def restart(self) -> None:
        self.updateLayout()
        self.restartObjectFactory()

        self.table_added = False
        self.accuracyTableAdded = False
        self.window.close()
        self.createWindow()
        self.createTable()

    def testModelAccuracy(self) -> pd.DataFrame:
        return self.getObjectFactory().getModelTestResults()
