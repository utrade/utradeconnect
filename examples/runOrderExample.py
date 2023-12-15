import os
import unittest

from utradeconnect.index import UtradeConnect
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


API_KEY = os.getenv("ORDER_API_KEY")
API_SECRET = os.getenv("ORDER_API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
BASE_URL = os.getenv("BASE_URL")
DEBUG = os.getenv("DEBUG", False)
DISABLE_SSL = os.getenv("DISABLE_SSL", True)

class TestAttributes:
    api_key = API_KEY
    secret_key = API_SECRET
    source = "WEBAPI"
    accessToken = ACCESS_TOKEN
    order_connect = None
    token = None
    client_id = "VIEW1"
    user_id = "VIEW1"
    app_order_id = None
    base_url = BASE_URL
    

class TestUtradeOrderConnect(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a new UtradeOrderConnect instance if not already created
        if not TestAttributes.order_connect:
            if DEBUG:
                print(
                    f"Not already created, creating new instance | "
                    "Api Key: {TestAttributes.api_key} | "
                    "Secret Key: {TestAttributes.secret_key} | "
                    "Source: {TestAttributes.source} | "
                    "Base Url: {TestAttributes.baseUrl} "
                )
            TestAttributes.order_connect = UtradeConnect(
                apiKey=TestAttributes.api_key,
                secretKey=TestAttributes.secret_key,
                source=TestAttributes.source,
                root=TestAttributes.base_url,
                debug=True,
                disable_ssl=True
            )


    def test_a_marketdata_login(self):
        try:
            # Call the interactive_login method
            response = TestAttributes.order_connect.interactive_login(TestAttributes.accessToken)
            if DEBUG:
                print("Interactive Login : ", response)
        except Exception as e:
            print("Error occurred during marketdata login:", str(e))


    def test_c_get_order_book(self):
        try:
            # Call the get_order_book method
            response = TestAttributes.order_connect.get_order_book(
                clientID=TestAttributes.client_id
            )
            print("Order Book: ", response)
        except Exception as e:
            print("Error occurred while getting order book:", str(e))

    def test_b_place_order(self):
        try:
            # Call the place_order method
            response = TestAttributes.order_connect.place_order(
                exchangeSegment="NSECM",
                exchangeInstrumentID=2885,
                productType="MIS",
                orderType="LIMIT",
                orderSide="BUY",
                timeInForce="DAY",
                disclosedQuantity=0,
                orderQuantity=10,
                limitPrice=300,
                stopPrice=0,
                orderUniqueIdentifier="454845",
                clientID=TestAttributes.client_id,
            )
            TestAttributes.app_order_id = (
                response["result"] and response["result"]["AppOrderID"]
            )
            print("Order: ", response)
        except Exception as e:
            print("Error occurred while placing order:", str(e))

    def test_d_modify_order(self):
        try:
            # Call the modify_order method
            response = TestAttributes.order_connect.modify_order(
                appOrderID=TestAttributes.app_order_id,
                modifiedProductType="NRML",
                modifiedOrderType="LIMIT",
                modifiedOrderQuantity=8,
                modifiedDisclosedQuantity=0,
                modifiedLimitPrice=1405,
                modifiedStopPrice=0,
                modifiedTimeInForce="DAY",
                orderUniqueIdentifier="454845",
                clientID=TestAttributes.client_id,
            )
            print("Modify Order: ", response)
        except Exception as e:
            print("Error occurred while modifying order:", str(e))

    def test_e_get_order_history(self):
        try:
            # Call the get_order_history method
            response = TestAttributes.order_connect.get_order_history(
                appOrderID=TestAttributes.app_order_id,
                clientID=TestAttributes.client_id,
            )
            print("Order History : ", response)
        except Exception as e:
            print("Error occurred while getting order history:", str(e))

    def test_f_cancel_order(self):
        try:
            # Call the cancel_order method
            response = TestAttributes.order_connect.cancel_order(
                appOrderID=TestAttributes.app_order_id,
                orderUniqueIdentifier="454845",
                clientID=TestAttributes.client_id,
            )
            print("Cancel Order : ", response)
        except Exception as e:
            print("Error occurred while canceling order:", str(e))

    def test_g_place_bracketorder(self):
        try:
            # Call the place_bracketorder method
            response = TestAttributes.order_connect.place_bracketorder(
                exchangeSegment="NSECM",
                exchangeInstrumentID=2885,
                orderType="LIMIT",
                orderSide="BUY",
                disclosedQuantity=0,
                orderQuantity=10,
                limitPrice=59,
                squarOff=1,
                stopLossPrice=1,
                trailingStoploss=1,
                isProOrder=False,
                orderUniqueIdentifier="454845",
            )
            TestAttributes.app_order_id = (
                response and response["result"] and response["result"]["AppOrderID"]
            )
            print("Bracket Order: ", response)
        except Exception as e:
            print("Error occurred while placing bracket order:", str(e))

    def test_h_modify_bracketorder(self):
        try:
            # Call the modify_bracketorder method
            response = TestAttributes.order_connect.modify_bracketorder(
                appOrderID=TestAttributes.app_order_id,
                orderQuantity=2,
                limitPrice=22,
                stopLossPrice=0.2,
                clientID=TestAttributes.client_id,
            )
            print("Bracket Order: ", response)
        except Exception as e:
            print("Error occurred while modifying bracket order:", str(e))

    def test_i_bracketorder_cancel(self):
        try:
            # Call the bracketorder_cancel method
            response = TestAttributes.order_connect.bracketorder_cancel(
                appOrderID=TestAttributes.app_order_id
            )
            print(" Place Bracketorder : ", response)
        except Exception as e:
            print("Error occurred while canceling bracket order:", str(e))

    def test_j_get_profile(self):
        try:
            # Call the get_profile method
            response = TestAttributes.order_connect.get_profile(
                clientID=TestAttributes.client_id
            )
            print(" Profile : ", response)
        except Exception as e:
            print("Error occurred while getting profile:", str(e))
    def test_k_get_balance(self):
        try:
            # Call the get_balance method
            response = TestAttributes.order_connect.get_balance(
                clientID=TestAttributes.client_id
            )
            print(" Balance : ", response)
        except Exception as e:
            print("Error occurred while getting balance:", str(e))

    def test_l_get_trade(self):
        try:
            # Call the get_trade method
            response = TestAttributes.order_connect.get_trade(
                clientID=TestAttributes.client_id
            )
            print(" Trade Book : ", response)
        except Exception as e:
            print("Error occurred while getting trade book:", str(e))

    def test_m_get_holding(self):
        try:
            # Call the get_holding method
            response = TestAttributes.order_connect.get_holding(
                clientID=TestAttributes.client_id
            )
            print("Holding : ", response)
        except Exception as e:
            print("Error occurred while getting holding:", str(e))

    def test_n_get_position_daywise(self):
        try:
            # Call the get_position_daywise method
            response = TestAttributes.order_connect.get_position_daywise(
                clientID=TestAttributes.client_id
            )
            print("DayWise Positions: ", response)
        except Exception as e:
            print("Error occurred while getting daywise positions:", str(e))

    def test_o_get_position_netwise(self):
        try:
            # Call the get_position_netwise method
            response = TestAttributes.order_connect.get_position_netwise(
                clientID=TestAttributes.client_id
            )
            print("NetWise Positions: ", response)
        except Exception as e:
            print("Error occurred while getting netwise positions:", str(e))


    # def test_t_convert_position(self):
    #     # Call the convert_position method
    #     response = TestAttributes.order_connect.convert_position(
    #         exchangeSegment="NSECM",
    #         exchangeInstrumentID=2885,
    #         targetQty=10,
    #         isDayWise=True,
    #         oldProductType="MIS",
    #         newProductType="NRML",
    #         clientID=TestAttributes.clientID,
    #     )
    #     print("Position Convert : ", response)

    def test_u_place_cover_order(self):
        try:
            # Call the place_cover_order method
            response = TestAttributes.order_connect.place_cover_order(
                exchangeSegment="NSECM",
                exchangeInstrumentID=2885,
                orderSide="BUY",
                orderType="LIMIT",
                orderQuantity=2,
                disclosedQuantity=1,
                limitPrice=1802,
                stopPrice=1899,
                orderUniqueIdentifier="454845",
                clientID=TestAttributes.client_id,
            )
            print("Cover Order : ", response)

            if not 'error' in response:
                # Call the modify_cover_order method
                response = TestAttributes.order_connect.modify_cover_order(
                    appOrderID= response['result']['AppOrderID'],
                    orderQuantity=3,
                    limitPrice=1802,
                    stopPrice=1899,
                    clientID=TestAttributes.client_id,
                )
                print("Modify Cover Order : ", response)

            if not 'error' in response:
                response = TestAttributes.order_connect.exit_cover_order(
                    appOrderID= response['result']['AppOrderID'],
                    clientID=TestAttributes.client_id,
                )
                print("Exit Cover Order : ", response)
        except Exception as e:
            print("Error occurred while placing cover order:", str(e))

    def test_v_cancelall_order(self):
        try:
            # Call the cancelall_order method
            response = TestAttributes.order_connect.cancelall_order(
                exchangeInstrumentID=22, exchangeSegment="NSECM"
            )
            print("Cancelall Order : ", response)
        except Exception as e:
            print("Error occurred while canceling all orders:", str(e))

    def test_w_interactive_logout(self):
        try:
            # Call the interactive_logout method
            response = TestAttributes.order_connect.interactive_logout(
                clientID=TestAttributes.client_id
            )
            print("Interactive Logout : ", response)
        except Exception as e:
            print("Error occurred during interactive logout:", str(e))

if __name__ == "__main__":
    unittest.main()
