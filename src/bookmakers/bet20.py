from session_manager import get_session

cookies = {
    "_ga": "GA1.1.1842126177.1695323861",
    "sid": "79273f2015f4bad93c03308cd15eb972",
    "_ga_J9LNZYMXZE": "GS1.1.1695370148.2.1.1695396130.0.0.0",
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
        "period": "0",
        "competitor1Id_neq": "",
        "competitor2Id_neq": "",
        "status_in[]": "0",
        "limit": "150",
        "main": "1",
        "relations[]": [
            "odds",
            "league",
            "result",
            "competitors",
            "withMarketsCount",
            "players",
            "sportCategories",
            "broadcasts",
            "statistics",
            "additionalInfo",
            "tips",
        ],
        "leagueId_in[]": str(tournment_id),
        "oddsExists_eq": "1",
        "lang": "en",
    }
    return params


competition_urls = {
    "football": {
        "bundesliga": 1008027,
        "ligue1": 1008026,
        "liga": 1008007,
        "premier-league": 1008013,
        "serie-a": 1008019,
        "primeira": 1008129,
        "mls": 1008132,
        "champions": 1008006,
        "uefa": 1008283,
        # "eredivise": ,
        # "chile":,
        # "serie-a-brasil":,
        # "arabia":,
        # "bundesliga-austria": ,
        # "division-1a",
        "super-lig": 1008040,
        # "poland":,
        # "czech":,
        # "colombia": ,
        "russia": 1008107,
        "arabia": 1008401,
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
    url = "https://platform.20bet.life/api/event/list"
    # url = "https://platform.20bet.life/api/outright/list"
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
    result = response["data"]
    items = result["items"]
    relations = result["relations"]
    competitors = relations["competitors"]
    teams = {}
    for competitor in competitors:
        teams[competitor["id"]] = competitor["name"]
    events = {}
    for item in items:
        events[item["id"]] = {
            "team1": teams[item["competitor1Id"]],
            "team2": teams[item["competitor2Id"]],
        }
    games = []
    odds = relations["odds"]
    for id, array in odds.items():
        if int(id) in events:
            team1 = events[int(id)]["team1"]
            team2 = events[int(id)]["team2"]
            active = False
            for market in array:
                if market["id"] == 621:
                    active = market["status"] == 1
                    outcomes = market["outcomes"]
                    for outcome in outcomes:
                        if outcome["id"] == 1:
                            first = outcome["odds"]
                        elif outcome["id"] == 2:
                            second = outcome["odds"]
                        elif outcome["id"] == 3:
                            third = outcome["odds"]

            if first and second and third:
                odds = [float(first), float(second), float(third)]
                games.append(
                    {"team1": team1, "team2": team2, "odds": odds, "active": active}
                )
    return games
