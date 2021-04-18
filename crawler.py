import requests
import time
import sys
import threading

def min_price_crawler(id):

    url = f"https://www.novaragnarok.com/data/cache/ajax/item_{id}.json?_=1618685957220"

    content = requests.get(url)

    data = content.json()

    list_prices = []

    for item in data["data"]:
        price = int(item["orders"]["price"])
        list_prices.append(price)

    if list_prices != []:
        return id, min(list_prices)
    else:
        return id, "Item not announced yet"


if __name__ == '__main__':
    args = sys.argv[1:]
    threads = []
    for i in args:
        x = threading.Thread(target=min_price_crawler, args=(i,))
        x.start()
        threads.append(x)
    
    for thread in threads:
        thread.join()
        