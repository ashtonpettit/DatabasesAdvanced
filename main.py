import requests
import pymongo
from bs4 import BeautifulSoup as bs
import collections
import time
import redis



class Crypto:

    def __init__(self):
        self.url = "https://www.blockchain.com/btc/unconfirmed-transactions"
        self.coin = "sc-1g6z4xm-0 hXyplo"
        self.conn = redis.Redis(host='redis', port=6379, db=0)

    def GetCryptoInfo(self):
        r = requests.get(self.url)
        soup = bs(r.text, features="html.parser")
        return soup

    def SearchSoup(self):
        soup = self.GetCryptoInfo()
        time_end = time.time() + 60   
        while time.time() < time_end:
            searchCoins = soup.find_all("div", {"class" : self.coin }) 
            self.CacheCoins(searchCoins)
            searchCoins.clear()
            soup = self.GetCryptoInfo()
        self.GetTopTen()

    def CacheCoins(self, coins):
        text = [x.get_text().replace("Time", ' ').replace("Amount", '')
            .replace("Hash", '').replace("(USD)$", '-')
            .replace(" BTC", '').replace(",", '').replace("(BTC)", '') for x in coins]
        for strings in text:
            item = strings.split('-')
            self.conn.hset("Crypto", item[1], item[0])

    def GetTopTen(self):
        coins_cache = self.conn.hgetall("Crypto")
        dictionary = {}
        dict.clear(dictionary)
        for key, value in coins_cache.items():
            dictionary[float(key)] = value
        ordered = collections.OrderedDict(sorted(dictionary.items()))
        res = collections.OrderedDict(reversed(list(ordered.items())))
        topTen = list(res.items())[:10]
        dictlist = dict(topTen)
        top10Dictionary = {str(key): str(value) for key, value in dictlist.items()}
        all_keys = list(self.conn.hgetall('Crypto').keys())
        self.conn.hdel('Crypto', *all_keys)
        self.CreateCoinWallet(top10Dictionary)

    def CreateCoinWallet(self, top10):
        crypto_wallet = {}
        dict.clear(crypto_wallet)
        for key, value in top10.items():
            coin = Coin()
            coin.SetCoin(key, value)
            crypto_wallet[coin.hash] = {
                "Time" : coin.time,
                "Amount(USD)" : coin.usd,
                "Amount(BTC)" : coin.btc
            }
        self.SendToMongo(crypto_wallet)

    def SendToMongo(self, wallet):
        client = pymongo.MongoClient('mongo:27017')
        mydb = client["DatabasesAdvanced"]
        myCollection = mydb["Crypto"]
        key = list(wallet.keys())[0]
        value = list(wallet.values())[0]
        first_pair = {key : value}
        myCollection.insert_one(first_pair)


class Coin:

    def __init__(self):
        self.hash = ""
        self.time = ""
        self.btc = ""
        self.usd = ""

    def SetCoin(self, key, value):
        coin = value.split()
        self.hash = coin[0]
        self.time = coin[1]
        self.btc = coin[2]
        self.usd = key




loop = True
while (loop == True):
    crypto = Crypto()
    crypto.SearchSoup() 

