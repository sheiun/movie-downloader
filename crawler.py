import os
import re

import requests
from bs4 import BeautifulSoup

targetURL = 'http://www.eyny.com/forum-205-1.html'


def pattern_mega_google(text):
    patterns = [
        'mega', 'mg', 'mu', 'ＭＥＧＡ', 'ＭＥ', 'ＭＵ',
        'ｍｅ', 'ｍｕ', 'ｍｅｇａ', 'GD', 'MG', 'google', 'GE'
    ]

    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True


def crawl(keyword=None, page=10):
    if keyword is None:
        print('Start parsing eyny movie....')
        rs = requests.session()
        res = rs.get(targetURL, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        page_url, page_link_all = [], []

        page_url.append(targetURL)
        page_link_all = soup.select('.pg')[0].find_all('a')

        if page > len(page_link_all):
            page = len(page_link_all)
        for index in range(1, len(page_link_all)):
            page_url.append('http://www.eyny.com/' +
                            page_link_all[index]['href'])

        content = list()
        total_page = len(page_url)
        count = 0

        for url in page_url:
            res = rs.get(url, verify=False)
            soup = BeautifulSoup(res.text, 'html.parser')
            for title_url in soup.select('.bm_c tbody .xst'):
                if pattern_mega_google(title_url.text):
                    name_write = title_url.text
                    url_write = 'http://www.eyny.com/{}'.format(
                        title_url['href'])
                    content.append((name_write, url_write))
            count += 1
            print('Crawler: {:.2%}'.format(count / total_page))

        return content
    else:
        from selenium import webdriver
        # Check System Platform
        # headless
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        # driver
        driver = webdriver.Chrome(
            'chromedriver_win.exe', chrome_options=option)
        driver.get(targetURL)
        driver.find_element_by_id('scbar_txt').send_keys(keyword)
        driver.find_element_by_id('scbar_btn').submit()

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        page_url, page_link_all = [], []

        page_url.append(driver.current_url)
        try:
            page_link_all = soup.select('.pg')[0].find_all('a')
        except:
            page_link_all = []

        if page > len(page_link_all):
            page = len(page_link_all)
        for index in range(1, len(page_link_all)):
            page_url.append('http://www.eyny.com/' +
                            page_link_all[index]['href'])

        content = list()
        total_page = len(page_url)
        count = 0

        for url in page_url:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            for title_url in soup.select('tbody .xst'):
                if pattern_mega_google(title_url.text):
                    name_write = title_url.text
                    url_write = 'http://www.eyny.com/{}'.format(
                        title_url['href'])
                    content.append((name_write, url_write))
            count += 1
            print('Crawler: {:.2%}'.format(count / total_page))

    return content
