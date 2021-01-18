import requests
from bs4 import BeautifulSoup
from time import sleep
import csv
from urllib.request import Request, urlopen
from fake_useragent import UserAgent
import random
from lxml import html
 
 
#USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


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
        

    #print(type(result))

    '''try:
        results = scrape_atingi('https://atingi.litmoseu.com/admin/people/425078/edit')
        for result in results:
            print(result)
    except Exception as e:
        print(e)


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
     wr.writerow(data)'''