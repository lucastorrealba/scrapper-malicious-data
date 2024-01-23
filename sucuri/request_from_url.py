from pprint import pprint

import requests


def request_from_url(fqdn):
    url = f'https://sitecheck.sucuri.net/api/v3/?scan={fqdn}'
    json_website = requests.get(url, headers={'Accept': 'application/json'})
    pprint(json_website.json())


if __name__ == '__main__':
    request_from_url('google.com')
    print("\n\n\n\n\n\n")
    request_from_url('dev-kingdopressword.pantheonsite.io')
