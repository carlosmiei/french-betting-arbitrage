from session_manager import get_session

cookies = {
    "SESSION": "8427b79ead3927f2510c3e4b15c29e82",
    "referral_values": "%7B%22type%22%3A%22reflinkid%22%2C%22val%22%3A%22924212_43A6372F07884BC4A956123625AC8C87%22%2C%22additional%22%3A%7B%22name_tag%22%3A%22btag%22%2C%22ref_partner_id%22%3Anull%2C%22bw_%22%3Anull%7D%7D",
    "is_rtl": "1",
    "reflinkid": "924212_43A6372F07884BC4A956123625AC8C87",
    "lng": "en",
    "flaglng": "en",
    "auid": "XvGEBGT4hf+e/1FSAyP0Ag==",
    "tzo": "1",
    "_glhf": "1695496402",
    "fast_coupon": "true",
    "v3fr": "1",
    "coefview": "0",
    "typeBetNames": "full",
    "ggru": "181",
    "sh.session": "085f2c5d-f690-4b4e-beec-a933e3016e8c",
}

headers = {
    "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Brave";v="116"',
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Is-srv": "false",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://melbet.com/en/line/football/118587-uefa-champions-league",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua-platform": '"macOS"',
}


def get_data(tournment_id):
    params = {
        "sports": "1",
        "champs": tournment_id,
        "count": "100",
        "lng": "en",
        "mode": "4",
        "country": "23",
        "partner": "8",
        "getEmpty": "true",
        "gr": "62",
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
    url = "https://melbet.com/service-api/LineFeed/Get1x2_VZip"
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
