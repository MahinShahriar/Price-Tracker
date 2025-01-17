import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import schedule



base_url = "https://www.amazon.com"
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        }
base_response = requests.get(url=base_url, headers=headers)
cookies = base_response.cookies.get_dict()
product_list = ['B0BBWH1R8H','B075NYWF5P','B09ZWCYQTX']

def product_page(product,url):
    product_response = requests.get(url=url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(product_response.text, 'html.parser')
    return soup

price_data = []

def price_tracker():
    for product in product_list:
        url = "https://www.amazon.com/dp/"+product
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        response = False
        while response==False:
            soup = product_page(product,url)
            price =  soup.find_all(name="span", class_="a-price-whole")

            if price:
                price= price[0].text.replace('.', '')
                print(f"URL: {url} , PRICE  : {price}")
                price_data.append({
                    'data_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'product_url': url,
                    'price': price,
                    })
                response = True
            else:
                print(f"Price not found for URL: {url}. Trying again!.")
            time.sleep(4)

        time.sleep(2)
    print(price_data)

schedule.every(2).minutes.do(price_tracker)
while True:
    schedule.run_pending()
    time.sleep(1)

