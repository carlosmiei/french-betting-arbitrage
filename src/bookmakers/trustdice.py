from session_manager import get_session

# https://api.trustdice.win/sports/tournament/?lang=en&sport=soccer&tag=upcoming&category=germany&tournament=bundesliga


def get_url(id):
    return f"https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=stake&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=stake&sportids=66&categoryids=0&champids={id}&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-05T16%3A20%3A00.000Z&endDate=2023-09-12T16%3A20%3A00.000Z"


# first
# https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=stake&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=stake&sportids=66&categoryids=0&champids=2936&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-05T16%3A20%3A00.000Z&endDate=2023-09-12T16%3A20%3A00.000Z
# https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=stake&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=stake&sportids=66&categoryids=0&champids=2936&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-05T16:20:00.000Z&endDate=2023-09-12T16:20:00.000Z
competition_urls = {
    "football": {
        "bundesliga": "https://api.trustdice.win/sports/tournament/?lang=en&sport=soccer&tag=upcoming&category=germany&tournament=bundesliga&count=100",
        "ligue1": "https://api.trustdice.win/sports/tournament/?lang=en&sport=soccer&tag=upcoming&category=france&tournament=ligue-1&count=100",
        "liga": "https://api.trustdice.win/sports/tournament/?lang=en&sport=soccer&tag=upcoming&category=spain&tournament=laliga&count=100",
        "premier-league": "https://api.trustdice.win/sports/tournament/?lang=en&sport=soccer&tag=upcoming&category=england&tournament=premier-league&count=100",
        "serie-a": "https://api.trustdice.win/sports/tournament/?lang=en&sport=soccer&tag=upcoming&category=italy&tournament=serie-a&count=100",
        "primeira": "https://api.trustdice.win/sports/tournament/?lang=en&sport=soccer&tag=upcoming&category=portugal&tournament=liga-portugal&count=100",
        "serie-a-brasil": "https://api.trustdice.win/sports/tournament/?lang=en&sport=soccer&tag=upcoming&category=brazil&tournament=brasileiro-serie-a&count=100",
        "bundesliga-austria": "https://api.trustdice.win/sports/tournament/?lang=en&sport=soccer&tag=upcoming&category=austria&tournament=bundesliga&count=100",
        "division-1a": "https://api.trustdice.win/sports/tournament/?lang=en&sport=soccer&tag=upcoming&category=belgium&tournament=pro-league&count=100",
        "champions": "https://api.trustdice.win/sports/tournament/?lang=en&sport=soccer&tag=upcoming&category=international-clubs&tournament=uefa-champions-league&count=100",
        "euro": "https://api.trustdice.win/sports/tournament/?lang=en&sport=soccer&tag=upcoming&category=international&tournament=uefa-euro--qualification&count=5",
    },
    "american-football": {
        "nfl": "https://api.trustdice.win/sports/tournament/?lang=en&sport=american-football&tag=upcoming&category=usa&tournament=nfl&count=100"
    },
    "basketball": {
        # "nba": "https://api.trustdice.win/sports/tournament/?lang=en&sport=basketball&tag=upcoming&category=usa&tournament=nba&count=100",
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
    result = response["results"]
    keys = list(result.keys())
    game_elements = result[keys[0]]
    games = []
    for el in game_elements:
        markets = el["markets"]
        first = None
        second = None
        third = None
        team1 = None
        team2 = None
        for market in markets:
            if market is None:
                continue
            if market["name"] == "1x2" or market["name"] == "Winner (incl. overtime)":
                outcomes = market["outcomes"]
                for outcome in outcomes:
                    if outcome["outcome_id"] == "1" or outcome["outcome_id"] == "4":
                        first = outcome["odds"]
                        team1 = outcome["name"]
                    elif outcome["outcome_id"] == "3" or outcome["outcome_id"] == "5":
                        third = outcome["odds"]
                        team2 = outcome["name"]
                    elif outcome["outcome_id"] == "2":
                        second = outcome["odds"]
                if len(outcomes) == 2:
                    if first and third:
                        odds = [float(first), float(third)]
                        games.append({"team1": team1, "team2": team2, "odds": odds})
                else:
                    if first and second and third:
                        odds = [float(first), float(second), float(third)]
                        games.append({"team1": team1, "team2": team2, "odds": odds})
                break
    return games
