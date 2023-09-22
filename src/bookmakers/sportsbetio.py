from session_manager import get_session


def get_url(id):
    return f"https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=sportsbetio&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=sportsbetio&sportids=66&categoryids=0&champids={id}&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0"


competition_urls = {
    "football": {
        "ligue1": 2943,
        "liga": 2941,
        "premier-league": 2936,
        "serie-a": 2942,
        "primeira": 3152,
        "serie-a-brasil": 11318,
        "bundesliga-austria": 2950,
        "division-1a": 2965,
        "mls": 4610,
        "eredivise": 3065,
        "copa-argentina": 3916,
        "colombia": 3857,
        "arabia": 2934,
        "division-1a": 2965,
        "chile": 3837,
        "belarus": 5285,
        "czech": 3105,
        "russia": 3140,
        "canada": 5086,
        "super-lig": 2951,
    },
    "basketball": {},
    "tennis": {},
}


async def get_page(competition):
    if (
        competition["sport"] in competition_urls
        and competition["competition"] in competition_urls[competition["sport"]]
    ):
        id = competition_urls[competition["sport"]][competition["competition"]]
        url = get_url(id)
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
    json = await get_page(competition)
    if json is None:
        return None
    games = []
    if len(json["Result"]["Items"]) == 0:
        return
    game_elements = json["Result"]["Items"][0]["Events"]
    for el in game_elements:
        items = el["Items"]
        odds = []
        first = None
        second = None
        third = None
        team1 = None
        team2 = None
        for item in items:
            if item["Name"] == "1x2":
                odds = item["Items"]
                for odd in odds:
                    if odd["ColumnNum"] == 1:
                        first = odd["Price"]
                        team1 = odd["Name"].strip()
                    elif odd["ColumnNum"] == 2:
                        second = odd["Price"]
                    elif odd["ColumnNum"] == 3:
                        third = odd["Price"]
                        team2 = odd["Name"].strip()
        if first and second and third:
            odds = [float(first), float(second), float(third)]
            games.append({"team1": team1, "team2": team2, "odds": odds})
    return games
