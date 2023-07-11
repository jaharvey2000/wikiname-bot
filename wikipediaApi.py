from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

API_USER_AGENT = os.getenv('USER_AGENT')
WIKIPEDIA_ENDPOINT = os.getenv('WIKIPEDIA_ENDPOINT')

# Check if variable exists
if (API_USER_AGENT == None or WIKIPEDIA_ENDPOINT == None):
    print('USER_AGENT or WIKIPEDIA_ENDPOINT environment variable not set')
    exit(1)

def random_page():
    headers = {
        'User-Agent': API_USER_AGENT,
        'Accept': 'application/problem+json'
    }

    res = requests.get(WIKIPEDIA_ENDPOINT, headers=headers)

    if (res.status_code == 200):
        return {
            'title': res.json()['titles']['normalized'],
            'extract': res.json()['extract'],
            'link': res.json()['content_urls']['desktop']['page']
        }
    else:
        return res.json()
