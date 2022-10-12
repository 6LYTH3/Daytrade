import pandas as pd
from tabulate import tabulate
from datetime import datetime
import sys
import json
import requests

column_format = {'DATE':[],'MARKET':[],'SECTOR':[],'STOCK':[],'MCap':[], 'FF':[], 'PE':[]}

logfile_name = datetime.now().strftime('%Y.%m.csv')
def getTradinglog():
    try:
        datalog = pd.read_csv(logfile_name)
    except Exception as e:
        datalog = pd.DataFrame(column_format)
    
    return datalog
    

def show(df):
    print(tabulate(df, showindex=False))

def companyProfile(company):
    r = requests.get(f"https://www.set.or.th/api/set/factsheet/{company}/profile?lang=th")
    if r.status_code == 404:
        return None

    p = json.loads(r.content)
    ff = round(p['freeFloats'][0]['percentFreeFloat'], 2)

    return {
        "name": p["name"], 
        "market": p["market"], 
        "industry": p["industry"], 
        "sector": p["sector"], 
        "businessType": p["businessType"], 
        "freeFloat": ff
        }

def trandingStat(company):
    r = requests.get(f"https://www.set.or.th/api/set/factsheet/{company}/trading-stat?lang=th")
    p = json.loads(r.content)[0]

    return {
        "pe": p['pe'],
        "pbv": p['pbv'],
        "close": p['close'],
        "totalVolume": float(p['totalVolume']),
        "marketCap": float(p['marketCap'])
    }

def main():
    datalog = getTradinglog()

    company = sys.argv[1].upper()
    if not company: 
        show(datalog)
        return
    
    profile = companyProfile(company)
    stat = trandingStat(company)

    column_format = {'DATE':[datetime.now().strftime("%Y-%m-%d")],'MARKET':[profile['industry']],'SECTOR':[profile['sector']],'STOCK':[company],'MCap':[stat['marketCap']], 'FF':[profile['freeFloat']], 'PE':[stat['pe']]}


    print(column_format)
    

if __name__ == '__main__':
    main()