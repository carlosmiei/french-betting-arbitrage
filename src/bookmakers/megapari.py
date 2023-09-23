from session_manager import get_session

cookies = {
    "platform_type": "desktop",
    "SESSION": "b8b87980d3015ad40f247232d7324b80",
    "lng": "es",
    "_cfvwab": "-1",
    "cookies_agree_type": "3",
    "tzo": "-6",
    "is12h": "0",
    "auid": "U5PMxWUO9qpx/53ZAww3Ag==",
    "che_g": "7395fe65-fafe-1aa9-5239-0927bbee008c",
    "_glhf": "1695497248",
    "ggru": "167",
    "window_width": "940",
}

headers = {
    "authority": "megapari.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-GB,en;q=0.8",
    # 'cookie': 'platform_type=desktop; SESSION=b8b87980d3015ad40f247232d7324b80; lng=es; _cfvwab=-1; cookies_agree_type=3; tzo=-6; is12h=0; auid=U5PMxWUO9qpx/53ZAww3Ag==; che_g=7395fe65-fafe-1aa9-5239-0927bbee008c; _glhf=1695497248; ggru=167; window_width=940',
    "is-srv": "false",
    "referer": "https://megapari.com/es",
    "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Brave";v="116"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}


def get_data(tournment_id):
    params = {
        "sports": "1",
        "champs": tournment_id,
        "count": "100",
        "lng": "es",
        "mode": "4",
        "country": "23",
        "partner": "192",
        "getEmpty": "true",
        "gr": "824",
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
    url = "https://megapari.com/service-api/LineFeed/Get1x2_VZip"
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
