import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
from zipline.api import order, symbol, record
from zipline.algorithm import TradingAlgorithm

# data
start = datetime.datetime(2013, 3, 19)
end = datetime.datetime(2014, 3, 19)
data = web.DataReader("AAPL", "yahoo", start, end)

data = data[["Adj Close"]]
data.columns = ["AAPL"]
data = data.tz_localize("UTC")
print(data.head())


def initialize(context):
    pass


def handle_data(context, data):
    order(symbol("AAPL"), 1)


algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data)
result = algo.run(data)
print(result[['starting_cash', 'ending_cash', 'ending_value']].head())

plt.plot(result.index, result.portfolio_value)
plt.show()
