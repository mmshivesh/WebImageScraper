from bs4 import BeautifulSoup
from pprint import pprint
import requests
import json
import pickle

url = 'https://www.google.com/search?tbm=isch&q='
search_string = input("Enter a search term : ")
search_string=search_string.replace(' ', '+')
search_url = url + search_string
print(f"The search url is : {search_url}")

downloadurls = []

response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15'})#, headers={'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0"})

text_soup = BeautifulSoup(response.content, "html.parser")
allimages = text_soup.find_all('div', {'class':'rg_meta'})

for i in allimages:
	downloadurls.append(json.loads(i.text)['ou'])

print("pickling query to file...")
fname = search_string.replace('+','_')
fp = open(f'{fname}','wb')
pickle.dump(downloadurls, fname)
fp.close()