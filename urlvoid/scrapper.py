from datetime import datetime

import bs4
import requests


from pprint import pprint

def scrap_website(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'lxml')
    summary_dict = dict()
    table_list = soup.find_all('table', 'table table-custom table-striped')
    assert len(table_list) == 2
    [table_1, table_2] = table_list
    # table 1
    tr_list = table_1.find_all('tr')
    for tr in tr_list:
        td_list = tr.find_all('td')
        assert len(td_list) == 2
        dict_key = td_list[0].text
        dict_value = td_list[1].text
        if dict_key in ['Domain Information']:
            continue
        if dict_value != 'Unknown':
            if dict_key in ['Domain Registration', 'IP Address']:
                dict_value = dict_value[:dict_value.index(' ')]
            elif dict_key in ['Last Analysis', 'Latitude\\Longitude']:
                dict_value = dict_value[:dict_value.index('\xa0')].strip()
        summary_dict[dict_key] = dict_value
    # table 2
    scanning_engines_dict = dict()
    tr_list = table_2.tbody.find_all('tr')
    detected_by_list = list()
    for tr in tr_list:
        td_list = tr.find_all('td')
        td_list = [td.text.strip() for td in td_list]
        if td_list[1] != 'Nothing Found':
            detected_by_list.append(td_list[0])
    summary_dict['detected_by'] = detected_by_list
    summary_dict['query_datetime'] = datetime.now()
    return summary_dict


URL = "https://www.urlvoid.com/scan/google.cl/"
URL_PHISHING = 'https://www.urlvoid.com/scan/taplink.cc/'

if __name__ == '__main__':
    print('Google')
    pprint(scrap_website(URL))
    print('taplink.cc')
    pprint(scrap_website(URL_PHISHING))
    print("ok! ")
