from session_manager import get_session

# https://api.kineko.com/events?time=all&leagues%5B%5D=206230140992253952

# first
# https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=stake&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=stake&sportids=66&categoryids=0&champids=2936&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-05T16%3A20%3A00.000Z&endDate=2023-09-12T16%3A20%3A00.000Z
# https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=stake&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=stake&sportids=66&categoryids=0&champids=2936&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-05T16:20:00.000Z&endDate=2023-09-12T16:20:00.000Z
competition_urls = {
    "football": {
        "bundesliga": "https://platform.vave3.com/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008027&oddsExists_eq=1&lang=en",
        "ligue1": "https://platform.vave3.com/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008026&oddsExists_eq=1&lang=en",
        "liga": "https://platform.vave3.com/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008019&oddsExists_eq=1&lang=en",
        "premier-league": "https://platform.vave3.com/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008013&oddsExists_eq=1&lang=en",
        "serie-a": "https://platform.vave3.com/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008019&oddsExists_eq=1&lang=en",
        "primeira": "https://platform.vave3.com/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008129&oddsExists_eq=1&lang=en",
        "serie-a-brasil": "https://platform.vave3.com/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008158&oddsExists_eq=1&lang=en",
        "division-1a": "https://platform.vave3.com/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008030&oddsExists_eq=1&lang=en",
        "mls": "https://platform.vave5.com/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008132&oddsExists_eq=1&lang=en",
        "eredivise": "https://platform.vave5.com/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008029&oddsExists_eq=1&lang=en",
        "russia": "https://platform.vave5.com/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008107&oddsExists_eq=1&lang=en",
        "copa-argentina": "https://platform.vave5.com/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008415&oddsExists_eq=1&lang=en",
        "super-lig": "https://platform.vave5.com/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008040&oddsExists_eq=1&lang=en",
        "canada-premier": "https://platform.vave5.com/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008845&oddsExists_eq=1&lang=en",
        "arabia": "https://platform.vave5.com/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008401&oddsExists_eq=1&lang=en",
        "poland": "https://platform.vave5.com/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008126&oddsExists_eq=1&lang=en",
        "champions": "https://platform.vave5.com/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008006&oddsExists_eq=1&lang=en",
        "euro": "https://platform.vave5.com/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008023&oddsExists_eq=1&lang=en",
    },
    "basketball": {
        # "nba": "https://platform.vave3.com/api/event/list?period=0&competitor1Id_neq=&competitor2Id_neq=&status_in%5B%5D=0&limit=150&main=1&relations%5B%5D=odds&relations%5B%5D=league&relations%5B%5D=result&relations%5B%5D=competitors&relations%5B%5D=withMarketsCount&relations%5B%5D=players&relations%5B%5D=sportCategories&relations%5B%5D=broadcasts&relations%5B%5D=statistics&relations%5B%5D=additionalInfo&relations%5B%5D=tips&leagueId_in%5B%5D=1008918&oddsExists_eq=1&lang=en",
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
            for market in array:
                if market["id"] == 621:
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
                games.append({"team1": team1, "team2": team2, "odds": odds})
    return games
