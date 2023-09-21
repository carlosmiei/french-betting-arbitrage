from session_manager import get_session

competition_urls = {
    "football": {
        "bundesliga": "https://platform.ivibets.org/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008027&oddsExists_eq=1&lang=en",
        "ligue1": "https://platform.ivibets.org/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008026&oddsExists_eq=1&lang=en",
        "liga": "https://platform.ivibets.org/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008007&oddsExists_eq=1&lang=en",
        "premier-league": "https://platform.ivibets.org/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008013&oddsExists_eq=1&lang=en",
        "serie-a": "https://platform.ivibets.org/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008019&oddsExists_eq=1&lang=en",
        "primeira": "https://platform.ivibets.org/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008129&oddsExists_eq=1&lang=en",
        "serie-a-brasil": "https://platform.ivibets.org/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008158&oddsExists_eq=1&lang=en",
        "division-1a": "https://platform.ivibets.org/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008030&oddsExists_eq=1&lang=en",
        "mls": "https://platform.ivibets.org/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008132&oddsExists_eq=1&lang=en",
        "poland": "https://platform.ivibets.org/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008106&oddsExists_eq=1&lang=en",
        "copa-argentina": "https://platform.ivibets.org/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008847&oddsExists_eq=1&lang=en",
        "eredivise": "https://platform.ivibets.org/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008029&oddsExists_eq=1&lang=en",
        "super-lig": "https://platform.ivibets.org/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008158&leagueId_in%5B%5D=1008040&oddsExists_eq=1&lang=en",
        "champions": "https://platform.ivibets.org/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008006&oddsExists_eq=1&lang=en",
        "colombia": "https://platform.ivibets.org/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008791&oddsExists_eq=1&lang=en",
        "ireland": "https://platform.ivibets.org/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008096&oddsExists_eq=1&lang=en",
        "uefa": "https://platform.ivibets.org/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008283&oddsExists_eq=1&lang=en=en",
    },
    "american-football": {
        # "nfl": "https://api.kineko.com/events?time=all&leagues%5B%5D=196001834805129216"
    },
    "basketball": {
        # "nba": "https://api.trustdice.win/sports/tournament/?lang=en&sport=basketball&tag=upcoming&category=usa&tournament=nba&count=100",
        # "euroleague": "https://www.betclic.fr/basket-ball-s4/euroligue-c14",
    },
    "tennis": {
        # "us-open-men": get_url(3027),
    },
}


async def get_page(competition):
    if (
        competition["sport"] in competition_urls
        and competition["competition"] in competition_urls[competition["sport"]]
    ):
        url = competition_urls[competition["sport"]][competition["competition"]]
    else:
        return None
    async with get_session().get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        },
    ) as response:
        response = await response.json()
    return response


def get_live_games(response):
    competitions = response["data"][0]["data"]
    games = []
    for league in competitions:
        for game in league["data"]:
            if game["is_live"] == 1:
                first = None
                second = None
                third = None
                open = False
                team1 = game["participants"][0]["name"]
                id1 = game["participants"][0]["id"]
                id2 = game["participants"][1]["id"]
                team2 = game["participants"][1]["name"]
                markets = game["markets"]
                if "winner" in markets:
                    winner = markets["winner"]
                    open = winner["open"]
                    outcomes = winner["outcomes"]
                    for outcome in outcomes:
                        participant = None
                        if outcome["name"].startswith("Winner"):
                            participant = outcome["participants"][0]["id"]
                        if participant == id1:
                            first = outcome["odds"]
                        elif participant == id2:
                            third = outcome["odds"]
                        else:
                            second = outcome["odds"]
                    if len(outcomes) == 2:
                        if first and third:
                            odds = [float(first), float(third)]
                            games.append(
                                {
                                    "team1": team1,
                                    "team2": team2,
                                    "odds": odds,
                                    "open": open,
                                }
                            )
                    else:
                        if first and second and third:
                            odds = [float(first), float(second), float(third)]
                            games.append(
                                {
                                    "team1": team1,
                                    "team2": team2,
                                    "odds": odds,
                                    "open": open,
                                }
                            )
    return games


async def get_games(competition):
    response = await get_page(competition)
    if response is None:
        return None
    if response["code"] != 200:
        return None

    games = []
    data = response["data"]
    items = data["items"]
    competitors = data["relations"]["competitors"]

    teams = {}
    for competitor in competitors:
        teams[competitor["id"]] = competitor["name"]

    info = {}
    for item in items:
        info[str(item["id"])] = {
            "home": item["competitor1Id"],
            "away": item["competitor2Id"],
        }

    odds = data["relations"]["odds"]
    keys = list(odds.keys())
    for key in keys:
        results = odds[key]
        for result in results:
            if result["id"] == 621:
                active = False
                outcomes = result["outcomes"]
                first = None
                second = None
                third = None
                team1 = teams[info[key]["home"]]
                team2 = teams[info[key]["away"]]
                for outcome in outcomes:
                    if outcome["id"] == 1:
                        first = outcome["odds"]
                        active = outcome["active"] == 1
                    elif outcome["id"] == 2:
                        second = outcome["odds"]
                        active = outcome["active"] == 1
                    elif outcome["id"] == 3:
                        third = outcome["odds"]
                        active = outcome["active"] == 1
                if first and second and third and team1 and team2:
                    game_odds = [float(first), float(second), float(third)]
                    games.append(
                        {
                            "team1": team1,
                            "team2": team2,
                            "odds": game_odds,
                            "active": active,
                        }
                    )
    return games
