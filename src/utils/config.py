import os
from dataclasses import dataclass

@dataclass
class Settings:
    CAPI_KEY: str = os.getenv('CAPI_KEY','')
    NOTION_TOKEN: str = os.getenv('NOTION_TOKEN','')
    NOTION_DB_ID: str = os.getenv('NOTION_DB_ID','')
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY','')
    DUE_REMINDER_DAYS: int = int(os.getenv('DUE_REMINDER_DAYS','3'))
    CSV_PATH: str = os.getenv('CSV_PATH','data/transactions.csv')
    NORDIGEN_ID: str = os.getenv('NORDIGEN_ID','')
    NORDIGEN_SECRET: str = os.getenv('NORDIGEN_SECRET','')
    NORDIGEN_ACCOUNT_IDS: str = os.getenv('NORDIGEN_ACCOUNT_IDS','')
    OFX_URL: str = os.getenv('OFX_URL','')
    OFX_ORG: str = os.getenv('OFX_ORG','')
    OFX_FID: str = os.getenv('OFX_FID','')
    OFX_USER: str = os.getenv('OFX_USER','')
    OFX_PASS: str = os.getenv('OFX_PASS','')
    OFX_ACCT_ID: str = os.getenv('OFX_ACCT_ID','')
    OFX_ACCT_TYPE: str = os.getenv('OFX_ACCT_TYPE','')

settings = Settings()
