from session_manager import get_german_session


def get_url(id):
    return f"https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=stake&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=stake&sportids=66&categoryids=0&champids={id}&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-05T16%3A20%3A00.000Z&endDate=2023-09-12T16%3A20%3A00.000Z"


# first
# https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=stake&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=stake&sportids=66&categoryids=0&champids=2936&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-05T16%3A20%3A00.000Z&endDate=2023-09-12T16%3A20%3A00.000Z
# https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=stake&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=stake&sportids=66&categoryids=0&champids=2936&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-05T16:20:00.000Z&endDate=2023-09-12T16:20:00.000Z
competition_urls = {
    "football": {
        "ligue1": "https://www.betseven13.com/iapi/sportsbook/v2/tournaments/34",
        "liga": "https://www.betseven13.com/iapi/sportsbook/v2/tournaments/8",
        "premier-league": "https://www.betseven13.com/iapi/sportsbook/v2/tournaments/17",
        "serie-a": "https://www.betseven13.com/iapi/sportsbook/v2/tournaments/23",
        "primeira": "https://www.betseven13.com/iapi/sportsbook/v2/tournaments/238",
        "serie-a-brasil": "https://www.betseven13.com/iapi/sportsbook/v2/tournaments/325",
        # "bundesliga-austria": get_url(2950),
        # "division-1a": "",
        "bundesliga": "https://www.betseven13.com/iapi/sportsbook/v2/tournaments/35",
        "copa-argentina": "https://www.betseven13.com/iapi/sportsbook/v2/tournaments/1024",
        "mls": "https://www.betseven13.com/iapi/sportsbook/v2/tournaments/242",
        "canada-premier": "https://www.betseven13.com/iapi/sportsbook/v2/tournaments/28432",
        "euro": "https://www.betseven13.com/iapi/sportsbook/v2/tournaments/27",
        "chile": "https://www.betseven13.com/iapi/sportsbook/v2/tournaments/27665",
        "colombia": "https://www.betseven13.com/iapi/sportsbook/v2/tournaments/27072",
        "scotland": "https://www.betseven13.com/iapi/sportsbook/v2/tournaments/36",
        "czech": "https://www.betseven13.com/iapi/sportsbook/v2/tournaments/172",
        "super-lig": "https://www.betseven13.com/iapi/sportsbook/v2/tournaments/52",
        "arabia": "https://www.betseven13.com/iapi/sportsbook/v2/tournaments/955",
    },
    "basketball": {
        # "nba": "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=sportsbetio&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=sportsbetio&sportids=67&categoryids=0&champids=2980&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-06T11%3A27%3A00.000Z&endDate=2023-09-13T11%3A27%3A00.000Z",
        # "euroleague": "https://www.betclic.fr/basket-ball-s4/euroligue-c14",
    },
    "tennis": {
        "us-open-men": get_url(3027),
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
    async with get_german_session().get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        },
        proxy=None,
    ) as response:
        response = await response.json()
    return response


async def get_games(competition):
    json = await get_page(competition)
    if json is None:
        return None
    games = []
    if json["data"] is None:
        return
    game_elements = json["data"]["events"]
    for el in game_elements:
        participants = el["participants"]
        team1 = participants["home"]["name"]
        team2 = participants["away"]["name"]
        odds = []
        first = None
        second = None
        third = None
        items = el["markets"]
        for item in items:
            if item["name"] == "1x2":
                odds = item["odds"]
                for odd in odds:
                    if odd["type"] == 1:
                        first = odd["value"]
                    elif odd["type"] == 2:
                        second = odd["value"]
                    elif odd["type"] == 3:
                        third = odd["value"]
        if first and second and third:
            odds = [float(first), float(second), float(third)]
            games.append({"team1": team1, "team2": team2, "odds": odds})
    return games
