import datetime
import logging
from utils.config import settings
from utils.state import StateStore
from connectors.base import Connector
from connectors.csv_connector import CSVConnector
from connectors.capitalone import CapitalOneConnector
from connectors.nordigen import NordigenConnector
from connectors.ofx_connector import OFXConnector
from notion.client import NotionClient
from notifications.telegram_notifier import TelegramNotifier
from analytics.engine import AnalyticsEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    state = StateStore()
    last_ts = state.get_last_timestamp() or (
        (datetime.datetime.utcnow() - datetime.timedelta(days=1)).isoformat()
    )

    # Build connectors dynamically
    connectors: list[Connector] = []
    if settings.CAPI_KEY:
        connectors.append(CapitalOneConnector(settings.CAPI_KEY))
    if settings.NORDIGEN_ID and settings.NORDIGEN_SECRET and settings.NORDIGEN_ACCOUNT_IDS:
        connectors.append(NordigenConnector())
    if settings.OFX_URL:
        connectors.append(OFXConnector())
    connectors.append(CSVConnector(settings.CSV_PATH))

    # Fetch & upsert
    notion = NotionClient(settings.NOTION_TOKEN, settings.NOTION_DB_ID)
    all_txns = []
    for conn in connectors:
        try:
            txns = conn.fetch_transactions(last_ts)
            all_txns.extend(txns)
            for txn in txns:
                notion.upsert_transaction(txn)
        except Exception as e:
            logger.error("%s failed: %s", conn.__class__.__name__, e)

    state.set_last_timestamp(datetime.datetime.utcnow().isoformat())

    if settings.OPENAI_API_KEY:
        report = AnalyticsEngine.summarize(all_txns)
        logger.info("Analytics Report:\n%s", report)

    due = (datetime.date.today() + datetime.timedelta(days=30)).isoformat()
    TelegramNotifier().send_due_reminder(due, settings.DUE_REMINDER_DAYS)

if __name__ == '__main__':
    main()
