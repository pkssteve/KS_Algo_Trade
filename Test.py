from pandas import Series, DataFrame
import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
from zipline.api import order, symbol
from zipline.algorithm import TradingAlgorithm


def initialize(context):
    pass


def handle_data(context, data):
    order(symbol('AAPL'), 1)


# getting stock data from web
start = datetime.datetime(2020, 4, 1)
end = datetime.datetime(2020, 4, 30)
gs = web.DataReader("AAPL", "yahoo")
gs.info()

print(gs.tail())
# new_gs = gs[gs['Volume'] != 0]
new_gs = gs[['Adj Close']]
print(new_gs.head())
new_gs.columns = ['AAPL']
print(new_gs.head())
new_gs = new_gs.tz_localize('UTC')
print(new_gs.head())

algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data)
result = algo.run(new_gs)
print(result.head())


# Calculate moving average
ma5 = new_gs['Adj Close'].rolling(window=5).mean()

# insert columns
new_gs.insert(len(new_gs.columns), "MA5", ma5)

print(new_gs.tail(20))

# plot
plt.plot(new_gs.index, new_gs['Adj Close'], label='Adj Close')
plt.plot(new_gs.index, new_gs['MA5'], label="MA5")
plt.legend(loc='best')
plt.grid()
plt.show()
