import os, json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def save_secrets(secrets):
    with open(secret_file, 'w') as f:
        json.dump(secrets, f, indent=4)

def get_secret(keyword, secrets=secrets):
    try:
        return secrets[keyword]
    except KeyError:
        return None

def input_secret(keyword, value, secrets=secrets):
    new_data = {keyword: value}
    secrets.update(new_data)
    save_secrets(secrets)


def delete_secret(keyword):
    try:
        del secrets[keyword]
        save_secrets(secrets)
        print(f"Deleted secret for keyword: {keyword}")
    except KeyError:
        return None

