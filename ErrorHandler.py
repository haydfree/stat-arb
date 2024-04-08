import datetime


class InvalidDataSourceError(Exception):
    pass


class InvalidInstrumentError(Exception):
    pass


class InvalidInstruments(Exception):
    pass


class DateRangeError(Exception):
    pass


class InvalidDateFormatError(Exception):
    pass


class InvalidInteger(Exception):
    pass


class InvalidTimeframeError(Exception):
    pass


class InvalidDateError(Exception):
    pass


class InvalidDataSetError(Exception):
    pass


class InvalidPairNameError(Exception):
    pass


class NaNValuesInDataFrameError(Exception):
    pass


class InvalidTradeError(Exception):
    pass


class InvalidNumberError(Exception):
    pass


class ErrorHandler:
    def __init__(self,
                 objectFactory):
        self.objectFactory = objectFactory

    @staticmethod
    def validateDataSource(dataSource) -> bool:
        if dataSource == "yahoo":
            return True
        raise InvalidDataSourceError("Invalid data source. Yahoo is the only data source currently available.")

    @staticmethod
    def validateInstrument(instrument) -> bool:
        if instrument in ["AAPL", "MSFT", "GOOG", "META", "SPY", "QQQ",
                          "TSLA", "NVDA", "AMZN", "NFLX", "AMD", "PEP",
                          "KO", "MA", "V"]:
            return True
        raise InvalidInstrumentError("Invalid instrument. Please select an instrument from the dropdown.")

    @staticmethod
    def validateInstruments(i1, i2) -> bool:
        if i1 != i2:
            return True
        raise InvalidInstruments("Instrument 1 cannot be equal to Instrument 2, please choose separate instruments.")

    @staticmethod
    def validateDateFormat(dateStr) -> bool:
        try:
            datetime.datetime.strptime(dateStr, "%Y-%m-%d")
            return True
        except ValueError:
            raise InvalidDateFormatError("Invalid date format. Please use YYYY-MM-DD.")

    @staticmethod
    def validateDate(date) -> bool:
        try:
            date + datetime.timedelta(days=1)
            return True
        except Exception:
            raise InvalidDateError("Invalid date. Years 1970-2024. Months 1-12. Days 1-31.")

    @staticmethod
    def validateDateRange(startDate,
                          endDate,
                          timeframe) -> bool:
        sd = startDate
        ed = endDate
        today = datetime.datetime.today()
        if timeframe == "1m":
            if sd <= today - datetime.timedelta(days=30):
                raise DateRangeError("1m timeframe needs to be 7 days max, within last 29 days, and > 1 day")
            if ed - sd >= datetime.timedelta(days=7) or ed - sd <= datetime.timedelta(days=1):
                raise DateRangeError("1m timeframe needs to be 7 days max, within last 29 days, and > 1 day")
        if timeframe == "5m" or timeframe == "15m":
            if sd <= today - datetime.timedelta(days=60):
                raise DateRangeError(f"{timeframe} timeframe needs to be 60 days max within last 60 days")
            if ed - sd >= datetime.timedelta(days=60):
                raise DateRangeError(f"{timeframe} timeframe needs to be 60 days max within last 60 days")
        if timeframe == "1h":
            if sd <= today - datetime.timedelta(days=730):
                raise DateRangeError("1h timeframe needs to be 730 days max within last 730 days")
            if ed - sd >= datetime.timedelta(days=730):
                raise DateRangeError("1h timeframe needs to be 730 days max within last 730 days")
        if startDate == endDate:
            raise DateRangeError("Start date and end date cannot be equal. Please choose separate dates.")
        return True

    @staticmethod
    def validateInteger(integer) -> bool:
        if isinstance(integer, int):
            return True
        raise InvalidInteger("Invalid selection for window or entry threshold, they should be integers")

    @staticmethod
    def validateTimeframe(timeframe) -> bool:
        if timeframe in ["1m", "5m", "15m", "1h", "1d"]:
            return True
        raise InvalidTimeframeError("Invalid timeframe. Please choose a timeframe from the dropdown")

    @staticmethod
    def validateEnoughData(data) -> bool:
        if data.size > 100:
            return True
        raise DateRangeError(f"Available data is too small {data.size}")

    @staticmethod
    def validateDataSet(dataSet) -> bool:
        if type(dataSet) is list and len(dataSet) != 0 and dataSet[0].getData().size > 100 and \
                dataSet[1].getData().size > 100:
            return True
        raise InvalidDataSetError("Data set is invalid. Either list is empty or one of the Data objects is too small.")

    @staticmethod
    def validatePairName(pairName) -> bool:
        flag = False
        try:
            s1, s2 = pairName.split("_")
            if s1 == s2:
                flag = False
            flag = True
        except Exception as e:
            raise InvalidPairNameError("Invalid pair name. Should be in format: pair1_pair2")

    @staticmethod
    def validateSpread(spread) -> bool:
        ErrorHandler.validateEnoughData(spread)
        if spread.isnull().values.any():
            raise NaNValuesInDataFrameError("Spread contains NaN values")


    @staticmethod
    def validateSeries(series) -> bool:
        ErrorHandler.validateEnoughData(series)
        if series.isnull().values.any():
            raise NaNValuesInDataFrameError(f"NaN values in series / dataframe {series}")

    @staticmethod
    def validateTrade(trade) -> bool:
        if all([trade.getSymbol(),
                trade.getPairName(),
                trade.getPairTradeDirection(),
                trade.getEntryPrice(),
                trade.getEntryTime(),
                trade.getDirection(),
                trade.getVolume()]):
            return True
        if isinstance(trade.getSymbol(), str) and \
           isinstance(trade.getPairName(), str) and \
           isinstance(trade.getPairTradeDirection(), int) and \
           isinstance(trade.getEntryPrice(), float) and \
           isinstance(trade.getEntryTime(), datetime.datetime) and \
           isinstance(trade.getDirection(), int) and \
           isinstance(trade.getVolume(), float):
            return True
        raise InvalidTradeError(f"Invalid trade: {trade, trade.getSymbol(), trade.getEntryTime()}")

    @staticmethod
    def validateTrades(trades) -> bool:
        for trade in trades:
            ErrorHandler.validateTrade(trade)

    @staticmethod
    def validatePositive(number) -> bool:
        if number > 0:
            return True
        raise InvalidNumberError(f"Number should be positive, is not {number}")

    @staticmethod
    def validateNumber(number) -> bool:
        if isinstance(number, int) or isinstance(number, float):
            return True
        raise InvalidNumberError(f"Value should be a number, is not {number}")

    @staticmethod
    def validateTradeDirection(tradeDirection) -> bool:
        if tradeDirection == 1 or tradeDirection == -1:
            return True
        raise InvalidNumberError(f"Trade direction should be 1 or -1 {tradeDirection}")
