"""
THIS CLASS HANDLES ALL THE LOGIC FOR OBTAINING TURTLEBC.COM WEBSITE DATA

Parameter configuration files are located in ../conf/settings.ini
"""
import os
import datetime as dt
import logging as log

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


"""
Login to TurtleBC.com and parse content from poloniex markets
"""


class TurtleBC:

    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dotenv_path = os.path.join(os.getcwd(), '.env')
        load_dotenv(self.dotenv_path)
        self.market_url_endpoint = os.environ['TURTLEBC_MARKET_URL']
        self.day_offset = int(os.environ['TURTLEBC_DAY_OFFSET'])

    def get_signals(self):
        login_url = 'https://www.turtlebc.com/users/sign_in'
        payload = {
            'utf8': '✓',
            'authenticity_token': '',
            'user[email]': os.environ['TURTLEBC_USER'],
            'user[password]': os.environ['TURTLEBC_PASS'],
            'user[remember_me]': 0
        }

        web_session = requests.session()
        login_page = web_session.get(login_url)  # GET request to the login page
        login_soup = BeautifulSoup(login_page.content, 'lxml')

        # get the csrf-token from the meta content tag
        meta_tags = login_soup.find_all('meta')
        for tag in meta_tags:
            if tag.get('name') == 'csrf-token':
                payload['authenticity_token'] = tag.get('content')

        # send the login payload and login request
        login_result = web_session.post(login_url, params=payload, headers=dict(referer=login_url))
        # log the result: login success == "200 https://www.turtlebc.com/turtle_markets"
        if login_result.status_code == 200 and login_result.url == 'https://www.turtlebc.com/turtle_markets':
            log.debug(str(login_result.status_code) + " " + str(login_result.url))
            log.info("login attempt successful")
        elif login_result.status_code != 200 or login_result.url != 'https://www.turtlebc.com/turtle_markets':
            log.warning("login attempt returned unexpected result:", login_result.status_code, login_result.url)

        # - - - - - - - RETRIEVE MARKET TABLE DATA - - - - - - -

        # attempt to retrieve the market data page and log result
        markets_page = web_session.get(self.market_url_endpoint)
        # success == "200 " + str(MARKET_URL_ENDPOINT)
        if markets_page.status_code == 200 and markets_page.url == self.market_url_endpoint:
            log.debug(str(markets_page.status_code) + " " + str(markets_page.url))
            log.info("market page retrieved successfully")
        elif markets_page.status_code == 200 and markets_page.url == self.market_url_endpoint:
            log.warning("market page retrieval returned unexpected result:", markets_page.status_code, markets_page.url)

        log.info("Parsing TurtleBC content...")
        # soupify market page
        market_soup = BeautifulSoup(markets_page.content, 'lxml')

        # isolate the coins table by html tag
        coins_table = market_soup.find_all('tr')
        # get column headers (first row of table)
        table_keys = list(coins_table[0].stripped_strings)
        # print("table_keys = ", table_keys)
        log.debug("table_keys = " + str(table_keys))

        # populate a list with the coins table data
        coins_data = []

        # for each row in the market table
        for i in range(1, len(coins_table)):
            coin_row = list(coins_table[i].stripped_strings)
            # append a dictionary to coins_data list containing the column headers as keys and the row data as values
            if len(coin_row) == len(table_keys):
                coins_data.append(dict(zip(table_keys, coin_row)))
                log.debug(coin_row)
            # print(list(coins_table[i].stripped_strings))

        # print out the coins_data list of coin dictionaries
        # modified to only print markets with more than ₿100
        # log.debug("coins_data = [")
        # for coin_dict in coins_data:
        #     adtv_1y = float(coin_dict.get('ADTV(1 Year)'))
        #     adtv = float(coin_dict.get('ADTV'))
        #     if adtv >= int(MINIMUM_BTC_VOLUME) and adtv_1y >= int(MINIMUM_BTC_VOLUME):
        #         log.debug(coin_dict)
        # log.debug("]")

        log.info("returning market data from Turtlebc()")
        return coins_data

    def get_filtered_btc_signals(self):
        signals_all = self.get_signals()
        new_signal_flag = False
        signals_filtered = []
        date_t = dt.date.today() + dt.timedelta(days=self.day_offset)

        for signal_dict in signals_all:
            if str(signal_dict['Market']).startswith('BTC') or str(signal_dict['Market']).endswith('BTC'):
                # uncomment print to see recent signal data (used for testing and development)
                # print(json.dumps(signal_dict, sort_keys=True, indent=4))

                # ensure the signal's date is today's
                if str(date_t) in signal_dict['Signal Time']:
                    if not new_signal_flag:
                        log.info("Trade signal(s) found for today... Attempting to execute trade(s)...")
                    signals_filtered.append(signal_dict)
                    new_signal_flag = True

        if new_signal_flag:
            log.info("Found new signals today! ^_^")
            return signals_filtered
        else:
            log.info("No signals today -_-")
            return None
