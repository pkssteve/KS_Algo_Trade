from zipline.api import order, record, symbol
import zipline
from yahoofinancials import YahooFinancials
import pandas as pd


def initialize(context):
    pass


def handle_data(context, data):
    order(symbol('AAPL'), 1)
    record(AAPL=data.current(symbol('AAPL'), 'price'))


# data 가져오기
ticker = 'AAPL'
start_date = '2015-01-01'
end_date = '2019-12-31'
freq = 'daily'
yahoo_financials = YahooFinancials(ticker)
df = yahoo_financials.get_historical_price_data(start_date, end_date, freq)
df = pd.DataFrame(df[ticker]['prices']).drop(['date'], axis=1).rename(columns={'formatted_date': 'date'})\
         .loc[:, ['date', 'open', 'high', 'low', 'close', 'volume', 'adjclose']].set_index('date')
df.index = pd.to_datetime(df.index)
data = df[['adjclose']]
data.columns = ['AAPL']
data = data.tz_localize('UTC')

# 실행
result = zipline.run_algorithm(start=data.index[0], end=data.index[-1], initialize=initialize, capital_base=1000,
                               handle_data=handle_data, data=data)
result.portfolio_value.pct_change().fillna(0).add(1).cumprod().sub(1).plot(label='portfolio')
print(result[['starting_cash', 'ending_cash', 'ending_value']].head())
