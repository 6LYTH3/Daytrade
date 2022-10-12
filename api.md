# set info

    # https://www.set.or.th/api/set/index/SET/info

    # investor
    # https://www.set.or.th/api/set/market/SET/investor-type

    # IPO
    # https://www.set.or.th/api/set/ipo/upcoming?limit=6&lang=th

    # https://www.set.or.th/th/listing/ipo/ipo-statistics

    # STOCK List
    # https://www.set.or.th/api/set/stock/list

    r = requests.get("https://www.set.or.th/api/set/ranking/mostActiveVolume/set/S?count=10")
    r = requests.get("https://www.set.or.th/api/set/ranking/mostActiveVolume/mai/S?count=10")
    r = requests.get("https://www.set.or.th/api/set/ranking/topGainer/set/S?count=10")
    # r = requests.get("https://www.set.or.th/api/set/ranking/topGainer/mai/S?count=10")
