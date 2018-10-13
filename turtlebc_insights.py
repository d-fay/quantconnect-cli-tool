# -*- coding: utf-8 -*-
import pandas
from code.turtle.scraper.test_data import SIGNAL_DATA

FILTER__EXCHANGE = 'Binance'

FILTER__BTC_VOLUME = 1500

# turtle = TurtleBC()
# signal_data = turtle.get_signals()
df = pandas.DataFrame(SIGNAL_DATA)  # Swapping out hard-coded data from the above calls

# enforce 6 decimals to show when printing our dataframe
pandas.set_option('display.float_format', lambda x: '%.6f' % x)

# df[['ADTV(1 Year)', 'Signal Price']] = df[['ADTV(1 Year)', 'Signal Price']].apply(pandas.to_numeric)
df['ADTV(1 Year)'] = df['ADTV(1 Year)'].apply(pandas.to_numeric)
df['Buy Balance'] = df['Buy Balance'].str[:-1].apply(pandas.to_numeric)

# print(df)
# print(df['ADTV(1 Year)'] > 100)

# FILTER ALL SIGNALS INTO NEW DATAFRAME
df_filtered = df[(df['ADTV(1 Year)'] > FILTER__BTC_VOLUME) & (df['Exchange'] == FILTER__EXCHANGE)]

print('\nThe following is a filtered list of market signals for {} from TurtleBC: \n{}\n'.format(FILTER__EXCHANGE, df_filtered))

# count of markets with a positive roi (100% buy balance is principle investment)
print('Number of filtered markets with a positive ROI: {}'.format(len(df_filtered[df_filtered["Buy Balance"] > 100])))
print('Number of filtered markets with a negative ROI: {}'.format(len(df_filtered[df_filtered["Buy Balance"] < 100])))
print('Win/Loss ratio: {}'.format(len(df_filtered[df_filtered["Buy Balance"] > 100])/len(df_filtered[df_filtered["Buy Balance"] < 100])))

# print('\nThe following filtered list of markets have a positive ROI: \n{}'.format(df_filtered[df_filtered["Buy Balance"] > 100]))

# print(df_filtered[df_filtered["Buy Balance"] < 100].mean())
