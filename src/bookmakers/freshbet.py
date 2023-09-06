from bs4 import BeautifulSoup
import requests
import json
import aiohttp

# https://sportservice.inplaynet.tech/api/prematch/getprematchgameall/en/52/?games=,25207895,25207890,25207893,25207897,25207889,25207891,25207898,25207894,25207892,25207896,25363539,25363542,25363545,25363551,25363552,25363556,25363557,25363558,25363559,25363560,


def get_url(id):
    return f"https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=stake&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=stake&sportids=66&categoryids=0&champids={id}&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-05T16%3A20%3A00.000Z&endDate=2023-09-12T16%3A20%3A00.000Z"


# first
# https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=stake&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=stake&sportids=66&categoryids=0&champids=2936&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-05T16%3A20%3A00.000Z&endDate=2023-09-12T16%3A20%3A00.000Z
# https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=stake&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=stake&sportids=66&categoryids=0&champids=2936&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-05T16:20:00.000Z&endDate=2023-09-12T16:20:00.000Z
competition_urls = {
    "football": {
        "ligue1": "https://sportservice.inplaynet.tech/api/prematch/getprematchgameall/en/52/?games=,26273789,26273794,26754890,26318058,26273790,26273798,26318059,26273799,26742782,26430548,26430551,26430566,26792454,26430550,26629518,26430567,26430547,26520742,",
        "liga": "https://sportservice.inplaynet.tech/api/prematch/getprematchgameall/en/52/?games=,25207895,25207890,25207893,25207897,25207889,25207891,25207898,25207894,25207892,25207896,25363539,25363542,25363545,25363551,25363552,25363556,25363557,25363558,25363559,25363560,",
        "premier-league": "https://sportservice.inplaynet.tech/api/prematch/getprematchgameall/en/52/?games=,26591314,26591308,26591309,26591316,26591317,26591319,26591327,26591315,26591318,26591328,26753820,26753823,26753826,26749916,26749876,26749859,26749879,26750022,26753827,26750105,",
        "serie-a": "https://sportservice.inplaynet.tech/api/prematch/getprematchgameall/en/52/?games=,26609734,26609744,26614975,26609769,26609787,26609792,26609788,26609791,26609793,26609813,26790714,26791352,26791416,26791417,26791426,26791445,",
        "primeira": "https://sportservice.inplaynet.tech/api/prematch/getprematchgameall/en/52/?games=,25983735,26451880,26451889,26451888,26451879,26451886,26451887,26451881,26451890,26451878,",
        "serie-a-brasil": "https://sportservice.inplaynet.tech/api/prematch/getprematchgameall/en/52/?games=,26514951,26514955,26514953,26514954,26537945,26514952,26560143,26560144,26581872,26581870,26626307,26647375,26647379,26669394,26669389,26669393,26692298,26692299,26713882,26736497,",
        "bundesliga-austria": "https://sportservice.inplaynet.tech/api/prematch/getprematchgameall/en/52/?games=,26093319,26115561,26115562,26115563,26115564,26367673,26115565,26594015,26137114,26743529,26271678,26271679,26293630,26293637,26744236,26009653,25881396,26293631,",
        "division-1a": "https://sportservice.inplaynet.tech/api/prematch/getprematchgameall/en/52/?games=,26753453,26753458,26753461,26753504,26753605,26753715,26753817,26753844,",
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
        return json.loads(response)


async def get_games(competition):
    response = await get_page(competition)
    game_elements = json.loads(response["game"])
    teams = json.loads(response["teams"])
    names = {}
    for team in teams:
        names[team["ID"]] = team["Name"]
    games = []
    for el in game_elements:
        # names = el.select(".betBox_contestantName")
        # team1 = "".join(names[0].text.split())
        # team2 = "".join(names[1].text.split())
        # odd_els = el.select(".oddValue")
        team1 = names[el["t1"]]
        team2 = names[el["t2"]]
        ev = el["ev"]
        main_odds = ev["448"]
        values = list(main_odds.values())
        odds = list(values)
        first = None
        second = None
        third = None
        for odd in odds:
            if odd["pos"] == 1:
                first = odd["coef"]
            elif odd["pos"] == 2:
                second = odd["coef"]
            elif odd["pos"] == 3:
                third = odd["coef"]
        odds = [float(first), float(second), float(third)]
        games.append({"team1": team1, "team2": team2, "odds": odds})
    return games
