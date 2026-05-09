1. Nifty 50 Backtesting Engine (Python)
This is my first Quantitative Finance project, created to bridge the gap between market theory and coding.
The project is a Limit Order Book (LOB) Matching Engine that replays historical intraday data to simulate real-world trading. It focuses on market microstructure, order precedence rules, and financial data normalization.

2. Features
-> Matching Algorithm: Implements Price-Time Priority (FIFO) to match buyers and sellers.

-> NSE Compliance: Strict validation of the ₹0.05 tick size for the Indian market.

-> Live Data Integration: Automatically fetches and flattens MultiIndex data from Yahoo Finance.

-> Trade Logging: Generates a detailed audit trail of every execution (Price, Qty, and Participant IDs).

3. Technologies Used
-> Python (Core Logic)

-> Pandas (Data Manipulation & Normalization)

-> yfinance (Market Data API)

-> Git & GitHub (Version Control)

4. Learning Resources & Approach

-> Theoretical Foundation: Concepts based on "Trading and Exchanges: Market Microstructure for Practitioners" by Larry Harris.

-> Technical Guidance: Used AI tools (Gemini) to architect the exchange rules, handle MultiIndex data quirks, and refine the matching logic.

-> Market Standards: Researched National Stock Exchange (NSE) tick rules to ensure the simulation was realistic for the Nifty 50 index.

5. How it Works
-> Order Entry: The engine creates orders for every minute of market activity.

-> Validation: Every order must pass a "Tick Test" to ensure it lands on a valid price point.

-> The Book: Orders are stored in a "Bid" or "Ask" queue and sorted by price.

-> Execution: A trade is triggered only when the Buy price meets or exceeds the Sell price, prioritizing the order that arrived first.

6. How to Run

-> Clone the repository(copy and paste this in git bash):
      git clone https://github.com/Rushikesh273/Backtesting_Engine_For_nifty50.git
   
-> Install dependencies(in IDE terminal):
     pip install yfinance pandas
     
-> Run the engine(in IDE terminal):
     python backtesting_engine.py
