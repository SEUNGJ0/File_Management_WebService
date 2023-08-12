import os, json
from django.core.exceptions import ImproperlyConfigured
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(keyword, secrets=secrets):
    try:
        return secrets[keyword]
    except KeyError:
        return None
        # error_msg = "Set the {} environment variable".format(keyword)
        # raise ImproperlyConfigured(error_msg)
    
def input_secret(keyword, value ,secrets=secrets):
    new_data = {keyword:value}
    secrets.update(new_data)
    with open('secrets.json', 'w') as file:
        json.dump(secrets, file, indent=4)