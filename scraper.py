from bs4 import BeautifulSoup
from pprint import pprint
import requests

url = 'https://www.google.com/search?tbm=isch&q='
search_string = input("Enter a search term : ")
search_string=search_string.replace(' ', '+')

search_url = url + search_string

response = requests.get(search_url)

text_soup = BeautifulSoup(response.content, features="html.parser")
pprint(text_soup)