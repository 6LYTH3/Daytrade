# Company and Share holder correlation

import sys
import json
import requests

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
            return f"{s[2]}\n{s[3]}"

    return ""

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

def cashBalance(stat):
    """ SET value > 100M
        MAI value > 80M
        PE > 40
        %CHG > 15%
        """

    lastPrice = stat['close']
    priceCash = round(lastPrice * 1.15, 2)

    # NO P/E
    if not stat['pe']:
        return f"จะติดที่ราคา {priceCash} (15%)"

    if stat['pe'] <= 35:
        return "N/A"
    elif stat['pe'] > 35 and stat['pe'] <= 40:
        return f"มีโอกาสติด Cash Balance ที่ราคา {priceCash}"
    else:
        return f"จะติดที่ราคา {priceCash} (15%)"

def showCorrelations(company):
    cors = correlations(company)
    if cors: 
        print(f'Correlations: {cors}')

def showSectors(company):
    sector = getSectors(company)
    if sector: 
        print(sector)


def main():
    company = sys.argv[1].upper()
    profile = companyProfile(company)
    if not profile: 
        # print(f"{company} not found")
        showCorrelations(company)
        print()
        showSectors(company)
        sys.exit()

    stat = trandingStat(company)

    marketCap = int(stat['marketCap']/1000000)

    # print out
    print()
    print(company)
    print(profile['name'])
    print(profile['market'], profile['industry'], profile['sector'])
    print(profile['businessType'])
    print()
    print(f"MargetCap: {marketCap:,}M")
    print(f"%ff: {profile['freeFloat']}")
    print(f"PE: {stat['pe']}")
    print(f"Last Volume: {stat['totalVolume']:,}")
    print(f"Cash Balance: {cashBalance(stat)}")
    print()

    showCorrelations(company) 
    print() 
    showSectors(company)
    print()

if __name__ == '__main__':
    main()