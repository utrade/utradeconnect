# Define API routes for Orders (apiconverter 3.5.11.1 interactive surface)
orders_routes = {
    "user.login": "/user/session",
    "user.logout": "/user/session",
    "user.profile": "/user/profile",
    "user.balance": "/user/balance",
    "trades": "/orders/trades",
    "order.status": "/orders",
    "order.place": "/orders/",
    "order.modify": "/orders/",
    "order.cancel": "/orders/",
    "order.cancelall": "/orders/cancelall",
    "order.spread": "/orders/spread",
    "order.margindetails": "/orders/margindetails",
    "order.modifyordermargindetails": "/orders/modifyordermargindetails",
    "order.history": "/orders",
    "portfolio.positions": "/portfolio/positions",
    "portfolio.holdings": "/portfolio/holdings",
    "portfolio.positions.convert": "/portfolio/positions/convert",
    "portfolio.squareoff": "/api/V2/interactive/portfolio/squareoff",
    "portfolio.squareoffall": "/api/V2/interactive/portfolio/squareoffall",
    "portfolio.dealerpositions": "/portfolio/positions",
    "order.dealer.status": "/orders",
    "dealer.trades": "/orders/trades",
}

# Define API routes for Market Data (/apibinarymarketdata)
market_routes = {
    "market.login": "/apibinarymarketdata/auth/login",
    "market.logout": "/apibinarymarketdata/auth/logout",
    "market.config": "/apibinarymarketdata/config/clientConfig",
    "market.instruments.master": "/apibinarymarketdata/instruments/master",
    "market.instruments.subscription": "/apibinarymarketdata/instruments/subscription",
    "market.instruments.unsubscription": "/apibinarymarketdata/instruments/subscription",
    "market.instruments.ohlc": "/apibinarymarketdata/instruments/ohlc",
    "market.instruments.indexlist": "/apibinarymarketdata/instruments/indexlist",
    "market.instruments.quotes": "/apibinarymarketdata/instruments/quotes",
    "market.search.instrumentsbyid": "/apibinarymarketdata/search/instrumentsbyid",
    "market.search.instrumentsbystring": "/apibinarymarketdata/search/instruments",
    "market.instruments.instrument.series": "/apibinarymarketdata/instruments/instrument/series",
    "market.instruments.instrument.equitysymbol": "/apibinarymarketdata/instruments/instrument/symbol",
    "market.instruments.instrument.futuresymbol": "/apibinarymarketdata/instruments/instrument/futureSymbol",
    "market.instruments.instrument.optionsymbol": "/apibinarymarketdata/instruments/instrument/optionSymbol",
    "market.instruments.instrument.optiontype": "/apibinarymarketdata/instruments/instrument/optionType",
    "market.instruments.instrument.expirydate": "/apibinarymarketdata/instruments/instrument/expiryDate",
    "market.instruments.instrument.strikeprice": "/apibinarymarketdata/instruments/instrument/strikePrice",
}

all_routes = {**orders_routes, **market_routes}

def get_orders_routes():
    """
    Returns the dictionary containing API routes for Orders.

    Returns:
        dict: Dictionary containing API routes for Orders.
    """
    return orders_routes

def get_market_routes():
    """
    Returns the dictionary containing API routes for Market Data.

    Returns:
        dict: Dictionary containing API routes for Market Data.
    """
    return market_routes

def get_all_routes():
    """
    Returns the dictionary containing all API routes.

    Returns:
        dict: Dictionary containing all API routes.
    """
    return all_routes
