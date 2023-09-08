from bs4 import BeautifulSoup
import requests
import json
import aiohttp


def get_url(id):
    return f"https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=stake&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=stake&sportids=66&categoryids=0&champids={id}&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-05T16%3A20%3A00.000Z&endDate=2023-09-12T16%3A20%3A00.000Z"


# first
# https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=stake&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=stake&sportids=66&categoryids=0&champids=2936&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-05T16%3A20%3A00.000Z&endDate=2023-09-12T16%3A20%3A00.000Z
# https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=stake&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=stake&sportids=66&categoryids=0&champids=2936&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-05T16:20:00.000Z&endDate=2023-09-12T16:20:00.000Z
competition_urls = {
    "football": {
        "ligue1": "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=sportsbetio&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=sportsbetio&sportids=66&categoryids=0&champids=2943&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-06T11%3A25%3A00.000Z&endDate=2023-09-13T11%3A25%3A00.000Z",
        "liga": "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=sportsbetio&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=sportsbetio&sportids=66&categoryids=0&champids=2941&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-06T11%3A24%3A00.000Z&endDate=2023-09-13T11%3A24%3A00.000Z",
        "premier-league": "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=sportsbetio&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=sportsbetio&sportids=66&categoryids=0&champids=2936&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-06T11%3A23%3A00.000Z&endDate=2023-09-13T11%3A23%3A00.000Z",
        "serie-a": "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=sportsbetio&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=sportsbetio&sportids=66&categoryids=0&champids=2942&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-06T11%3A25%3A00.000Z&endDate=2023-09-13T11%3A25%3A00.000Z",
        "primeira": "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=sportsbetio&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=sportsbetio&sportids=66&categoryids=0&champids=3152&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-06T11%3A26%3A00.000Z&endDate=2023-09-13T11%3A26%3A00.000Z",
        "serie-a-brasil": "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=sportsbetio&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=sportsbetio&sportids=66&categoryids=0&champids=11318&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-06T11%3A25%3A00.000Z&endDate=2023-09-13T11%3A25%3A00.000Z",
        # "bundesliga-austria": get_url(2950),
        "division-1a": "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=sportsbetio&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=sportsbetio&sportids=66&categoryids=0&champids=2965&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-06T11%3A26%3A00.000Z&endDate=2023-09-13T11%3A26%3A00.000Z",
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
    json = await get_page(competition)
    if json is None:
        return None
    games = []
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
