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

    def test_v_cancelall_order(self):
        try:
            # Call the cancelall_order method
            response = TestAttributes.order_connect.cancelall_order(
                exchangeInstrumentID=22, exchangeSegment="NSECM"
            )
            print("Cancelall Order : ", response)
        except Exception as e:
            print("Error occurred while canceling all orders:", str(e))

    def test_w_place_spread_order(self):
        try:
            response = TestAttributes.order_connect.place_spread_order(
                exchangeSegment="NSEFO",
                exchangeInstrumentID=13620424,
                productType="NRML",
                action="BUY",
                orderType="LIMIT",
                orderDuration="DAY",
                quantity=75,
                spreadPrice=1000,
                spreadExchangeInstrumentID=13620424,
                clientID=TestAttributes.client_id,
            )
            print("Place Spread Order : ", response)
        except Exception as e:
            print("Error occurred while placing spread order:", str(e))

    def test_x_modify_spread_order(self):
        try:
            response = TestAttributes.order_connect.modify_spread_order(
                orderID="1240992685",
                spreadPrice=900,
                quantity=75,
                productType="NRML",
                action="BUY",
                orderDuration="DAY",
                spreadExchangeInstrumentID=13687399,
                clientID=TestAttributes.client_id,
            )
            print("Modify Spread Order : ", response)
        except Exception as e:
            print("Error occurred while modifying spread order:", str(e))

    def test_y_get_spread_order_book(self):
        try:
            response = TestAttributes.order_connect.get_spread_order_book(
                clientID=TestAttributes.client_id
            )
            print("Spread Order Book : ", response)
        except Exception as e:
            print("Error occurred while getting spread order book:", str(e))

    def test_z_cancel_spread_order(self):
        try:
            response = TestAttributes.order_connect.cancel_spread_order(
                orderID="1240992685",
                clientID=TestAttributes.client_id,
            )
            print("Cancel Spread Order : ", response)
        except Exception as e:
            print("Error occurred while canceling spread order:", str(e))

    def test_za_get_order_margin(self):
        try:
            response = TestAttributes.order_connect.get_order_margin(
                portfolio=[
                    {
                        "exchange": 1,
                        "exchangeInstrumentId": 2885,
                        "productType": "NRML",
                        "orderType": "LIMIT",
                        "orderSide": "BUY",
                        "quantity": 1,
                        "price": 1200,
                        "stopPrice": 1180,
                        "orderSessionType": "NORMAL",
                    }
                ],
                clientID=TestAttributes.client_id,
            )
            print("Order Margin : ", response)
        except Exception as e:
            print("Error occurred while getting order margin:", str(e))

    def test_zb_get_modify_order_margin(self):
        try:
            response = TestAttributes.order_connect.get_modify_order_margin(
                orderID="1210910568",
                instrumentInformation={
                    "exchange": 1,
                    "exchangeInstrumentId": 2885,
                    "orderSide": "BUY",
                    "orderSessionType": 1,
                    "productType": "NRML",
                    "orderType": "LIMIT",
                    "quantity": 1,
                    "price": 1200,
                    "stopPrice": 1190,
                },
                clientID=TestAttributes.client_id,
            )
            print("Modify Order Margin : ", response)
        except Exception as e:
            print("Error occurred while getting modify order margin:", str(e))

    def test_zc_squareoff(self):
        try:
            response = TestAttributes.order_connect.squareoff(
                exchangeSegment="NSECM",
                exchangeInstrumentID=2885,
                productType="MIS",
                squareoffMode="Regular",
                squareOffQtyValue=1,
                positionSquareOffQuantityType="ExactQty",
                clientID=TestAttributes.client_id,
            )
            print("Square Off : ", response)
        except Exception as e:
            print("Error occurred while squaring off:", str(e))

    def test_zd_squareoff_all(self):
        try:
            response = TestAttributes.order_connect.squareoff_all(
                squareoffMode="Regular",
                clientID=TestAttributes.client_id,
            )
            print("Square Off All : ", response)
        except Exception as e:
            print("Error occurred while squaring off all:", str(e))

    def test_ze_interactive_logout(self):
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
