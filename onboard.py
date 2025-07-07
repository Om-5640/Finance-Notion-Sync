import os
import sys
import json
import requests
from base64 import b64encode
from getpass import getpass

# Dependencies: pip install PyYAML requests

# Constants
API_URL = 'https://api.github.com'
REPO = os.getenv('GITHUB_REPOSITORY')  # e.g. 'your-org/finance-notion-sync-free'
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # with repo 'secrets' scope

if not REPO or not GITHUB_TOKEN:
    print('Error: Set GITHUB_REPOSITORY (owner/repo) and GITHUB_TOKEN env vars.')
    sys.exit(1)

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

# 1. Get public key for repo secrets
r = requests.get(f'{API_URL}/repos/{REPO}/actions/secrets/public-key', headers=headers)
r.raise_for_status()
pubkey = r.json()
key_id = pubkey['key_id']
key = pubkey['key']

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

# Convert GitHub public key (base64) to RSA key
pk = serialization.load_der_public_key(b64decode(key))

def encrypt_secret(secret_value):
    """Encrypt a secret using GitHub's public key."""
    ciphertext = pk.encrypt(
        secret_value.encode(),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return b64encode(ciphertext).decode()

# 2. Prompt user for each secret
secrets = {}
questions = [
    ('NOTION_TOKEN', 'Notion Integration Token'),
    ('NOTION_DB_ID', 'Notion Database ID'),
    ('TELEGRAM_TOKEN', 'Telegram Bot Token'),
    ('TELEGRAM_CHAT_ID', 'Telegram Chat ID'),
    ('CAPI_KEY', 'Capital One API Key (optional)'),
    ('NORDIGEN_ID', 'Nordigen ID (optional)'),
    ('NORDIGEN_SECRET', 'Nordigen Secret (optional)'),
    ('NORDIGEN_ACCOUNT_IDS', 'Nordigen Account IDs, comma-separated (optional)'),
    ('OFX_URL', 'OFX Server URL (optional)'),
    ('OFX_ORG', 'OFX Organization (optional)'),
    ('OFX_FID', 'OFX Financial Institution ID (optional)'),
    ('OFX_USER', 'OFX Username (optional)'),
    ('OFX_PASS', 'OFX Password (optional)'),
    ('OFX_ACCT_ID', 'OFX Account ID (optional)'),
    ('OFX_ACCT_TYPE', 'OFX Account Type (optional)'),
    ('CSV_PATH', 'CSV Path (default data/transactions.csv)'),
    ('OPENAI_API_KEY', 'OpenAI API Key (optional)'),
    ('DUE_REMINDER_DAYS', 'Days before due date to remind (default 3)')
]

print('Enter your credentials (leave blank to skip optional)')
for name, prompt_text in questions:
    if 'PASS' in name or 'SECRET' in name or 'TOKEN' in name or 'KEY' in name:
        val = getpass(f'{prompt_text}: ')
    else:
        val = input(f'{prompt_text}: ')
    if val:
        secrets[name] = val

# 3. Encrypt and upload each secret
for name, val in secrets.items():
    encrypted = encrypt_secret(val)
    payload = {'encrypted_value': encrypted, 'key_id': key_id}
    resp = requests.put(
        f'{API_URL}/repos/{REPO}/actions/secrets/{name}',
        headers=headers,
        json=payload
    )
    if resp.status_code in (201, 204):
        print(f'Set secret: {name}')
    else:
        print(f'Failed to set {name}:', resp.text)

# 4. Initialize state.json
init_ts = (datetime.datetime.utcnow() - datetime.timedelta(days=30)).isoformat() + 'Z'
with open('state.json', 'w') as f:
    json.dump({'last_timestamp': init_ts}, f)
print('Initialized state.json with timestamp:', init_ts)

# 5. Commit state.json
os.system('git add state.json && git commit -m "Add initial state via onboard.py" && git push')

print('Onboarding complete! Your GitHub Actions secrets are configured, and state.json is bootstrapped.')
