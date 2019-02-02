from bs4 import BeautifulSoup
import argparse
import requests
import json
import pickle

parser = argparse.ArgumentParser()

parser.add_argument('-v',action='store_true', default=False, help='Debug/verbose mode')
parser.add_argument('-c',action='store_true', default=False, help='Cache images offline in a pickle object')
parser.add_argument('-s',dest='search_string', default=None, help='Search string to query')
parser.add_argument('-d',dest='download_location',default='./', help='Image download location')
parser.add_argument('-p',dest='pickle_location', default=None, help='Pickle object location')
args = parser.parse_args()
if args.v:
	print(args)

if args.pickle_location==None:
	url = 'https://www.google.com/search?tbm=isch&q='
	if args.search_string==None:
		args.search_string = input("Enter a search query : ")
	search_string=args.search_string.replace(' ', '+')
	search_url = url + search_string
	if args.v:
		print(f"The search url is : {search_url}")

	downloadurls = []

	response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15'})

	text_soup = BeautifulSoup(response.content, "html.parser")
	allimages = text_soup.find_all('div', {'class':'rg_meta'})

	for i in allimages:
		downloadurls.append(json.loads(i.text)['ou'])
	print(f'Obtained {len(downloadurls)} image urls')

	if args.c:
		fname = search_string.replace('+','_')
		print(f"caching query to file: {fname}...")
		fp = open(fname,'wb')
		pickle.dump(downloadurls, fp)
		fp.close()
else:
	fp = open(args.pickle_location,'rb')
	links = pickle.load(fp)
	if args.v:
		print(links)