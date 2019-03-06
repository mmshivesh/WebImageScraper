# WebImageScraper

Scrape images from Google Images

## Dependencies:
Requests and BeautifulSoup

## Usage:
Download images (upto 100 currently). To use this, download the scraper.py and run,

`python3 scraper.py`

The arguments supported are:

`-s`	-	(s)earch term.

`-c`	-	Include this flag to (c)ache the search query. The searches are cached using a simple pickle file at the location of `scraper.py` within the subfolder `/caches` with the same filename as the search query and extension `.cache`.

`-p`	-	If you wish to download from a pre-existing cache file, include the (p)ath of the cache file after this argument.

`-d`	-	Choose the location to (d)ownload the files. A `downloads` folder is created at the location and the image files are stored in a subdirectory with the name of the search term. 

`-v`	-	(V)erbose mode to see the intermediate steps

The implementation is in a class. The class `downloader` is initialized with the following:

1. search_term	-	The term to search for
2. verbose_mode	-	Verbose mode status

The Methods provided involve:

1. `get_urls`	-	Takes cache status as a parameter. Obtains the image urls into `downloadurls`.
2. `printprogress`	-	Print the progess of the download. Takes the current `number` of the file being downloaded as a parameter
3. `download` - Downloads the images into the location specified by the `download_location` parameter
4. `load_from_cache`	-	Load the download urls from the cache file into `downloadurls`.

Todo:
- [ ] Auto search the cache first for a cache file. Access Google Images only upon a cache miss
- [ ] Parallelize the downloads in threads
- [ ] Increase downloaded image count per run (currently 100)