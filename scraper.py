from bs4 import BeautifulSoup
import argparse, requests, json, pickle, os,sys, urllib.parse

class downloader:
	
	def __init__(self, search_term, verbose_mode):
		self.search_term = search_term
		self.verbose_mode = verbose_mode
		self.downloadurls = []
	
	def get_urls(self, cache=True):
		if self.search_term is None:
			print("The search term is empty. If you have a cache pickle file, use the -p argument")
			return
		url = 'https://www.google.com/search?tbm=isch&q='
		search_string=self.search_term.replace(' ', '+')
		search_url = url + urllib.parse.quote(search_string, safe='').replace('-','%2D')

		response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15'})

		text_soup = BeautifulSoup(response.content, "html.parser")
		allimages = text_soup.find_all('div', {'class':'rg_meta'})

		for i in allimages:
			self.downloadurls.append(json.loads(i.text)['ou'])
		
		if self.verbose_mode:
			print(f"The search url is : {search_url}")
			print(f'Obtained {len(self.downloadurls)} image urls')
		
		
		if cache:
			if not os.path.exists('./caches/'):
				os.mkdir('caches')
			fname = './caches/' + search_string.replace('+','_') + '.cache'
			print(f"caching query to file: {fname}...")
			fp = open(fname,'wb')
			pickle.dump(self.downloadurls, fp)
			fp.close()

	def printprogress(self, number):
		bar_len = 60
		filled_len = int(round(bar_len * number / float(len(self.downloadurls))))
		percents = round(100.0 * number / float(len(self.downloadurls)), 1)
		bar = '=' * filled_len + '-' * (bar_len - filled_len)
		sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', "Downloading"))
		sys.stdout.flush()

	def download(self, download_location='./'):

		if len(self.downloadurls) == 0:
			print("The list of urls is empty. Either call get_urls() or load data from cache file.")
			exit(-1)
		# To choose the file names for the images
		if self.search_term is not None:
			filefoldername=self.search_term.replace(' ', '_')
		else:
			# Since the search term is empty, we need to get the cache file name and use that as the individual image name
			filefoldername=self.pickle_location.split('/')[-1].split('.')[0]
		
		final_path = download_location + 'downloads/'+filefoldername
		# Check if the download folder exists
		if not os.path.exists(download_location +'downloads'):
			os.mkdir(download_location +'downloads')

		# Check if the search_term folder in the download folder exists
		if not os.path.exists(final_path):
			os.mkdir(final_path)
		
		# Now since we have the links, create the file names and download it to downloads/<query>/<img name> folder
		count=0
		for url,no in zip(self.downloadurls,range(0,len(self.downloadurls))):
			file_name = filefoldername + str(count) + '.' + url.split('.')[-1].split("?")[0].split("&")[0].split("/")[0]
			# Print progress
			self.printprogress(no)
			# Download the URLs
			response = requests.get(url)
			if response.ok:
				with open(final_path+'/'+file_name, 'wb') as imagefile:
					imagefile.write(response.content)
			count+=1
			pass

	def load_from_cache(self, p):
		if p is None:
			print("No cache location specified. Please try again")
			exit(-1)
		self.pickle_location = p
		fp = open(p,'rb')
		self.downloadurls = pickle.load(fp)
		if self.verbose_mode:
			print(self.downloadurls)

if __name__ == '__main__':
	# Parse command line arguments

	parser = argparse.ArgumentParser(description="Google Image Dataset Scraper")
	parser.add_argument('-v',action='store_true', default=False, help='Debug/verbose mode')
	parser.add_argument('-c',action='store_true', default=False, help='Cache images offline in a pickle object')
	parser.add_argument('-s',dest='search_string', default=None, help='Search string to query')
	parser.add_argument('-d',dest='download_location',default='./', help='Image download location')
	parser.add_argument('-p',dest='pickle_location', default=None, help='Pickle object location')
	args = parser.parse_args()


	x = downloader(args.search_string, verbose_mode=args.v)
	if args.search_string is not None:
		x.get_urls(cache=args.c)
	elif args.pickle_location is not None:
		x.load_from_cache(args.pickle_location)
	x.download(download_location=args.download_location)