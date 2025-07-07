import os
import requests

class TelegramNotifier:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        if not (self.token and self.chat_id):
            raise ValueError('Telegram creds required')

    def send_due_reminder(self, due_date: str, days_before: int):
        text = f"Bill due on {due_date} (in {days_before} days)."
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        resp = requests.post(url, json={'chat_id': self.chat_id, 'text': text}, timeout=10)
        resp.raise_for_status()
        return resp.json()
