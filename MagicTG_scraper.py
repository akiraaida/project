import urllib.request
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
from http.client import IncompleteRead
import time
import json

def check_internet(url):
    try:
        header = {"pragma" : "no-cache"}
        req = Request(url, headers=header)
        response = urlopen(req)
        return True, response
    except urllib.error.URLError as err:
        return False, ''
    except IncompleteRead:
        check_internet(url)

def reFetchTable(page, relativeLink):
	try:
		while True: 
			conn, html = check_internet("http://www.facetofacegames.com/" + str(relativeLink) + "?page=" + str(page) + "&sort_by_price=0")
			print ("%r" % (conn))
			try:
				if conn is True:
					#pass the HTML to Beautifulsoup.
					soup = BeautifulSoup(html,'html.parser')
					#get the HTML of the table called site Table where all the links are displayed
					main_table = soup.find("table",class_='invisible-table products_table')
					print (main_table)
					print ('End of the Page:', page)
					filename = str(relativeLink)[9:str(relativeLink).rfind("/")] + ".txt"
					with open(filename, 'a+', encoding='UTF-8') as file:
						file.write(str(main_table))
					break
				else:
					#need to make it wait and re-do the while.
					time.sleep(30)
			except urllib.error.URLError as err:
				#need to wait
				time.sleep(20)

	except IncompleteRead:
		# Oh well, reconnect and keep trucking
		reFetchTable(page, relativeLink)
		
def fetchPriceTable(relativeLink): 		
	for i in range(1,500):
		try:
			while True: 
				conn, html = check_internet("http://www.facetofacegames.com" + str(relativeLink) + "?page={}&sort_by_price=0".format(i))
				print ("%r" % (conn))
				try:
					if conn is True:
						#pass the HTML to Beautifulsoup.
						soup = BeautifulSoup(html,'html.parser')
						#get the HTML of the table called site Table where all the links are displayed
						main_table = soup.find("table",class_='invisible-table products_table')
						if main_table is None:
							return
						print (main_table)
						print ('End of the Page:', i)
						filename = str(relativeLink)[9:str(relativeLink).rfind("/")] + ".txt"
						with open(filename, 'a+', encoding='UTF-8') as file:
							file.write(str(main_table))
						break
					else:
						#need to make it wait and re-do the while.
						time.sleep(30)
				except urllib.error.URLError as err:
					#need to wait
					time.sleep(20)		
		
		except IncompleteRead:
			# Oh well, reconnect and keep trucking
			reFetchTable(i, relativeLink)
			continue
		
mainPageUrl = "http://www.facetofacegames.com/"
#download the URL and extract all the magic single sub categories to the variable html 
mainPagehtml = urlopen(mainPageUrl)
#pass the HTML to Beautifulsoup.
mainPageSoup = BeautifulSoup(mainPagehtml,'html.parser')
#get the HTML of the table called site Table where all the links are displayed
category_table = mainPageSoup.find("ul",{"id":"category_tree"})		
subcategory_table = category_table.find("a", {"id":"category_8"}).parent
#links array will contain every single page's url that I am going to get price table for
links = subcategory_table.find_all("a",class_="leaf_category")
for link in links:
	print(link['href'])
	fetchPriceTable(link['href'])

		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
#Now we go into main_table and get every a element in it which has a class "title" 
#links = main_table.find_all("a",class_="name")

#from each link extract the text of link and the link itself
#List to store a dict of the data we extracted 
#extracted_records = []
#for link in links: 
#    title = link.textT
#    url = link['href']
#    record = {
#       'title':title,
#        'url':url
#        }
#    extracted_records.append(record)
#print(extracted_records)