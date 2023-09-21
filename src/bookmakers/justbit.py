from session_manager import get_session

headers = {
    "authority": "c117x.play-platform.com",
    "accept": "application/json",
    "accept-language": "en-GB,en;q=0.8",
    "content-type": "application/json",
    # 'cookie': 'cf_clearance=LY8t_aD2mmvWOJgQayTt9A1dmso8Tqz71saomP.bYl4-1695285729-0-1-1bd65104.1c78dd43.74be7303-0.2.1695285729',
    "device": "desktop",
    "origin": "https://c117x.play-platform.com",
    "referer": "https://c117x.play-platform.com/sportsbook/Football/England/Premier%20League",
    "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Brave";v="116"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "x-locale": "ENG",
    "x-project-id": "117",
}


def get_data(category, tournment_id):
    json_data = {
        "filter": {
            "categoryId": category,
            "onlyMainMarketTypes": True,
            "sportId": 1,
            "tournamentId": tournment_id,
            "fromDate": None,
            "timeHours": None,
            "toDate": None,
            "sportServices": [
                "LIVE",
                "PREMATCH",
            ],
        },
    }
    return json_data


competition_urls = {
    "football": {
        "bundesliga": [261, 6367],
        "ligue1": [250, 6279],
        "liga": [246, 6208],
        "premier-league": [325, 7354],
        "serie-a": [304, 7089],
        "primeira": [200, 5411],
        "mls": [153, 4967],
        "champions": [1602, 8137],
        "uefa": [1602, 8064],
        "eredivise": [230, 5783],
        "chile": [286, 6907],
        "serie-a-brasil": [278, 6708],
        "arabia": [203, 5484],
        "bundesliga-austria": [266, 30381],
        "division-1a": [271, 40386],
        "super-lig": [214, 5700],
        "poland": [161, 5093],
        "czech": [292, 6971],
        "colombia": [288, 6936],
    },
    "basketball": {
        # "nba": 3,
        # "euroleague": "https://www.betclic.fr/basket-ball-s4/euroligue-c14",
    },
    "tennis": {
        # "us-open-men": get_url(3027),
    },
}

params = {
    "locale": "ENG",
}


async def get_page(competition):
    url = "https://c117x.play-platform.com/api/sportsbook/events"
    if (
        competition["sport"] in competition_urls
        and competition["competition"] in competition_urls[competition["sport"]]
    ):
        ids = competition_urls[competition["sport"]][competition["competition"]]
        body = get_data(ids[0], ids[1])
    else:
        return None
    async with get_session().post(
        url,
        json=body,
        headers=headers,
        params=params,
    ) as response:
        response = await response.json()
    return response


async def get_games(competition):
    response = await get_page(competition)
    if response is None:
        return None

    data = response["data"]
    if len(data) == 0:
        return None
    keys = list(data.keys())
    key = keys[0]
    games = []
    events = data[key]["events"]
    events_keys = list(events.keys())
    for event_key in events_keys:
        event = events[event_key]
        if (len(event["participants"])) == 0:
            continue
        home = event["participants"]["home"]["fullName"]
        away = event["participants"]["away"]["fullName"]
        marketTypes = event["marketTypes"]
        if "346" in marketTypes:
            active = False
            winner = marketTypes["346"]
            markets = winner["markets"]
            markets_keys = list(markets.keys())
            key = markets_keys[0]
            market = markets[key]
            active = market["status"] == "ACTIVE"
            odds = market["outcomes"]
            first = None
            second = None
            third = None
            odds_keys = list(odds.keys())
            for key in odds_keys:
                outcome = odds[key]
                if outcome["name"] == home:
                    first = outcome["odds"]
                elif outcome["name"] == away:
                    third = outcome["odds"]
                elif outcome["name"] == "X":
                    second = outcome["odds"]

            if first and second and third:
                odds = [float(first), float(second), float(third)]
                games.append(
                    {"team1": home, "team2": away, "odds": odds, "active": active}
                )
    return games
