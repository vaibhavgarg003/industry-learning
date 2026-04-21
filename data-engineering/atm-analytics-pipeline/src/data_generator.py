import random
from datetime import datetime, timedelta

def generate_atm_transactions(num_records = 10000):

    atms = ["ATM001", "ATM002", "ATM003", "ATM004", "ATM005", "ATM006", "ATM007", "ATM008", "ATM009", "ATM010"]

    cities = {
        "ATM001": "Hyderabad", "ATM002": "Bangalore", "ATM003": "Kolkata", "ATM004": "Pune", "ATM005": "Mumbai",
        "ATM006": "Chennai", "ATM007": "Delhi", "ATM008": "Kochi", "ATM009": "Goa", "ATM010": "Jaipur"
    }

    transaction_types = ["Withdrawal", "Deposit", "Balance Inquiry", "Fund Transfer"
    ]

    statuses = ["Success", "Failed", "Pending","Timed Out"]

    status_weights = [0.85, 0.10, 0.03, 0.02]

    start_date = datetime(2024, 1, 1)
    records = []

    for i in range(1, num_records + 1):
        atm_id = random.choice(atms)
        city = cities[atm_id]
        transaction_type = random.choice(transaction_types)
        amount = round(random.uniform(10, 1000), 2) if transaction_type in ["Withdrawal", "Deposit", "Fund Transfer"] else 0.00
        status = random.choices(statuses, weights=status_weights, k=1)[0]
        timestamp = start_date + timedelta(minutes=random.randint(0, 60*24*30))  # Random timestamp within a month

        record = {
            "TransactionID": f"TXN{i:05d}",
            "ATMID": atm_id,
            "City": city,
            "TransactionType": transaction_type,
            "Amount": amount,
            "Status": status,
            "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        records.append(record)
    return records

def get_columns():
    return ["TransactionID", "ATMID", "City", "TransactionType", "Amount", "Status", "Timestamp"]