from bs4 import BeautifulSoup

# import requests
import json
import aiohttp

# https://api.kineko.com/events?time=all&leagues%5B%5D=206230140992253952

# first
# https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=stake&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=stake&sportids=66&categoryids=0&champids=2936&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-05T16%3A20%3A00.000Z&endDate=2023-09-12T16%3A20%3A00.000Z
# https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=stake&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=stake&sportids=66&categoryids=0&champids=2936&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-05T16:20:00.000Z&endDate=2023-09-12T16:20:00.000Z
competition_urls = {
    "football": {
        "bundesliga": "https://1xbit1.com/LineFeed/Get1x2_VZip?sports=1&champs=12821%2C96463&count=100&lng=en&tf=2200000&tz=1&mode=4&country=53&partner=65&getEmpty=true",
        "ligue1": "https://1xbit1.com/LineFeed/Get1x2_VZip?sports=1&champs=12821%2C127733&count=100&lng=en&tf=2200000&tz=1&mode=4&country=53&partner=65&getEmpty=true",
        "liga": "https://1xbit1.com/LineFeed/Get1x2_VZip?sports=1&champs=88637%2C127733&count=100&lng=en&tf=2200000&tz=1&mode=4&country=53&partner=65&getEmpty=true",
        "premier-league": "https://1xbit1.com/LineFeed/Get1x2_VZip?sports=1&champs=88637&count=100&lng=en&tf=2200000&tz=1&mode=4&country=53&partner=65&getEmpty=true",
        "serie-a": "https://1xbit1.com/LineFeed/Get1x2_VZip?sports=1&champs=110163&count=100&lng=en&tf=2200000&tz=1&mode=4&country=53&partner=65&getEmpty=true",
        "primeira": "https://1xbit1.com/LineFeed/Get1x2_VZip?sports=1&champs=118663&count=100&lng=en&tf=2200000&tz=1&mode=4&country=53&partner=65&getEmpty=true",
        "serie-a-brasil": "https://1xbit1.com/LineFeed/Get1x2_VZip?sports=1&champs=96463%2C1268397&count=100&lng=en&tf=2200000&tz=1&mode=4&country=53&partner=65&getEmpty=true",
        "bundesliga-austria": "https://1xbit1.com/LineFeed/Get1x2_VZip?sports=1&champs=26031%2C28787&count=100&lng=en&tf=2200000&tz=1&mode=4&country=53&partner=65&getEmpty=true",
        "division-1a": "https://1xbit1.com/LineFeed/Get1x2_VZip?sports=1&champs=28787&count=100&lng=en&tf=2200000&tz=1&mode=4&country=53&partner=65&getEmpty=true",
        "mls": "https://1xbit1.com/LineFeed/Get1x2_VZip?sports=1&champs=828065&count=50&lng=en&tf=2200000&tz=1&mode=4&country=53&partner=65&getEmpty=true",
        "russia": "https://1xbit1.com/LineFeed/Get1x2_VZip?sports=1&champs=225733%2C828065&count=100&lng=en&tf=2200000&tz=1&mode=4&country=53&partner=65&getEmpty=true",
        "eredivise": "https://1xbit1.com/LineFeed/Get1x2_VZip?sports=1&champs=2018750&count=50&lng=en&tf=2200000&tz=1&mode=4&country=53&partner=65&getEmpty=true",
        "super-lig": "https://1xbit1.com/LineFeed/Get1x2_VZip?sports=1&champs=11113&count=100&lng=en&tf=2200000&tz=1&mode=4&country=53&partner=65&getEmpty=true",
        "copa-argentina": "https://1xbit1.com/LineFeed/Get1x2_VZip?sports=1&champs=119577&count=50&lng=en&tf=2200000&tz=1&mode=4&country=53&partner=65&getEmpty=true",
        "croatia": "https://1xbit1.com/LineFeed/Get1x2_VZip?sports=1&champs=2439506&count=50&lng=en&tf=2200000&tz=1&mode=4&country=53&partner=65&getEmpty=true",
        "canada-premier": "https://1xbit1.com/LineFeed/Get1x2_VZip?sports=1&champs=1924563&count=50&lng=en&tf=2200000&tz=1&mode=4&country=53&partner=65&getEmpty=true",
        "poland": "https://1xbit1.com/LineFeed/Get1x2_VZip?sports=1&champs=30693&count=50&lng=en&tf=2200000&tz=1&mode=4&country=53&partner=65&getEmpty=true",
        "arabia": "https://1xbit1.com/LineFeed/Get1x2_VZip?sports=1&champs=16819&count=50&lng=en&tf=2200000&tz=1&mode=4&country=53&partner=65&getEmpty=true",
    },
    "basketball": {
        # "nba": "",
        # "euroleague": "https://www.betclic.fr/basket-ball-s4/euroligue-c14",
    },
    "tennis": {
        # "us-open-men": get_url(3027),
    },
}


async def get_page(competition):
    async with aiohttp.ClientSession() as session:
        if (
            competition["sport"] in competition_urls
            and competition["competition"] in competition_urls[competition["sport"]]
        ):
            url = competition_urls[competition["sport"]][competition["competition"]]
        else:
            return None
        async with session.get(
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
    result = response["Value"]
    games = []
    for el in result:
        first = None
        second = None
        third = None
        team1 = el["O1"]
        team2 = el["O2"]
        odds = el["E"]
        for odd in odds:
            if odd["T"] == 1:
                first = odd["C"]
            elif odd["T"] == 2:
                second = odd["C"]
            elif odd["T"] == 3:
                third = odd["C"]

        if first and second and third:
            odds = [float(first), float(second), float(third)]
            games.append({"team1": team1, "team2": team2, "odds": odds})
    return games
