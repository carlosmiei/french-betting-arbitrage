from session_manager import get_session

cookies = {
    "platform_type": "desktop",
    "lng": "en",
    "SESSION": "dc480a0d1fb7bb7e3c3da7f86149b3c4",
    "_cfvwab": "-1",
    "cookies_agree_type": "3",
    "tzo": "-6",
    "is12h": "0",
    "auid": "LY0LEmUNw6uLoMOtBl1dAg==",
    "che_g": "f221fc88-5508-e5c2-149e-1be2072bd6b7",
    "sh.session": "7d71467c-31fa-4ffd-af9e-20c181637d0e",
    "_glhf": "1695418938",
    "ggru": "188",
    "window_width": "798",
}

headers = {
    "authority": "platform.20bet.life",
    "accept": "application/json",
    "accept-language": "en-GB,en;q=0.5",
    "client-timezone": "Europe/Lisbon",
    "content-type": "application/json",
    # 'cookie': '_ga=GA1.1.1842126177.1695323861; sid=79273f2015f4bad93c03308cd15eb972; _ga_J9LNZYMXZE=GS1.1.1695370148.2.1.1695396130.0.0.0',
    "origin": "https://20bet.life",
    "referer": "https://20bet.life/",
    "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Brave";v="116"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}


def get_data(tournment_id):
    params = {
        "sports": "1",
        "champs": tournment_id,
        "count": "100",
        "lng": "en",
        "mode": "4",
        "country": "23",
        "partner": "132",
        "getEmpty": "true",
        "virtualSports": "true",
        "gr": "395",
    }

    return params


competition_urls = {
    "football": {
        "bundesliga": 96463,
        "ligue1": 12821,
        "liga": 127733,
        "premier-league": 88637,
        "serie-a": 110163,
        "primeira": 118663,
        "mls": 828065,
        "champions": 118587,
        "uefa": 118593,
        "eredivise": 2018750,
        "copa-argentina": 2151274,
        # "chile":,
        "serie-a-brasil": 1268397,
        # "arabia":,
        # "bundesliga-austria": ,
        "division-1a": 28787,
        "super-lig": 11113,
        "poland": 27731,
        # "czech":,
        # "colombia": ,
        "russia": 225733,
        "arabia": 16819,
    },
    "basketball": {
        # "nba": 3,
        # "euroleague": "https://www.betclic.fr/basket-ball-s4/euroligue-c14",
    },
    "tennis": {
        # "us-open-men": get_url(3027),
    },
}


async def get_page(competition):
    url = "https://br.1x001.com/service-api/LineFeed/Get1x2_VZip"
    if (
        competition["sport"] in competition_urls
        and competition["competition"] in competition_urls[competition["sport"]]
    ):
        id = competition_urls[competition["sport"]][competition["competition"]]
        params = get_data(id)
    else:
        return None
    async with get_session().get(
        url,
        headers=headers,
        params=params,
    ) as response:
        response = await response.json()
    return response


async def get_games(competition):
    response = await get_page(competition)
    if response is None:
        return None
    result = response["Value"]
    games = []
    for el in result:
        first = None
        second = None
        third = None
        team1 = el["O1"]
        if team1 == "Home":
            continue
        team2 = el["O2"]
        odds = el["E"]
        for odd in odds:
            if odd["T"] == 1:
                first = odd["C"]
            elif odd["T"] == 2:
                second = odd["C"]
            elif odd["T"] == 3:
                third = odd["C"]

        if competition["competition"] == "nfl":
            if first and third:
                odds = [float(first), float(third)]
                games.append({"team1": team1, "team2": team2, "odds": odds})
        else:
            if first and second and third:
                odds = [float(first), float(second), float(third)]
                games.append({"team1": team1, "team2": team2, "odds": odds})
    return games
