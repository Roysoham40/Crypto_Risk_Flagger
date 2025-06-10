import requests
import pandas as pd
from datetime import datetime, timedelta
import time
from dateutil import parser
import os

# Configuration
ETHERSCAN_API_KEY = ""  # Replace with your Etherscan API key
WALLET_ADDRESS = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"  # Replace with target Ethereum wallet
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
ETHERSCAN_API_URL = "https://api.etherscan.io/api"
USD_THRESHOLD = 10000  # Transactions above $10,000 are flagged
TIME_WINDOW = timedelta(hours=1)  # Time window for rapid transfers
OUTPUT_CSV = "flagged_transactions.csv"

def get_eth_usd_price():
    """Fetch current ETH to USD price from CoinGecko API."""
    try:
        response = requests.get(COINGECKO_API_URL)
        response.raise_for_status()
        return response.json()["ethereum"]["usd"]
    except requests.RequestException as e:
        print(f"Error fetching ETH price: {e}")
        return None

def get_transactions(wallet_address):
    """Fetch transactions for a wallet address using Etherscan API."""
    params = {
        "module": "account",
        "action": "txlist",
        "address": wallet_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY
    }
    try:
        response = requests.get(ETHERSCAN_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if data["status"] == "1":
            return data["result"]
        else:
            print(f"Etherscan API error: {data['message']}")
            return []
    except requests.RequestException as e:
        print(f"Error fetching transactions: {e}")
        return []

def convert_wei_to_eth(wei):
    """Convert Wei to ETH."""
    return int(wei) / 1e18

def flag_risky_transactions(transactions, eth_usd_price):
    """Flag transactions based on AML criteria."""
    flagged = []
    transactions = sorted(transactions, key=lambda x: int(x["timeStamp"]))

    for i, tx in enumerate(transactions):
        # Extract transaction details
        value_eth = convert_wei_to_eth(tx["value"])
        value_usd = value_eth * eth_usd_price if eth_usd_price else 0
        timestamp = datetime.fromtimestamp(int(tx["timeStamp"]))
        recipient = tx["to"]
        hash = tx["hash"]

        # Initialize flags
        high_value_flag = False
        rapid_transfer_flag = False
        reason = []

        # Flag high-value transactions
        if value_usd > USD_THRESHOLD:
            high_value_flag = True
            reason.append(f"High value: ${value_usd:,.2f}")

        # Flag rapid transfers (within 1 hour)
        for j in range(i + 1, len(transactions)):
            next_tx = transactions[j]
            next_timestamp = datetime.fromtimestamp(int(next_tx["timeStamp"]))
            if next_timestamp - timestamp <= TIME_WINDOW:
                rapid_transfer_flag = True
                reason.append(f"Rapid transfer within {TIME_WINDOW}")
                break

        # If transaction is flagged, add to results
        if high_value_flag or rapid_transfer_flag:
            flagged.append({
                "timestamp": timestamp,
                "hash": hash,
                "recipient": recipient,
                "value_eth": value_eth,
                "value_usd": value_usd,
                "reason": "; ".join(reason)
            })

    return flagged

def save_to_csv(flagged_transactions):
    """Save flagged transactions to a CSV file."""
    if not flagged_transactions:
        print("No flagged transactions to save.")
        return

    df = pd.DataFrame(flagged_transactions)
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Flagged transactions saved to {OUTPUT_CSV}")

def main():
    # Fetch ETH to USD price
    eth_usd_price = get_eth_usd_price()
    if not eth_usd_price:
        print("Failed to fetch ETH price. Exiting.")
        return

    print(f"Current ETH price: ${eth_usd_price:,.2f}")

    # Fetch transactions
    transactions = get_transactions(WALLET_ADDRESS)
    if not transactions:
        print("No transactions found or error occurred. Exiting.")
        return

    print(f"Fetched {len(transactions)} transactions for wallet {WALLET_ADDRESS}")

    # Flag risky transactions
    flagged_transactions = flag_risky_transactions(transactions, eth_usd_price)
    print(f"Found {len(flagged_transactions)} risky transactions")

    # Save to CSV
    save_to_csv(flagged_transactions)

if __name__ == "__main__":
    main()