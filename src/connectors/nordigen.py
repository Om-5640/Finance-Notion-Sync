import os
import requests
from connectors.base import Connector

class NordigenConnector(Connector):
    TOKEN_URL = 'https://ob.nordigen.com/api/v2/token/new/'
    ACCOUNTS_URL = 'https://ob.nordigen.com/api/v2/accounts/{id}/transactions/'

    def __init__(self):
        self.id = os.getenv('NORDIGEN_ID')
        self.secret = os.getenv('NORDIGEN_SECRET')
        self.account_ids = os.getenv('NORDIGEN_ACCOUNT_IDS','').split(',')
        if not (self.id and self.secret and self.account_ids):
            raise ValueError('Nordigen credentials & account IDs are required')
        self.token = self._get_token()

    def _get_token(self) -> str:
        resp = requests.post(self.TOKEN_URL, json={ 'secret_id': self.id, 'secret_key': self.secret })
        resp.raise_for_status()
        return resp.json()['access']

    def fetch_transactions(self, since_timestamp: str) -> list:
        since = since_timestamp.split('T')[0] if since_timestamp else None
        txns = []
        headers = {'Authorization': f'Bearer {self.token}'}
        for aid in self.account_ids:
            url = self.ACCOUNTS_URL.format(id=aid)
            params = { 'date_from': since } if since else {}
            resp = requests.get(url, headers=headers, params=params)
            resp.raise_for_status()
            booked = resp.json()['transactions']['booked']
            for t in booked:
                txns.append({
                    'id': t['transactionId'],
                    'date': t['bookingDate'],
                    'vendor': t.get('remittanceInformationUnstructured',''),
                    'amount': float(t['transactionAmount']['amount']),
                    'category': 'Uncategorized',
                    'card_last4': ''
                })
        return txns
