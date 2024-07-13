#This program implements Regular Expressions, BeautifulSoup4, and the Urllib libraries
#The script scrapes the canada computers website for CPU sales, updating daily.
#SSL is used so that HTTPS websites can be parsed

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re
import ssl
import time
from datetime import date
#The site contains SSL (HTTPS), so these lines are necessary
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#Declaring the link to CPUs, which is used to retrieve the HTML document using URLlib and BS4
cpuPageOne = "https://www.canadacomputers.com/index.php?cPath=4"
pageOneHTML = urllib.request.urlopen(cpuPageOne, context = ctx).read()
soup = BeautifulSoup(pageOneHTML, 'html.parser')
#identifies a "product", which in the case of the retrieved HTML, is the <div> for one product panel
products = soup.find_all('div', class_ = 'px-0 col-12 productInfoSearch pt-2')
#iterates through products for identification and printing
def searchDeals():
    for product in products:
        if len(product.find_all("strong")) > 1:
            #The reason why I checked for the length of this command is that the only items encased in the "strong"
            #HTML tag were those including prices. If there was more than one price, a deal was available, therefore
            #products with deals should contain more than one strong tag.
            productLink = product.find('a').get('href', None)
            productName = product.find("a").text
            if productName.split()[1] == 'Ryzen':
                productName = re.findall( '(^.*) .*[0-8]-', productName)[0]
            else:
                productName = re.findall('(^.*) D', productName)[0]
            prices =  product.find_all("strong")
            originalPrice = prices[0].text
            salePrice = prices[1].text
            saleString = f"The {productName} is on sale now! It is usually {originalPrice}, but is now {salePrice}. \n Buy it now at: {productLink}\n"
            print(saleString)
#Runs the above function every 24 hours, updating with new deals.
if __name__ == '__main__':
    while True:
        currentDate = date.today()
        print(f"Deals found on {currentDate}:")
        searchDeals()
        time.sleep(60 * 60 * 24)
#All pages should in theory be formatted the same throughout the site, so this code should work with any other
#product page across the site by simply replacing the link & updating the RegEx search pattern. Can also easily be 
#configured to update at shorter intervals (by changing time.sleep argument), or be run with multiple pages and deals at once.