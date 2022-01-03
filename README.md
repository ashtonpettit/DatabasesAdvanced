# DatabasesAdvanced
## Webscraper by Ashton Pettit

### Crypto()

Crypto initialises with a url for the website to scrape, the HTML class name of the coins to scrape, and the configuration for the redis connection. Within the Crypto class there are several methods to handle the scraping and storage.

### Coin()

This class is the object of the coins scraped from the website. It contains the USD amount, the BTC amount, the date and time, and the hash of the coin.

### GetCryptoInfo()

This method handles the request using the url initialised and stores it in a variable called soup that uses the python package BeautifulSoup.

### SearchSoup()
This calls GetCryptoInfo() to get the scraping information then for 60 seconds it scrapes the site for coins and calls GetCryptoInfo() with each loop. Then it caches the response using the method CacheCoins(). When the 60 seconds are done it calls GetTopTen().

### CacheCoins()
In this method the results of the scrape are stored into redis, first the strings are formated then split so that USD is seperate from the rest of the string. Then its sent to Redis.

### GetTopTen()
After all the coins are cached this method will collect them all from Redis and store them in a dictionary using the USD as the key. Then the dictionary is ordered by USD amount and the only the top 10 are selected. Then the dictionary is sent to CreateCoinWallet(). The Redis cache is cleared.

### CreateCoinWallet()
The dictionary is looped and a coin object is created for each top 10 coin. The hash, USD, BTC, and time are stored in the corresponding properties. Then these Coin objects properties are stored in another dictionary and sent to SendToMongo().

### SendToMongo()
The mongo client is established aswell as the collection to store and the results are sent to the collection.


### Dockerfile
Python 3.8 is pulled in and a mount to /code is created as the working directory. Then the python packages are installed.

### Docker-compose
A Redis image and Mongo image are created and linked with the main volume in /code.
