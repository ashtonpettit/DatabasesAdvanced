import requests
from bs4 import BeautifulSoup as bs
import collections
import json
import time
import os

class Crypto:

    def GetCryptoInfo(self):
        url = "https://www.blockchain.com/btc/unconfirmed-transactions"
        r = requests.get(url)
        soup = bs(r.text, features="html.parser")
        return soup

    def FormatString(self, coins_unformatted):
        coins = list(dict.fromkeys(coins_unformatted))
        text = [x.get_text().replace("Time", ' ').replace("Amount", '').replace("Hash", '').replace("(USD)$", '-').replace(",", '') for x in coins]
        return text

    def SearchSoup(self):
        soup = self.GetCryptoInfo()
        coin = "sc-1g6z4xm-0 hXyplo"
        time_end = time.time() + 60
        searchCoins = soup.find_all("div", {"class" : coin })
        while time.time() < time_end: 
            soup = self.GetCryptoInfo() 
            nextSearch = soup.find_all("div", {"class" : coin }) 
            searchCoins.extend(nextSearch)
        return searchCoins

    def ArrayToDict(self, coins):
        dictionary = {}
        for coin in coins:
            text = coin.split("-")
            dictionary[float(text[1])] = text[0]
            text.clear()
        ordered = collections.OrderedDict(sorted(dictionary.items()))
        res = collections.OrderedDict(reversed(list(ordered.items())))
        topTen = list(res.items())[:10]
        return topTen

    def WriteToFile(self, lines):
        if os.path.exists("coins.txt"):
            method = 'a'
        else:
            method = 'w'
        textfile = open('coins.txt', method)
        for element in lines:
            textfile.write(json.dumps(element) + "\n")
        textfile.close()
    
    def FullFunction(self):
        coins = self.SearchSoup()
        formatted = self.FormatString(coins)
        dict = self.ArrayToDict(formatted)
        self.WriteToFile(dict)


loop = True
while (loop == True):
    crypto = Crypto()
    crypto.FullFunction()