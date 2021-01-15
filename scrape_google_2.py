import requests
from bs4 import BeautifulSoup
from time import sleep
import csv
from urllib.request import Request, urlopen
from fake_useragent import UserAgent
import random
from lxml.html import fromstring
from itertools import cycle
import traceback
import numpy as np
 
def get_random_ua():
    random_ua = ''
    ua_file = 'ua_file.txt'
    try:
        with open(ua_file) as f:
            lines = f.readlines()
        if len(lines) > 0:
            prng = np.random.RandomState()
            index = prng.permutation(len(lines) - 1)
            idx = np.asarray(index, dtype=np.integer)[0]
            random_proxy = lines[int(idx)]
    except Exception as ex:
        print('Exception in random_ua')
        print(str(ex))
    finally:
        return random_ua

user_agent = get_random_ua()
headers = {'user-agent': user_agent,}

'''def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies'''

    



def fetch_results(search_term, number_results, language_code):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')
    
    

    bing_url = 'https://www.bing.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)

    '''proxies = {
    "http": 'http://162.248.247.153', 
    "https": 'http://162.248.247.153'
    }'''
    response = requests.get(bing_url, headers=headers)

    response.raise_for_status()
    return search_term, response.text
 

def parse_results(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')

    found_results = []
    result_block = soup.find_all('div', attrs={'class': 'g'})
    for result in result_block:

        link = result.find('a', href=True)
        
        if link:
            link = link['href']
            if link != '#':
                found_results.append(link)
    return found_results


def scrape_google(search_term, number_results, language_code):
    try:
        keyword, html = fetch_results(search_term, number_results, language_code)
        results = parse_results(html, keyword)
        return results
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Google")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")





if __name__ == '__main__':

    with open('4yrs&2yrs.csv', newline='') as csvfile:
        collegeNames = list(csv.reader(csvfile))
    suffix = ' baseball'
    collegeNamesFinal = [str(s) + suffix for s in collegeNames]
    data = []
    for keyword in collegeNamesFinal:
        try:
            results = scrape_google(keyword, 1, "en")
            for result in results:
                data.append(result)
                print(result)
        except Exception as e:
            print(e)
        finally:
            sleep(12)
    print('Collected Urls, now writing to csv')
    with open('masterCollegeUrls.csv', 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(data)


