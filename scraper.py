from bs4 import BeautifulSoup
import argparse
import requests
import json
import pickle
import os,sys
import urllib.parse

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

parser = argparse.ArgumentParser(description="Google Image Dataset Scraper")

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
	search_url = url + urllib.parse.quote(search_string, safe='').replace('-','%2D')
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
		if not os.path.exists('./caches/'):
			os.mkdir('caches')
		fname = './caches/' + search_string.replace('+','_') + '.cache'
		print(f"caching query to file: {fname}...")
		fp = open(fname,'wb')
		pickle.dump(downloadurls, fp)
		fp.close()
else:
	fp = open(args.pickle_location,'rb')
	downloadurls = pickle.load(fp)
	if args.v:
		print(downloadurls)

# Now since we have the links, create the file names and download it to downloads/<query>/<img name> folder
