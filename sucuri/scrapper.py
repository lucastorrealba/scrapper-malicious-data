import random
from time import sleep

import selenium.webdriver.remote.webelement
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
import bs4


def scrap_website(fqdn):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    url = f'https://sitecheck.sucuri.net/results/{fqdn}'
    driver.get(url)
    delay = 1
    element = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'results')))

    if element is None or element.text == '':
        return {}
    print(element)
    print("ASDASDASDA")
    # print(element.text)
    summary_dict = dict()
    tag = element.find_element(By.CLASS_NAME, 'active').text
    soup = bs4.BeautifulSoup(element.text, 'lxml')
    soup = soup.text
    soup = soup.split('\n')
    blocklist_list = list()
    is_malware = 'Warning: Malware Detected' in soup
    for s in soup:
        if "Domain blacklisted by" in s:
            block = s.split(':')[0].strip()
            block = block[block.index('by') + 3:]
            blocklist_list.append(block)
    # blocklist = "".join([block_name + '-' for block_name in blocklist])
    # if blocklist != '':
    #     blocklist = blocklist[:-1]
    summary_dict['tag'] = tag  # {Minimal, Low, Medium, High, Critical} Security Risk
    summary_dict['blocklist'] = blocklist_list
    summary_dict['is_malware'] = is_malware
    driver.quit()
    return summary_dict


def main():
    for fqdn in ['google.com', 'hgbzlu.xyz', 'facebook.com']:
        print(scrap_website(fqdn))

if __name__ == '__main__':
    main()
