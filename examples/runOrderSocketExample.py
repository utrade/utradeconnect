

# Interactive API Credentials
import os
from utradeconnect.index import UtradeConnect
from utradeconnect.orderSocket import OrderSocket_io
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

API_KEY = os.getenv("ORDER_API_KEY")
API_SECRET = os.getenv("ORDER_API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
BASE_URL = os.getenv("BASE_URL")
DEBUG = os.getenv("DEBUG", False)
DISABLE_SSL = os.getenv("DISABLE_SSL", True)
source = "WEBAPI"

# Initialise
utradeInstance = UtradeConnect(
    apiKey=API_KEY,
    secretKey=API_SECRET,
    source=source,
    root=BASE_URL,
    debug=DEBUG,
    disable_ssl=DISABLE_SSL
)

# Login for authorization token
response = utradeInstance.interactive_login(ACCESS_TOKEN)
print("Login: ", response)
# Store the token and userid
set_interactiveToken = response['result']['token']
set_iuserID = response['result']['userID']
print("Login: ", response)

# Connecting to Interactive socket
soc = OrderSocket_io(set_interactiveToken, set_iuserID, BASE_URL)


# Callback for connection
def on_connect():
    """Connect from the socket."""
    print('Interactive socket connected successfully!')


# Callback for receiving message
def on_message():
    print('I received a message!')


# Callback for joined event
def on_joined(data):
    print('Interactive socket joined successfully!' , data)


# Callback for error
def on_error(data):
    print('Interactive socket error!' , data)


# Callback for order
def on_order(data):
    print("Order placed!" , data)


# Callback for trade
def on_trade(data):
    print("Trade Received!" , data)


# Callback for position
def on_position(data):
    print("Position Retrieved!" , data)


# Callback for trade conversion event
def on_tradeconversion(data):
    print("Trade Conversion Received!" , data)


# Callback for message logout
def on_messagelogout(data):
    print("User logged out!" , data)


# Callback for disconnection
def on_disconnect():
    print('Interactive Socket disconnected!')


# Assign the callbacks.
soc.on_connect = on_connect
soc.on_message = on_message
soc.on_joined = on_joined
soc.on_error = on_error
soc.on_order = on_order
soc.on_trade = on_trade
soc.on_position = on_position
soc.on_tradeconversion = on_tradeconversion
soc.on_messagelogout = on_messagelogout
soc.on_disconnect = on_disconnect

# Event listener
el = soc.get_emitter()
el.on('connect', on_connect)
el.on('order', on_order)
el.on('trade', on_trade)
el.on('position', on_position)
el.on('tradeConversion', on_tradeconversion)

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
soc.connect()
