import requests
import pandas as pd
from tabulate import tabulate
import json
from datetime import datetime, timedelta
import sys

STOCKLIST = {}

with open('stock_list.json', 'r', encoding='utf-8') as f:
    STOCKLIST = json.loads(f.read())

def correlations(company):
    """ input :str: company symbol
        output: list of correlation
    """
    cor = {}
    with open("correlation.json", "r", encoding='utf-8') as f:
        cor = json.loads(f.read())

    sectors = cor['sector'].keys()
    for s in sectors:
        sector = cor['sector'][s]
        for c in sector:
            if company in c:
                return " ".join(c)

    return ""

def getSectors(company):
    """ input :str: company symbol
        output: list of correlation
    """
    cor = {}
    with open("sectors.json", "r", encoding='utf-8') as f:
        cor = json.loads(f.read())

    sectors = cor['sector']
    for s in sectors:
        symbol = s[-1].split(" ")
        if company in symbol:
            return s[2].strip()

    return ""

def show(data):
    print(tabulate(data, headers='keys', tablefmt='grid'))

def format(data):
    stocks = []
    for d in data:
        stock = dict((k, d[k]) for k in ['symbol', 'sign', 'last', 'percentChange', 'totalVolume'] if k in d)
        for s in STOCKLIST['securitySymbols']:
            if d['symbol'] == s['symbol']:
                stock['industry'] = s['industry']
                stock['sector'] = s['sector']
        stock['percentChange'] = round(stock['percentChange'], 2)
        stock['totalVolume'] = round(float(stock['totalVolume']/1000000),2)
        stock['cors'] = correlations(d['symbol'])
        stock['detail'] = getSectors(d['symbol'])
        stocks.append(stock)

    return stocks

def save(data, date_select, market_type):
    if date_select == 0:
        now = datetime.now().strftime("%Y-%m-%d")
        data.to_csv(f"marketlog/{now}-{market_type}.csv")

def load(date_select, market_type):
    dateSelect = datetime.now() - timedelta(days=date_select)
    now = dateSelect.strftime("%Y-%m-%d")
    
    data = pd.read_csv(f"marketlog/{now}-{market_type}.csv")
    return data

def main():
    now = datetime.now().strftime("%Y-%m-%d")

    date_select = 0
    try:
        date_select = int(sys.argv[1])
    except Exception as e:
        pass

    if date_select > 0:
        setMostVol = load(date_select, 'set_most_vol')
        maiMostVol = load(date_select, 'mai_most_vol')
        setTopGainer = load(date_select, 'set_top_gainer')
        maiTopGainer = load(date_select, 'mai_top_gainer')

    else:
        setMostVol = getMostActive('set')
        maiMostVol = getMostActive('mai')
        setTopGainer = getTopGainer('set')
        maiTopGainer = getTopGainer('mai')

    set_most_vol_df = pd.DataFrame(format(setMostVol['stocks']))
    mai_most_vol_df = pd.DataFrame(format(maiMostVol['stocks']))
    set_top_gainer_df = pd.DataFrame(format(setTopGainer['stocks']))
    mai_top_gainer_df = pd.DataFrame(format(maiTopGainer['stocks']))

    if not set_most_vol_df.empty: 
        save(set_most_vol_df, date_select, 'set_most_vol')
        print('SET Most Volume ------------------------------------------------------------------')
        print(set_most_vol_df.sort_values('sector'))
        print()
    if not mai_most_vol_df.empty: 
        save(mai_most_vol_df, date_select, 'mai_most_vol')
        print('MAI Most Volume ------------------------------------------------------------------')
        print(mai_most_vol_df.sort_values('sector'))
        print()
    if not set_top_gainer_df.empty: 
        save(set_top_gainer_df, date_select, 'set_top_gainer')
        print('SET Top Gainer -------------------------------------------------------------------')
        print(set_top_gainer_df.sort_values('sector'))
        print()
    if not mai_top_gainer_df.empty: 
        save(mai_top_gainer_df, date_select, 'mai_top_gainer')
        print('MAI Top Gainer ------------------------------------------------------------------')
        print(mai_top_gainer_df.sort_values('sector'))

def getMostActive(market):
    r = requests.get(f"https://www.set.or.th/api/set/ranking/mostActiveVolume/{market}/S?count=10")
    if r.ok:
        return r.json()

def getTopGainer(market):
    r = requests.get(f"https://www.set.or.th/api/set/ranking/topGainer/{market}/S?count=10")
    if r.ok:
        return r.json()

if '__main__' == __name__:
    main()