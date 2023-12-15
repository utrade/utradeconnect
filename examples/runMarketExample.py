import os
from utradeconnect.index import UtradeConnect

import unittest
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


API_KEY = os.getenv("MARKET_DATA_API_KEY")
API_SECRET = os.getenv("MARKET_DATA_API_SECRET")
BASE_URL = os.getenv("BASE_URL")

class TestAttributes:
    api_key = API_KEY
    secret_key = API_SECRET
    source = "WEBAPI"
    market_connect = None
    token = None
    BASE_URL = BASE_URL


class TestUtradeMarketConnect(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a new UtradeMarketConnect instance if not already created
        if not TestAttributes.market_connect:
            TestAttributes.market_connect = UtradeConnect(
                apiKey=TestAttributes.api_key, 
                secretKey=TestAttributes.secret_key, 
                source=TestAttributes.source,
                root=TestAttributes.BASE_URL,
                disable_ssl=True,
                debug=True
            )

    def test_a_marketdata_login(self):
        try:
            # Call the marketdata_login method
            response = TestAttributes.market_connect.marketdata_login()
            print("Market Login: ", response)
        except Exception as e:
            print("Error occurred: ", str(e))

    def test_b_get_config(self):
        try:
            # Call the get_config method
            response = TestAttributes.market_connect.get_config()
            print("Config: ", response)
        except Exception as e:
            print("Error occurred: ", str(e))

    def test_c_get_quote(self):
        try:
            instruments = [
                {"exchangeSegment": 1, "exchangeInstrumentID": 22},
                {"exchangeSegment": 1, "exchangeInstrumentID": 2885},
            ]
            # Call the get_quote method
            response = TestAttributes.market_connect.get_quote(
                instruments=instruments, eventCode=1501, publishFormat="JSON"
            )
            print("Quote: ", response)
        except Exception as e:
            print("Error occurred: ", str(e))

    def test_d_send_subscription(self):
        try:
            instruments = [
                {"exchangeSegment": 1, "exchangeInstrumentID": 22},
                {"exchangeSegment": 1, "exchangeInstrumentID": 2885},
            ]
            # Call the send_subscription method
            response = TestAttributes.market_connect.send_subscription(
                instruments=instruments, eventCode=1501
            )
            print("Subscription : ", response)
        except Exception as e:
            print("Error occurred: ", str(e))

    def test_e_send_unsubscription(self):
        try:
            instruments = [
                {"exchangeSegment": 1, "exchangeInstrumentID": 22},
                {"exchangeSegment": 1, "exchangeInstrumentID": 2885},
            ]
            # Call the send_unsubscription method
            response = TestAttributes.market_connect.send_unsubscription(
                instruments=instruments, eventCode=1501
            )
            print("Unsubscription : ", response)
        except Exception as e:
            print("Error occurred: ", str(e))

    def test_f_get_master(self):
        try:
            exchangeSegmentList = ["NSECM"]
            # Call the get_master method
            response = TestAttributes.market_connect.get_master(
                exchangeSegmentList=exchangeSegmentList
            )
            print("Master : ", response)
        except Exception as e:
            print("Error occurred: ", str(e))

    def test_g_get_ohlc(self):
        try:
            # Call the get_ohlc method
            response = TestAttributes.market_connect.get_ohlc(
                exchangeSegment="NSECM",
                exchangeInstrumentID=26074,
                startTime="JUN 13 2023 090000",
                endTime="JUN 13 2023 153000",
                compressionValue=60,
            )
            print("OHLC : ", response)
        except Exception as e:
            print("Error occurred: ", str(e))

    def test_h_get_series(self):
        try:
            exchangeSegment = 1
            # Call the get_series method
            response = TestAttributes.market_connect.get_series(exchangeSegment)
            print("Series : ", response)
        except Exception as e:
            print("Error occurred: ", str(e))

    def test_i_get_equity_symbol(self):
        try:
                # Call the get_equity_symbol method
            response = TestAttributes.market_connect.get_equity_symbol(
                exchangeSegment=1, series="EQ", symbol="AXISBANK"
            )
            print("Equity Symbol : ", response)
        except Exception as e:
            print("Error occurred: ", str(e))

    def test_j_get_expiry_date(self):
        try:
                # Call the get_expiry_date method
            response = TestAttributes.market_connect.get_expiry_date(
                exchangeSegment=2, series="OPTIDX", symbol="NIFTY"
            )
            print("Expiry Date : ", response)
        except Exception as e:
            print("Error occurred: ", str(e))

    def test_k_get_future_symbol(self):
        try:
            # Call the get_future_symbol method
            response = TestAttributes.market_connect.get_future_symbol(
                exchangeSegment=2, series="FUTIDX", symbol="NIFTY", expiryDate="27APR2023"
            )
            print("Future Option : ", response)
        except Exception as e:
            print("Error occurred: ", str(e))

    def test_l_get_option_symbol(self):
        try:
            # Call the get_option_symbol method
            response = TestAttributes.market_connect.get_option_symbol(
                exchangeSegment=2,
                series="OPTIDX",
                symbol="NIFTY",
                expiryDate="27APR2023",
                optionType="PE",
                strikePrice=840,
            )
            print("Option Option : ", response)
        except Exception as e:
            print("Error occurred: ", str(e))

    def test_m_get_option_type(self):
        try:
            # Call the get_option_type method
            response = TestAttributes.market_connect.get_option_type(
                exchangeSegment=2, series="OPTIDX", symbol="NIFTY", expiryDate="27APR2023"
            )
            print("Option Type : ", response)
        except Exception as e:
            print("Error occurred: ", str(e))

    def test_n_get_index_list(self):
        try:
            # Call the get_index_list method
            response = TestAttributes.market_connect.get_index_list(exchangeSegment=2)
            print("Index List  : ", response)
        except Exception as e:
            print("Error occurred: ", str(e))
    
    def test_o_search_by_instrumentid(self):
        instruments = [{'exchangeSegment': 2, 'exchangeInstrumentID': 116472}]
        try:
            # Call the search_by_instrumentid method
            response = TestAttributes.market_connect.search_by_instrumentid(instruments=instruments)
            print("Search By Instrument ID : ", response)
        except Exception as e:
            print("Error occurred: ", str(e))
    
    def test_p_search_by_scriptname(self):
        try:
            # Call the search_by_instrumentid method
            response = TestAttributes.market_connect.search_by_scriptname(searchString='RELIANCE')
            print("Search By Instrument ID : [", response['result'][0], ', {.........]')
        except Exception as e:
            print("Error occurred: ", str(e))
    
    def test_q_marketdata_logout(self):
        try:
            # Call the marketdata_logout method
            response = TestAttributes.market_connect.marketdata_logout()
            print("Search By Instrument ID : ", response)
        except Exception as e:
            print("Error occurred: ", str(e))

    


if __name__ == "__main__":
    unittest.main()
