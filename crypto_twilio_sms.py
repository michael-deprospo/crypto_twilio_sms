#Michael DeProspo
#Silly text notifier for a few cryptocurrencies using coinmarketcap and twilio apis.
import os
from yahoo_fin import stock_info as si
from twilio.rest import Client
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

symbols = ','.join(('BTC','ETH','NANO','XLM','DOGE'))
symbol_list = symbols.split(',')

print(symbols)
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
  'symbol':symbols
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '00fba422-51e9-4930-86d6-e55922a887e9',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params = parameters)
  data = json.loads(response.text)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
prices = {}
#print(data)
for symbol in symbol_list:
  name = data['data'][symbol]['name']
  price = data['data'][symbol]['quote']['USD']['price']
  prices[symbol] = price

msg = "You've subscribed to Mike's Kooky Coin Pricing. \n"
for symbol in prices:
  msg+= symbol + " is currently $" + str(round(prices[symbol],2)) + ". "
print(msg)

account_sid = "ACa8341886e11b06d5a17a028fe6430eac"
auth_token = "8e0f046ea68540357040c1538c1c01f0"
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     #body="Can't bench two plates lolololololololololololololol",
                     body = msg,
                     from_= '+13126971798',
                     to = '#xxxxxxxxxxx'
                 )

print(message.sid)
