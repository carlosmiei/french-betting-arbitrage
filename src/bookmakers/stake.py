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
        "ligue1": get_url(2943),
        "liga": get_url(2941),
        "premier-league": get_url(2936),
        "serie-a": get_url(2942),
        "primeira": get_url(3152),
        "serie-a-brasil": get_url(11318),
        "bundesliga-austria": get_url(2950),
        "division-1a": get_url(2965),
    },
    "basketball": {
        "nba": get_url(2980),
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
        # names = el.select(".betBox_contestantName")
        # team1 = "".join(names[0].text.split())
        # team2 = "".join(names[1].text.split())
        # odd_els = el.select(".oddValue")
        competitors = el["Competitors"]
        team1 = competitors[0]["Name"]
        team2 = competitors[1]["Name"]
        items = el["Items"]
        odds = []
        for item in items:
            if item["Name"] == "1x2":
                items = item["Items"]
                first = items[0]["Price"]
                second = items[1]["Price"]
                third = items[2]["Price"]
                odds = [float(first), float(second), float(third)]
                games.append({"team1": team1, "team2": team2, "odds": odds})
    return games
