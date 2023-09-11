from session_manager import get_session


cookies = {
    "referrer": "www.google.com",
}

headers = {
    "authority": "thunderpick.io",
    "accept": "*/*",
    "accept-language": "en-GB,en;q=0.6",
    "content-type": "application/json",
    # "cookie": "referrer=www.google.com",
    "origin": "https://thunderpick.io",
    "referer": "https://thunderpick.io/en/sports/football/br/s%C3%A9rie-a/2148",
    "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "same-origin",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}


def get_data(id, country, sport):
    game_ids = 10 if sport == "football" else 18
    json_data = {
        "gameIds": [
            game_ids,
        ],
        "competitionId": id,
        "country": country,
    }
    return json_data


# response = requests.post(
#     "https://betslipapi.isppro.net/api/Guest/GetNewLines",
#     headers=headers,
#     json=json_data,
# )

competition_urls = {
    "football": {
        "bundesliga": [268, 276],
        "ligue1": [297, 250],
        "liga": [218, 724],
        "premier-league": [187, 826],
        "serie-a": [295, 380],
        "primeira": [495, 620],
        "mls": [774, 840],
        "serie-a-brasil": [2148, 76],
        "super-lig": [266, 792],
        "division-1a": [2748, 56],
        "eredivise": [664, 528],
        "poland": [2138, 616],
        "champions": [164, None],
        "euro": [2945, None],
        "uefa": [164, None],
        "chile": [716, 152],
    },
    "american-football": {
        "nfl": [389, 840],
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
    url = "https://thunderpick.io/api/matches"
    if (
        competition["sport"] in competition_urls
        and competition["competition"] in competition_urls[competition["sport"]]
    ):
        id = competition_urls[competition["sport"]][competition["competition"]]
        body = get_data(id[0], id[1], competition["sport"])
    else:
        return None
    async with get_session().post(
        url,
        json=body,
        headers=headers,
        cookies=cookies,
    ) as response:
        response = await response.json()
    return response


async def get_games(competition):
    response = await get_page(competition)
    if response is None:
        return None
    result = response["data"]["upcoming"]
    live = response["data"]["live"]
    both = result + live
    games = []
    for el in both:
        first = None
        second = None
        third = None
        team1 = el["teams"]["home"]["name"]
        team2 = el["teams"]["away"]["name"]
        market = el["market"]
        competition = el["competition"]["name"]
        if competition == "NFL":
            first = market["home"]["odds"]
            third = market["away"]["odds"]
            if first and third:
                odds = [float(first), float(third)]
                games.append({"team1": team1, "team2": team2, "odds": odds})
        else:
            first = market["home"]["odds"]
            second = market["draw"]["odds"]
            third = market["away"]["odds"]

            if first and second and third:
                odds = [float(first), float(second), float(third)]
                games.append({"team1": team1, "team2": team2, "odds": odds})
    return games
