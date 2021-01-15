import requests
import pandas as pd


for x in range(1,30):
	url = 'http://europlayers.com/SearchTeam.aspx?FormType=1&PageId=' + str(x) 
	html = requests.get(url).content
	df_list = pd.read_html(html)
	df = df_list[-1]
	df.to_csv('europlayers.csv', mode='a', header=False)
	print("Done with " + str(x))