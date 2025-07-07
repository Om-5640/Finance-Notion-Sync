import os
import requests

class NotionClient:
    API_URL = 'https://api.notion.com/v1/pages'
    VERSION = '2022-06-28'

    def __init__(self, token: str = None, database_id: str = None):
        self.token = token or os.getenv('NOTION_TOKEN')
        self.db = database_id or os.getenv('NOTION_DB_ID')
        if not (self.token and self.db):
            raise ValueError('Notion token & DB ID required')
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Notion-Version': self.VERSION,
            'Content-Type': 'application/json'
        }

    def upsert_transaction(self, txn: dict) -> dict:
        payload = {
            'parent': {'database_id': self.db},
            'properties': {
                'Date': {'date': {'start': txn['date']}},
                'Vendor': {'title': [{'text': {'content': txn['vendor']}}]},
                'Amount': {'number': txn['amount']},
                'Category': {'select': {'name': txn['category']}},
                'Card Last4': {'rich_text': [{'text': {'content': txn['card_last4']}}]}
            }
        }
        resp = requests.post(self.API_URL, headers=self.headers, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()

