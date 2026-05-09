import time
import pandas as pd
import yfinance as yf

def get_nse_tick(price):
    if price < 2.00: 
        return 0.01 
    return 0.05     

def is_valid_tick(price):
    tick = get_nse_tick(price)
    if tick == 0:
        return False
    # Multiply by 100 to work in 'paise' and avoid decimal floating errors
    return round(price * 100) % round(tick * 100) == 0

class Order:
    def __init__(self, order_id, order_type, price, quantity):
        self.order_id = order_id
        self.order_type = order_type.upper().strip() #Buy or Sell/Bid or Ask order
        self.price = round(price, 2)
        self.quantity = quantity
        self.timestamp = time.time()

    def __repr__(self):
        # Using ljust() for neatness     
        type_str = str(self.order_type).ljust(4)
        id_str = str(self.order_id).ljust(2)
        price_str = str(self.price).ljust(7)
        qty_str = str(self.quantity)
        
        return type_str + " ID:" + id_str + " | Price: ₹" + price_str + " | Qty: " + qty_str


class OrderBook:
    def __init__(self):
        self.bids = []  # Buy orders in descending order
        self.asks = []  # Sell orders in ascending order
        self.ltp = 0.0  # Last Traded Price (Price of most recent Trade)
        self.trade_log = [] # List of dictionaries to feed into Pandas later

    def add_order(self, order):
        if not is_valid_tick(order.price):
            id_str = str(order.order_id).ljust(2)
            print("Order Rejected: ID:" + id_str + " -> Invalid tick size for price ₹" + str(order.price))
            return

        if order.order_type == 'BUY': # Find the correct book 
            self.bids.append(order)
            self.bids.sort(key=lambda x: (-x.price, x.timestamp))
        elif order.order_type == 'SELL':
            self.asks.append(order)
            self.asks.sort(key=lambda x: (x.price, x.timestamp))
        else:
            print("Order Rejected: Side must be 'BUY' or 'SELL'")
            return
        
        print("Order Accepted: " + str(order))
        self.match() # Match orders after a new order is added

    def match(self):
        # Matching goes on as long as the highest bid is >= the lowest ask
        while self.bids and self.asks and self.bids[0].price >= self.asks[0].price:
            best_bid = self.bids[0]
            best_ask = self.asks[0]

            # Find the trade price based on time priority to find current best bid or ask
            if best_bid.timestamp < best_ask.timestamp:
                trade_price = best_bid.price
            else:
                trade_price = best_ask.price

            # Find the trade quantity (the smaller of the two orders)
            trade_qty = min(best_bid.quantity, best_ask.quantity)

            # Update the Last Traded Price
            self.ltp = trade_price

            # Log the trade for Pandas
            self.trade_log.append({
                'Time': time.strftime('%H:%M:%S'),
                'Price': trade_price,
                'Quantity': trade_qty,
                'Buyer_ID': best_bid.order_id,
                'Seller_ID': best_ask.order_id
            })
            
            # Use rjust function for aligning purpose
            qty_str = str(trade_qty).rjust(3)
            price_str = str(trade_price).ljust(7)
            print(">>> Trade Executed: " + qty_str + " shares at ₹" + price_str + " <<<")

            # Reduce quantity (reduces quantity or number of shares of a buy or sell order based on how much has been used in a trade)
            best_bid.quantity -= trade_qty
            best_ask.quantity -= trade_qty

            # Orders completed should be removed 
            if best_bid.quantity == 0:
                self.bids.pop(0)
            if best_ask.quantity == 0:
                self.asks.pop(0)

if __name__ == "__main__":
    nse = OrderBook()
    target_ticker = "^NSEI" # Nifty 50 Index
    start_date = "2026-05-06"
    end_date = "2026-05-07" 

    print("--- BACKTEST START ---")
    print("Fetching data for: " + start_date)

    try:
        
        df = yf.download(target_ticker, start=start_date, end=end_date, interval="1m")

        if df.empty:
            print("No data found. Is the ticker correct?")
        else:
            
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            df = df.reset_index()
            print("Loaded " + str(len(df)) + " minutes of market activity.")

            for index, row in df.iterrows():
                # Even indices are BUY and Odd indices are SELL
                side = "BUY" if index % 2 == 0 else "SELL"
                
                market_price = float(row['Close'])
                quantity = 50 
                
                new_order = Order(
                    order_id = index + 1000, 
                    order_type = side,
                    price = market_price,
                    quantity = quantity
                )
                
                 
                nse.add_order(new_order)

    except Exception as e:
        print("An error occurred during the data feed: " + str(e))

    
    print("\n" + "="*60)
    print(" REPLAY RESULTS: NIFTY 50 SESSION (MAY 6, 2026) ")
    print("="*60)
    
    if nse.trade_log:
        trades_df = pd.DataFrame(nse.trade_log)
        print(trades_df.to_string(index=False, justify='center'))
        print("\nTotal Trades Executed: " + str(len(nse.trade_log)))
    else:
        print("Simulation complete. No trades were matched.")
        print("Tip: If the market moved in one direction, Bids and Asks might not have met.")
    
    print("="*60 + "\n")

    print("\n" + "-"*30)
    print("BACKTEST COMPLETE")
    print("Total Orders Processed: " + str(len(df)))
    print("Total Trades Matched:   " + str(len(nse.trade_log)))
    print("-"*30)

