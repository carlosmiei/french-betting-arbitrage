from bs4 import BeautifulSoup
import requests
import json
import aiohttp

# https://sportsbook.betplay.io/api/bettingfeed/preview/markets/bytournament?LangCode=en-US&TournamentId=39508


## get info about competitions
# https://sportsbook.betplay.io/api/bettingfeed/prematch/events?LangCode=en-US
def get_url(id):
    return f"https://sportsbook.betplay.io/api/bettingfeed/preview/markets/bytournament?LangCode=en-US&TournamentId={id}"


competition_urls = {
    "football": {
        "ligue1": get_url(39503),
        "liga": get_url(39616),
        "premier-league": get_url(39491),
        "serie-a": get_url(39461),
        "primeira": get_url(39575),
        "serie-a-brasil": get_url(39257),
        "bundesliga-austria": get_url(39382),
        "division-1a": get_url(41259),
        "bundesliga": get_url(39508),
    },
    "basketball": {
        "nba": get_url(3619),
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
    response = await get_page(competition)
    games = []
    for el in response:
        meta = el["ActiveMarkets"]
        match_id = None
        for m in meta:
            if m["Name"].strip() == "Match Winner":
                match_id = m["ID"]
                break
        active_odds = el["ActiveOdds"]
        first = None
        second = None
        third = None
        team1 = None
        team2 = None
        odds = []
        for odd in active_odds:
            if odd["MarketID"] == match_id:
                if odd["Name"] == "1":
                    team1 = odd["Title"]
                    first = odd["Value"]
                elif odd["Name"] == "x":
                    second = odd["Value"]
                elif odd["Name"] == "2":
                    team2 = odd["Title"]
                    third = odd["Value"]
            if first and second and third:
                odds = [float(first), float(second), float(third)]
                break
        # if len(odds) == 0:
        #     print("Something is off")
        games.append({"team1": team1, "team2": team2, "odds": odds})
    return games
