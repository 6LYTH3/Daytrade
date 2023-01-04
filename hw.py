# Company and Share holder correlation

import sys
import json
import requests
import pandas as pd

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

def companyInfo(company):
    info = {"name": "", "market": "", "sector": "", "industry": "", "cor": ""}
    for s in STOCKLIST["securitySymbols"]:
        if s['symbol'] == company:
            info = {
               "name": company, 
               "market": s["market"], 
               "industry": s["industry"], 
               "sector": s["sector"],
               "cor": correlations(company)
            }
            break

    if info['name'] == '':
        return companyProfile(company)

    return info


def companyProfile(company):
    r = requests.get(f"https://www.set.or.th/api/set/factsheet/{company}/profile?lang=th")
    if r.status_code == 404:
        return None

    p = json.loads(r.content)
    if not p:
        return {"name": "", "market": "", "sector": "", "industry": "", "cor": ""}

    return {
        "name": p["name"], 
        "market": p["market"], 
        "industry": p["industry"], 
        "sector": p["sector"], 
        "cor": correlations(company)
        }

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
            # return f"{s[2]}\n{s[3]}"
            return f"{s[2]}"

    return ""

def showCorrelations(company):
    cors = correlations(company)
    if cors: 
        print(f'Correlations: {cors}')

def showSectors(company):
    sector = getSectors(company)
    if sector: 
        print(sector)

def getHomeWork():
    buffer = []
    with open("homework.txt", "r") as f:
        for l in f.readlines():
            tmp = l.strip()
            if tmp != '':
                tmp = tmp.split()[0]
                buffer.append(tmp.upper())

    return buffer

def main():
    hw = getHomeWork()

    companies = []

    for c in hw:
        firm = companyInfo(c)
        companies.append(
                {'name': c, 
                'market': firm['market'], 
                'sector': firm['sector'], 
                'industry': firm['industry'],
                'cor': firm['cor'],
                'biz': getSectors(c)
                })

    df = pd.DataFrame(companies)
    df = df.sort_values(['sector']).reset_index(drop=True)
    print(df)

    # find section 

if __name__ == '__main__':
    main()
