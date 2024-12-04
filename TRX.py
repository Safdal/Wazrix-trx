import requests
import time
import schedule
from datetime import datetime

# WazirX API endpoints
BASE_URL = 'https://api.wazirx.com'
TRADE_URL = 'https://api.wazirx.com/api/v2'

# Replace these with your WazirX API key and secret
API_KEY = 'ephvHtwUvL80azJB4GStUUumNnbrSodRjh5Icmp3BUTb77cJwc5myPQ0wmZxHUvm'
API_SECRET = '****************************************'

def get_market_price():
    response = requests.get(f'{BASE_URL}/api/v2/tickers/trxinr')
    data = response.json()
    return float(data['ticker']['last'])

def place_market_order(quantity):
    order_data = {
        'symbol': 'trxinr',
        'side': 'buy',
        'type': 'market',
        'quantity': quantity,
        'recvWindow': 5000,
    }
    response = requests.post(f'{TRADE_URL}/order', headers={
        'X-Api-Key': API_KEY,
    }, data=order_data)
    return response.json()

def place_stop_loss_order(order_id, stop_price):
    # Stop Loss order logic
    pass

def place_take_profit_order(order_id, target_price):
    # Take Profit order logic
    pass

def update_trailing_stop(buy_price, initial_stop, trailing_trigger):
    stop_loss = buy_price * (1 - initial_stop / 100)
    current_price = get_market_price()
    
    while True:
        current_price = get_market_price()
        if current_price >= buy_price + trailing_trigger:
            stop_loss = max(stop_loss, current_price - trailing_trigger)
            print(f'New Stop Loss Updated: {stop_loss}')
        elif current_price <= stop_loss:
            print(f'Stop Loss Hit at: {stop_loss}')
            break
        time.sleep(5)

def trade():
    print(f"Trading at {datetime.now()}")
    market_price = get_market_price()
    quantity = 10  # Replace with the amount to trade
    
    order_response = place_market_order(quantity)
    print(f"Order placed: {order_response}")
    
    buy_price = market_price  # Simulated buy price
    stop_loss_price = buy_price * (1 - 0.7 / 100)
    target_price = buy_price * (1 + 1.5 / 100)
    
    print(f"Buy Price: {buy_price}, Stop Loss: {stop_loss_price}, Target: {target_price}")
    
    # Simulating trailing stop loss
    update_trailing_stop(buy_price, 0.7, 2)

# Schedule the task to run daily at 9:30 AM
schedule.every().day.at("09:30").do(trade)

print("Trading bot running...")
while True:
    schedule.run_pending()
    time.sleep(1)
