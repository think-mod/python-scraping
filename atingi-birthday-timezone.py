import requests
from bs4 import BeautifulSoup
from time import sleep
import csv
from urllib.request import Request, urlopen
from fake_useragent import UserAgent
import random
from lxml import html
 

def fetch_results(search_url):
    assert isinstance(search_url, str), 'Search term must be a string'  

    atingi_url = search_url
    response = requests.get(atingi_url)
    response.raise_for_status()
    return response.text
 

def parse_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    found_results = []
    table_results = soup.find_all('table', attrs={'role': 'presentation'})
    #print(table_results)
    for table in table_results:

        tabledata = table.find_all('td')
        
        if tabledata:
            for data in tabledata:
                #text = data.renderContents()
                #print(text)
                #trimmed_text = text.strip()
                text = data.text.strip()
                found_results.append(text)
    return found_results


def scrape_atingi(search_url):
    try:
        html = fetch_results(search_url)
        #print(html)
        results = parse_results(html)
        return results
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Atingi")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")





if __name__ == '__main__':

    session_requests = requests.session()

    login_url = "https://atingi.litmoseu.com/account/Login"
    result = session_requests.get(login_url)

    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='__RequestVerificationToken']/@value")))[0]

    payload = {
        "username": "f.sudermann@think-modular.com", 
        "password": "jw^F_fvuQ4%)Ezhu", 
        "__RequestVerificationToken": authenticity_token
    }  

    result = session_requests.post(
	    login_url, 
        data = payload, 
        headers = dict(referer=login_url)
    )

    with open('atingi_profile_links_2.csv', newline='') as profile_links:
        profile_reader = csv.reader(profile_links, delimiter=' ', quotechar='|')
        for index, row in enumerate(profile_reader):
            url = row[0].lstrip('ï»¿')
            result = session_requests.get(
                url, 
                headers = dict(referer = url)
            )

            ## here is where I reference the old methods, login works correctly

            profile = parse_results(result.content)

            with open('atingi_profiles.csv', 'a', newline='') as csvfile:
                #print(profile)
                data = []
                for index, item in enumerate(profile):
                    if item == "Username":
                        #print(item)
                        #print(profile[index+1])
                        #username = profile[index+1].strip('Most people use an email address as their username')
                        #username = username.rstrip('\r')
                        #print(profile[index+1])
                        #print(username)
                        data.append(profile[index+1])
                    elif item == "Time zone":
                        data.append(profile[index+1])
                    elif item == "Date de Naissance | Date of Birth":
                        data.append(profile[index+1])

                print(data)
                wr = csv.writer(csvfile)
                wr.writerow(data)