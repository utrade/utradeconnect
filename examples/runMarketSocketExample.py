from datetime import datetime
import os

from utradeconnect.index import UtradeConnect
from utradeconnect.marketSocket import MDSocket_io

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# MarketData API Credentials
API_KEY = os.getenv("MARKET_DATA_API_KEY")
API_SECRET = os.getenv("MARKET_DATA_API_SECRET")
BASE_URL = os.getenv("BASE_URL")
DEBUG = os.getenv("DEBUG", True)
DISABLE_SSL = os.getenv("DISABLE_SSL", True)

source = "WEBAPI"

# Initialise
utradeInstance = UtradeConnect(
    apiKey=API_KEY,
    secretKey=API_SECRET,
    source=source,
    root=BASE_URL,
    disable_ssl=DISABLE_SSL,
    debug=DEBUG,
    )

# Login for authorization token
response = utradeInstance.marketdata_login()

if DEBUG:
    print("got response", response)

# Store the token and userid
set_marketDataToken = response['result']['token']
set_muserID = response['result']['userID']

# Connecting to Marketdata socket
soc = MDSocket_io(set_marketDataToken, set_muserID, BASE_URL)

# Instruments for subscribing
Instruments = [
                {'exchangeSegment': 1, 'exchangeInstrumentID': 2885},
                {'exchangeSegment': 1, 'exchangeInstrumentID': 26000},
                {'exchangeSegment': 2, 'exchangeInstrumentID': 51601}
               ]

# Callback for connection
def on_connect():
    """Connect from the socket."""
    print('Market Data Socket connected successfully!')

    # # Subscribe to instruments
    print('Sending subscription request for Instruments - \n' + str(Instruments))
    response = utradeInstance.send_subscription(Instruments, 1501)
    print('Sent Subscription request!')
    print("Subscription response: ", response)

# Callback on receiving message
def on_message(data):
    print('I received a message!')

# Callback for message code 1501 FULL
def on_message1501_json_full(data):
    print('I received a 1501 Touchline message!' , data)

# Callback for message code 1502 FULL
def on_message1502_json_full(data):
    print('I received a 1502 Market depth message!' , data)

# Callback for message code 1505 FULL
def on_message1505_json_full(data):
    print('I received a 1505 Candle data message!' , data)

# Callback for message code 1507 FULL
def on_message1507_json_full(data):
    print('I received a 1507 MarketStatus data message!' , data)

# Callback for message code 1510 FULL
def on_message1510_json_full(data):
    print('I received a 1510 Open interest message!' , data)

# Callback for message code 1512 FULL
def on_message1512_json_full(data):
    print('I received a 1512 Level1,LTP message!' , data)

# Callback for message code 1105 FULL
def on_message1105_json_full(data):
    print('I received a 1105, Instrument Property Change Event message!' , data)


# Callback for message code 1501 PARTIAL
def on_message1501_json_partial(data):
    print('I received a 1501, Touchline Event message!' , data)

# Callback for message code 1502 PARTIAL
def on_message1502_json_partial(data):
    print('I received a 1502 Market depth message!' , data)

# Callback for message code 1505 PARTIAL
def on_message1505_json_partial(data):
    print('I received a 1505 Candle data message!' , data)

# Callback for message code 1510 PARTIAL
def on_message1510_json_partial(data):
    print('I received a 1510 Open interest message!' , data)

# Callback for message code 1512 PARTIAL
def on_message1512_json_partial(data):
    print('I received a 1512, LTP Event message!' , data)



# Callback for message code 1105 PARTIAL
def on_message1105_json_partial(data):
    print('I received a 1105, Instrument Property Change Event message!' , data)

# Callback for disconnection
def on_disconnect(data):
    print('Market Data Socket disconnected!')


# Callback for error
def on_error(data):
    """Error from the socket."""
    print('Market Data Error', data)


# Assign the callbacks.
soc.on_connect = on_connect
soc.on_message = on_message
soc.on_message1502_json_full = on_message1502_json_full
soc.on_message1505_json_full = on_message1505_json_full
soc.on_message1507_json_full = on_message1507_json_full
soc.on_message1510_json_full = on_message1510_json_full
soc.on_message1501_json_full = on_message1501_json_full
soc.on_message1512_json_full = on_message1512_json_full
soc.on_message1105_json_full = on_message1105_json_full
soc.on_message1502_json_partial = on_message1502_json_partial
soc.on_message1505_json_partial = on_message1505_json_partial
soc.on_message1510_json_partial = on_message1510_json_partial
soc.on_message1501_json_partial = on_message1501_json_partial
soc.on_message1512_json_partial = on_message1512_json_partial
soc.on_message1105_json_partial = on_message1105_json_partial
soc.on_disconnect = on_disconnect
soc.on_error = on_error


# Event listener
el = soc.get_emitter()
el.on('connect', on_connect)
el.on('1501-json-full', on_message1501_json_full)
el.on('1502-json-full', on_message1502_json_full)
el.on('1507-json-full', on_message1507_json_full)
el.on('1512-json-full', on_message1512_json_full)
el.on('1105-json-full', on_message1105_json_full)

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
soc.connect()
