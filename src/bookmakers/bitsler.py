from session_manager import get_session

headers = {
    "authority": "sports.bitsler.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-GB,en;q=0.8",
    "content-type": "application/json",
    "origin": "https://www.bitsler.com",
    "referer": "https://www.bitsler.com/",
    "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "sec-gpc": "1",
    "socketiokey": "-ow2GGhIJnoyehMGA0H6",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}


def get_data(id):
    json_data = {
        "id": "sr:tournament:" + str(id),
        "page": 1,
        "perPage": 200,
        "notoken": True,
    }

    return json_data


# response = requests.post(
#     "https://betslipapi.isppro.net/api/Guest/GetNewLines",
#     headers=headers,
#     json=json_data,
# )

competition_urls = {
    "football": {
        "bundesliga": 35,
        "ligue1": 24,
        "liga": 8,
        "premier-league": 17,
        "serie-a": 23,
        "primeira": 238,
        "mls": 242,
        "serie-a-brasil": 325,
        "arabia": 19238,
        "copa-argentina": 1024,
        "champions": 7,
        "chile": 27665,
        "euro": 27,
        "colombia": 27072,
        "czech": 172,
        "ireland": 192,
        "belarus": 169,
        "russia": 203,
        "scotland": 36,
        "uruguai": 278,
        # "bundesliga-austria": "",
        # "division-1a": "",
    },
    "american-football": {"nfl": 31},
    "basketball": {
        # "nba": 3,
        # "euroleague": "https://www.betclic.fr/basket-ball-s4/euroligue-c14",
    },
    "tennis": {
        # "us-open-men": get_url(3027),
    },
}


async def get_page(competition):
    url = "https://sports.bitsler.com/api/getMatchesByTournament"
    if (
        competition["sport"] in competition_urls
        and competition["competition"] in competition_urls[competition["sport"]]
    ):
        id = competition_urls[competition["sport"]][competition["competition"]]
        body = get_data(id)
    else:
        return None
    async with get_session().post(
        url,
        data=body,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        },
    ) as response:
        response = await response.json()
    return response


def american_to_decimal(american_odds):
    if str(american_odds)[0] == "-" or str(american_odds)[0] == "+":
        american_odds = float(american_odds)
        if american_odds > 0:
            return round(american_odds / 100 + 1, 2)
        else:
            return round(100 / abs(american_odds) + 1, 2)
    return float(american_odds)


async def get_games(competition):
    response = await get_page(competition)
    if response is None:
        return None
    result = response["payload"]
    games = []
    for el in result:
        first = None
        second = None
        third = None
        team1 = el["home"]["name"]
        team2 = el["away"]["name"]
        markets = el["defaultMarkets"]
        for market in markets:
            if market is None:
                continue
            if market["name"] == "1x2" or market["name"] == "Winner (incl. overtime)":
                outcomes = market["outcomes"]
                for outcome in outcomes:
                    if outcome["id"].startswith("1") or outcome["id"].startswith("4"):
                        first = round(float(outcome["odds"]), 2)
                    elif outcome["id"].startswith("2"):
                        second = round(float(outcome["odds"]), 2)
                    elif outcome["id"].startswith("3") or outcome["id"].startswith("5"):
                        third = round(float(outcome["odds"]), 2)

        if len(outcomes) == 2:  # nfl
            if first and third:
                odds = [float(first), float(third)]
                games.append({"team1": team1, "team2": team2, "odds": odds})
        else:
            if first and second and third:
                odds = [float(first), float(second), float(third)]
                games.append({"team1": team1, "team2": team2, "odds": odds})
    return games
