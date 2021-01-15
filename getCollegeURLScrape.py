'''
import requests
import pandas as pd
import csv
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

with open('collegenames.csv', newline='') as csvfile:
    collegenames = list(csv.reader(csvfile))




for x in range(1,1132):
	url = 'https://www.google.com/search?q=' + collegenames + " baseball" 
	html = requests.get(url).content
	df_list = pd.read_html(html)
	df = df_list[-1]
	df.to_csv('europlayers.csv', mode='a', header=False)
	print("Done with " + str(x))

	

from requests_html import HTMLSession
import csv
import pandas as pd

with open('collegenames.csv', newline='') as csvfile:
    collegenames = list(csv.reader(csvfile))

for x in range(1,1132):
	query = "baseball ".join(collegenames[x])
	url = 'https://www.google.com/search?q=' + query
	session = HTMLSession()
	r = session.get(url)
	searchbox = r.html.find('.search', first=True)
	programURL = searchbox.find('a', first=True)
	with open('collegeURLS.csv') as fd:
		fd.write(programURL)



import requests
import pandas as pd


for x in range(1,4):
	url = 'http://www.hsbaseballweb.com/d'+str(x)+'_addresses.htm' 
	html = requests.get(url).content
	df_list = pd.read_html(html)
	df = df_list[3]
	df.to_csv('collegeURLS.csv', mode='a', header=False)
	print("Done with " + str(x))
	'''

import pandas as pd
from bs4 import BeautifulSoup
import requests
import urllib.request
import numpy as np




for x in range(1,4):
	url = 'http://www.hsbaseballweb.com/d'+str(x)+'_addresses.htm'
      

	html=urllib.request.urlopen(url)

	bs = BeautifulSoup(html,'lxml')

	table = bs.select('center')
	website_links = []
	for a in bs.find_all('a', href=True):
		website_links.append(a['href'])
	
	df1 = pd.DataFrame(website_links)
	df1.to_csv('collegeURLS.csv', mode='a', header=False)
	print('Copied page '+str(x))

	'''
	df1 = pd.DataFrame(website_links)
	dfs = pd.read_html(str(table),encoding='utf-8', header=0)

	dfs = dfs[4]

	dfs.append(df1)
	dfs.to_csv('collegeURLS.csv', mode='a', header=False)
	print('done with page'+str(x)) 
	'''
