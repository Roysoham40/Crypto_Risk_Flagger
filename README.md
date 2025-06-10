# Crypto Transaction Risk Flagger

A Python script that fetches Ethereum transactions for a wallet using the Etherscan API, converts ETH to USD via CoinGecko API, and flags high-risk transactions (> $10,000 or within 1 hour) for AML compliance. Flagged transactions are saved to a CSV.

## Features
- Fetches transactions via Etherscan API.
- Converts ETH to USD with real-time CoinGecko data.
- Flags transactions: > $10,000 or rapid transfers (1-hour window).
- Saves results to CSV (timestamp, hash, recipient, value_eth, value_usd, reason).
- Handles API errors and rate limits.

## Prerequisites
- Python 3.6+
- [Etherscan API key](https://etherscan.io/apis) (free)
- Ethereum wallet address with transactions
- Libraries: `requests`, `pandas`, `python-dateutil`

## Installation
1. Clone repo:
   ```bash
   git clone https://github.com/Roysoham40/crypto-transaction-risk-flagger.git
   cd crypto-transaction-risk-flagger

2. Set up virtual environment:
   python -m venv venv

3. Install libraries:
   pip install requests pandas python-dateutil

4. Configure crypto_risk_flagger.py:
   python
   
   Set Etherscan API key:
   ETHERSCAN_API_KEY = "YOUR_ETHERSCAN_API_KEY"

   Set wallet address:
   WALLET_ADDRESS = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"

## USAGE

1. Run script:
   python crypto_risk_flagger.py

2. Output: Flagged transactions saved to flagged_transactions.csv.
   Columns: timestamp, hash, recipient, value_eth, value_usd, reason
   
## NOTES

- CoinGecko API: No key needed for ETH-to-USD conversion.
- Security: Don’t commit ETHERSCAN_API_KEY. Use .gitignore.
- Customize: Adjust USD_THRESHOLD or TIME_WINDOW in script.

## TROUBLESHOOTING

- Invalid API Key: Check key at etherscan.io.
- No Transactions: Verify wallet has activity.
- Module Errors: Ensure libraries are installed in active environment.




   


   
