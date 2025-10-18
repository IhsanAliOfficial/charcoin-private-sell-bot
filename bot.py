import os
import json
import time
import random
import logging
from dotenv import load_dotenv

# -------------------------------
# Setup Logging
# -------------------------------
if not os.path.exists("logs"):
    os.makedirs("logs")
logging.basicConfig(
    filename="logs/charbot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "DUMMY_KEY")
RPC_URL = os.getenv("RPC_URL", "https://api.mainnet-beta.solana.com")
JUPITER_API = os.getenv("JUPITER_API", "https://quote-api.jup.ag/v6/quote")

# -------------------------------
# Bot settings
# -------------------------------
PRICE_CHECK_INTERVAL = 15   # seconds
FRACTIONS_PER_STAGE = 5     # for demo
TEST_MODE = True            # <---- Prevents real transactions

# -------------------------------
# Dummy Investors File
# -------------------------------
if not os.path.exists("investors.json"):
    dummy_investors = [
        {
            "wallet": "DemoWallet12345",
            "total_tokens": 10000,
            "staking_percentage": 0.3,
            "stages": [
                {"stage_number": 1, "target_price_usd": 0.2, "percentage_to_sell": 0.25, "completed": False},
                {"stage_number": 2, "target_price_usd": 0.3, "percentage_to_sell": 0.25, "completed": False},
                {"stage_number": 3, "target_price_usd": 0.5, "percentage_to_sell": 0.5, "completed": False},
            ]
        }
    ]
    with open("investors.json", "w") as f:
        json.dump(dummy_investors, f, indent=2)

with open("investors.json") as f:
    investors = json.load(f)


# -------------------------------
# Dummy CHAR price simulator
# -------------------------------
def get_char_price():
    base_price = 0.18
    # Randomly fluctuate for demo
    fluctuation = random.uniform(-0.02, 0.05)
    simulated_price = round(base_price + fluctuation, 4)
    logging.info(f"Simulated CHAR price: ${simulated_price}")
    return simulated_price


# -------------------------------
# Dummy Jupiter Swap Executor
# -------------------------------
def execute_jupiter_swap(wallet, amount):
    if TEST_MODE:
        logging.info(f"🧪 Simulating swap for {wallet} of {amount:.2f} CHAR")
        print(f"🧪 Simulated swap executed for {wallet}: {amount:.2f} CHAR")
    else:
        # Real Jupiter swap logic goes here
        pass


# -------------------------------
# Core Investor Processor
# -------------------------------
def process_investor(inv):
    total = inv["total_tokens"]
    staked = total * inv["staking_percentage"]
    available = total - staked

    for stage in inv["stages"]:
        if stage.get("completed"):
            continue

        current_price = get_char_price()
        target_price = stage["target_price_usd"]

        print(f"🔍 Checking {inv['wallet']} — Current: ${current_price} | Target: ${target_price}")

        if current_price >= target_price:
            to_sell = available * stage["percentage_to_sell"]
            fraction = to_sell / FRACTIONS_PER_STAGE

            logging.info(f"Target hit for {inv['wallet']}! Selling {to_sell} CHAR in {FRACTIONS_PER_STAGE} parts.")
            print(f"💰 Target hit! Simulating sale of {to_sell} CHAR...")

            for i in range(FRACTIONS_PER_STAGE):
                execute_jupiter_swap(inv['wallet'], fraction)
                time.sleep(1)

            stage["completed"] = True
            with open("investors.json", "w") as wf:
                json.dump(investors, wf, indent=2)
            print(f"✅ Stage {stage['stage_number']} completed for {inv['wallet']}")
            break


# -------------------------------
# Main Bot Loop
# -------------------------------
def main():
    print("🚀 CHAR Auto-Sell Dummy Bot Started (Test Mode)")
    logging.info("Bot started in TEST MODE.")
    while True:
        for investor in investors:
            process_investor(investor)
        print(f"⏳ Waiting {PRICE_CHECK_INTERVAL}s before next check...\n")
        time.sleep(PRICE_CHECK_INTERVAL)


if __name__ == "__main__":
    main()
