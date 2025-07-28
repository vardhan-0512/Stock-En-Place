import pandas as pd
import requests
import sys
import os 
from yahooquery import search
# print("Current Working Directory:", os.getcwd())

if __name__ == "__main__":
    sys.stdin = open("input.txt", "r")
    sys.stdout = open("Output.txt", "w")
    sys.stderr = open("Error.txt", "w")

def tickers_sp500():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = requests.get(url).text
    df = pd.read_html(html, header=0)[0]
    tickers = df['Symbol'].tolist()
    return tickers

def fetch_sp500_list():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = requests.get(url).text
    df = pd.read_html(html, header=0)[0]
    return df['Security']


def find_ticker(ticker):
    result = search(ticker)
    if result and 'quotes' in result and len(result['quotes']) > 0:
        return result['quotes'][0]['symbol']
    return None
names=fetch_sp500_list()
print(len(names))
#print(names)
for stock in names:
    ticker = find_ticker(stock)
    if ticker:
        print(ticker)
    else:
        print(f"Ticker not found for {stock}")

