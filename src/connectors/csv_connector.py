import csv
from datetime import datetime
from connectors.base import Connector

class CSVConnector(Connector):
    def __init__(self, path: str = 'data/transactions.csv'):
        self.path = path

    def fetch_transactions(self, since_timestamp: str) -> list:
        last = datetime.fromisoformat(since_timestamp) if since_timestamp else None
        txns = []
        with open(self.path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                dt = datetime.fromisoformat(row['date'])
                if not last or dt > last:
                    txns.append({
                        'id': row.get('id') or f"{row['date']}-{row['name']}-{row['amount']}",
                        'date': row['date'],
                        'vendor': row['name'],
                        'amount': float(row['amount']),
                        'category': row.get('category') or 'Uncategorized',
                        'card_last4': row.get('card_last4','')
                    })
        return txns
