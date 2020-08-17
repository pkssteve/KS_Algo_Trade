import pandas_datareader as web
import datetime
import pandas
import matplotlib.pyplot as plt
from zipline.api import order, record, symbol
from zipline.algorithm import TradingAlgorithm
from zipline.api import set_commission

# getting raw data
start = datetime.datetime(2014, 1, 1)
end = datetime.datetime(2016, 3, 29)
data = web.DataReader('AAPL', 'yahoo', start, end)

# modify raw data for use
data = data[['Adj Close']]
data.columns = ['AAPL']
data = data.tz_localize('UTC')

data.head()
fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

# plt.plot(data.index, data['AAPL'])
# plt.show()

def getRSI(data):
    iter = 0
    AU=0
    AD=0
    for curPrice in data.values:
        if iter > 0:
            if data.values[iter - 1] < curPrice:
                AU = AU + (curPrice - data.values[iter - 1])
            elif data.values[iter - 1] > curPrice:
                AD = AD + (data.values[iter - 1] - curPrice)

        iter = iter + 1
    return AU / (AD + AU)


def initialize(context):
    context.i = 0
    context.sym = symbol('AAPL')
    context.hold = False
    # set_commission(commission.PerDollar(cost=0.00165))


def handle_data(context, data):
    context.i += 1
    if context.i < 20:
        return

    buy = False
    sell = False

    ma5 = data.history(context.sym, 'price', 5, '1d').mean()
    ma20 = data.history(context.sym, 'price', 20, '1d').mean()
    templist = data.history(context.sym, 'price', 15, '1d')

    pre_rsi = getRSI(templist[0:-1])
    rsi = getRSI(templist[1:])

    if ma5 > ma20 and context.hold is False:
        order(context.sym, 100)
        context.hold = True
        buy = True
    elif ma5 < ma20 and context.hold is True:
        order(context.sym, -100)
        context.hold = False
        sell = True

    record(AAPL=data.current(context.sym, 'price'), ma5=ma5, ma20=ma20, buy=buy, sell=sell, rsi=rsi)


algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data)
result = algo.run(data)



ax1.plot(result.index, result.ma5)
ax1.plot(result.index, result.ma20)
ax1.legend(loc='best')

ax1.plot(result.ix[result.buy == True].index, result.ma5[result.buy == True], '^')
ax1.plot(result.ix[result.sell == True].index, result.ma5[result.sell == True], 'v')

ax2.plot(result.index, result.portfolio_value)
print(result[['starting_cash', 'ending_cash', 'ending_value']])
plt.show()
# result['portfolio_value'].plot()
