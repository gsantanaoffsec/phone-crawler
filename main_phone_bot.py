import re

import threading

import requests

from bs4 import BeautifulSoup

DOMAIN = 'https://django-anuncios.solyd.com.br'
URL_AUT = 'https://django-anuncios.solyd.com.br/automoveis/'

LINKS = []

PHONES = []


def web_request(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print('Request error!')
    except Exception as error:
        print('Request error!')
        print(error)


def parsing(response_html):
    try:
        soup = BeautifulSoup(response_html, 'html.parser')
        return soup
    except Exception as error:
        print('Parsing error')
        print(error)


def find_links(soup):
    try:
        cards_main = soup.find('div', class_='ui three doubling link cards')
        cards = cards_main.find_all('a')
    except Exception as error:
        print('Error finding links')
        print(error)
        return None

    links = []

    for card in cards:
        try:
            link = card['href']
            links.append(link)
        except Exception as error:
            print(error)
            pass

    return links


def find_phones(soup):
    try:
        description = soup.find_all('div', class_='sixteen wide column')[2].p.get_text().strip()
    except Exception as error:
        print('Error finding description!')
        print(error)
        return None

    regex = re.findall(r"\(?0?([1-9]{2})[ \-.)]{0,2}(9[ \-.]?\d{4})[ \-.]?(\d{4})", description)
    if regex:
        return regex


def discover_phones():
    while True:
        try:
            # Remove the first link from the list
            ad_link = LINKS.pop(0)
        except IndexError:
            return None
        ad_response = web_request(DOMAIN + ad_link)
        if ad_response:
            ad_soup = parsing(ad_response)
            if ad_soup:
                phones = find_phones(ad_soup)
                if phones:
                    for telephone in phones:
                        print(f'Phone found: {telephone}')
                        PHONES.append(telephone)
                        save_phones(telephone)


def save_phones(telephone):
    telephone_str = f'{telephone[0]}{telephone[1]}{telephone[2]}\n'
    try:
        with open('telephones.csv', 'a') as file:
            file.write(str(telephone_str))
    except Exception as error:
        print('Error saving file!')
        print(error)


# Indicates the start of the program
if __name__ == '__main__':
    search_response = web_request(URL_AUT)
    if search_response:
        soup_search = parsing(search_response)
        if soup_search:
            LINKS = find_links(soup_search)

        THREADS = []

        for i in range(10):
            thread = threading.Thread(target=discover_phones())
            THREADS.append(thread)

        for thread in THREADS:
            thread.start()

        for thread in THREADS:
            thread.join()
