from bs4 import BeautifulSoup
import urllib
import urllib.request
import re


def scrap_product(url):

    price_tag = None
    website = None

    if len(url) < 5:
        return None

    if url.find('www.amazon') > 0:
        website = 'AMAZON'
    elif url.find('www.flipkart') > 0:
        website = 'FLIPKART'
    else:
        return None

    try:
        with urllib.request.urlopen(url) as response:
            html = response.read()
    except:
        return None

    soup = BeautifulSoup(html, 'lxml')

    if website == 'AMAZON':
        price_tag = soup.find_all(id="priceblock_ourprice")
        if price_tag.__len__()==0:
            price_tag = soup.find_all(id="displayedPrice")
    elif website == 'FLIPKART':
        price_tag = soup.find_all("div", {"class": "_30jeq3 _16Jk6d"})
    price_text = price_tag[0].get_text()
    price_str = re.sub('([^0-9.])+', '', price_text)
    price = float(price_str)

    title_tag = soup.find_all('title')
    title = title_tag[0].get_text()

    return price, title
