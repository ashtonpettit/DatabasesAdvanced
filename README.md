# DatabasesAdvanced
## Webscraper by Ashton Pettit

### Crypto()

Crypto calls a method called FullFunction. FullFunction is a method that executes the sub-methods inside of Crypto in the correct order.

First is SearchSoup() which calls the method GetCryptoInfo().
GetCryptoInfo() handles the request and stores it in a BeautifulSoup object.

### SearchSoup()
Then in SearchSoup() the divs containing the crypto information are searched for and stored to a list. 
A while loop runs for 60 seconds where it will continuously refresh the request and collect the divs and extend the list with crypto information.

### FormatString()
Next the list is sent to FormatString() where it is temporarily converted to a dictionary to ensure only unique elements
remain in the list. It's then turned back into a list and each string is formatted by adding spaces and removing unnecessary text. 'Amount' is replaced with a dash '-' character for a future method.

### ArraytoDict()
Once the strings in the list are formatted the list is sent to ArraytoDict() to be stored in a dictionary.
Each element is split by the '-' character, and then swapped so the USD amount is the key and the string containing the hash, BitCoin amount, and time is the value.
This dictionary is sorted and reversed and everything but the top 10 elements are purged.

### WritetoFile()
Finally the dictionary is sent to WritetoFile(). In this method a check is done to see if a file exists already to determine whether a write ('w') or append ('a') method of opening the file is required. Then the dictionary is written to the file.
