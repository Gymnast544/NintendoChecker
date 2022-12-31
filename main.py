import requests
from bs4 import BeautifulSoup
import threading
import time
import os
from keep_alive import keep_alive

keep_alive()


import discord
from discord import Webhook, RequestsWebhookAdapter, File


mainhook1 = os.environ['mainhook1']

mainhook2 = os.environ['mainhook2']
webhook = Webhook.partial(mainhook1, mainhook2,\
 adapter=RequestsWebhookAdapter())

webhook.send("Hello world")

timebetweenchecks = 1

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
}
page = requests.get("https://store.nintendo.com/nintendo-3ds-2ds.html?product_list_dir=desc&product_list_limit=36&product_list_order=price", headers=HEADERS)
print("Gotten content")

#print(page.content)
f = open("sample.txt", "w")
f.write(str(page.content))
f.close()


def checkURL(URL):
    global s
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/67.0.3396.87 Safari/537.36',}
    page = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    productparts = soup.find_all("span", class_="product-item-link")
    print(productparts[0])
    print(len(productparts))
    products = []
    for productspan in productparts:
      products.append(str(productspan).split(">")[1].replace("</span", "").strip())
    print(products)
    return products
    

class amdproduct:
    def __init__(self, url):
        self.url = url
        self.products = checkURL(url)

    def checkChanges(self):
        try:
            newproducts = checkURL(self.url)
        except:
            newproducts = self.products
        if len(newproducts) != len(self.products):
            self.products = newproducts
            print("we have a change my friend")
            webhook.send("@everyone change detected at Nintendo store. \Products: "+str(self.products)+"\n"+self.url)


def startproduct(url):
  product = amdproduct(url)
  while True:
    product.checkChanges()
    time.sleep(timebetweenchecks)
products = []
f = open("URLs.txt", "r")
for line in f:
  currenturl = str(line.strip())
  print(currenturl)
  threading.Thread(target=startproduct, args =(currenturl,)).start()
  #products.append(bbproduct(line.strip()))
  #print(line.strip())


while True:
  t = time.localtime()
  current_time = time.strftime("%H:%M:%S", t)
  print("still running", current_time)
  webhook.send("Bot still running, time is "+str(current_time))
  time.sleep(10)