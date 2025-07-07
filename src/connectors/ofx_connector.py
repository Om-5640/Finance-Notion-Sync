import os
from datetime import datetime
from ofxclient import OfxClient
from connectors.base import Connector
from ofxparse import OfxParser

class OFXConnector(Connector):
    """
    Fetch transactions via the OFX protocol. User must supply env vars:
    OFX_URL, OFX_ORG, OFX_FID, OFX_USER, OFX_PASS, OFX_ACCT_ID, OFX_ACCT_TYPE
    """
    def __init__(self):
        self.url = os.getenv('OFX_URL')
        self.org = os.getenv('OFX_ORG')
        self.fid = os.getenv('OFX_FID')
        self.user = os.getenv('OFX_USER')
        self.password = os.getenv('OFX_PASS')
        self.acct_id = os.getenv('OFX_ACCT_ID')
        self.acct_type = os.getenv('OFX_ACCT_TYPE')  # CHECKING, SAVINGS, CREDITCARD
        if not all([self.url, self.org, self.fid, self.user, self.password, self.acct_id, self.acct_type]):
            raise ValueError('All OFX env vars are required')
        self.client = OfxClient(self.url, self.org, self.fid)

    def fetch_transactions(self, since_timestamp: str) -> list:
        since = since_timestamp.split('T')[0] if since_timestamp else None
        session = self.client.client()
        response = session.download_statements(
            username=self.user,
            password=self.password,
            acct_id=self.acct_id,
            acct_type=self.acct_type,
            client_uid='uuid',
            date_start=since,
            date_end=datetime.utcnow().date().isoformat()
        )
        ofx = OfxParser.parse(response)
        txns = []
        for stmt in ofx.account.statement.transaction_list:
            txns.append({
                'id': stmt.id,
                'date': stmt.date.strftime('%Y-%m-%d'),
                'vendor': stmt.payee or '',
                'amount': stmt.amount,
                'category': 'Uncategorized',
                'card_last4': ''
            })
        return txns
