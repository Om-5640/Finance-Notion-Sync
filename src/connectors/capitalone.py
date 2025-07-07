import os
import requests
from connectors.base import Connector

class CapitalOneConnector(Connector):
    BASE_URL = 'https://api.capitalone.com/transactions'

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('CAPI_KEY')
        if not self.api_key:
            raise ValueError('Capital One API key is required')

    def fetch_transactions(self, since_timestamp: str) -> list:
        resp = requests.get(
            self.BASE_URL,
            headers={'Authorization': f'Bearer {self.api_key}'},
            params={'since': since_timestamp},
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json().get('transactions', [])
        return [
            {
                'id': t['id'],
                'date': t['transactionDate'],
                'vendor': t['merchantName'],
                'amount': t['amount'],
                'category': t.get('category') or 'Uncategorized',
                'card_last4': t.get('card',{}).get('last4','')
            }
            for t in data
        ]
