import requests
from bs4 import BeautifulSoup
from time import sleep
import csv
from urllib.request import Request, urlopen
from fake_useragent import UserAgent
import random
 
 
USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


    

# Retrieve a random index proxy (we need the index to delete it if not working)
def random_proxy():
  return random.randint(0, len(proxies) - 1)

def fetch_results(search_term, number_results, language_code):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')
    
    

    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    response = requests.get(google_url, headers=USER_AGENT)
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
            sleep(5)
    print('Collected Urls, now writing to csv')
    with open('masterCollegeUrls.csv', 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(data)


