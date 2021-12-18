import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

# r = requests.get('https://api.github.com', auth=('user', 'pass'))

# print (r.status_code)
# print (r.headers['content-type'])
url = 'https://maktabkhooneh.org'

try:
    response = requests.get(url)
    html = BeautifulSoup(response.text, 'html.parser')

    # If the response was successful, no Exception will be raised
    print(response.text)
    response.raise_for_status()
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')  # Python 3.6
except Exception as err:
    print(f'Other error occurred: {err}')  # Python 3.6
else:
    print('Success!')