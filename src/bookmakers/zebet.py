from bs4 import BeautifulSoup
import requests
import aiohttp

competition_urls = {
    "football": {
        "ligue1": "https://www.zebet.fr/fr/competition/96-ligue_1_uber_eats",
        "liga": "https://www.zebet.fr/fr/competition/306-laliga",
        "bundesliga": "https://www.zebet.fr/fr/competition/268-bundesliga",
        "premier-league": "https://www.zebet.fr/fr/competition/94-premier_league",
        "serie-a": "https://www.zebet.fr/fr/competition/305-serie_a",
        "primeira": "https://www.zebet.fr/fr/competition/154-primeira_liga",
        "serie-a-brasil": "https://www.zebet.fr/fr/competition/81-brasileirao",
        "a-league": "https://www.zebet.fr/fr/competition/2169-a_league",
        "bundesliga-austria": "https://www.zebet.fr/fr/competition/131-bundesliga",
        "division-1a": "https://www.zebet.fr/fr/competition/101-pro_league_1a",
        "super-lig": "https://www.zebet.fr/fr/competition/254-super_lig",
    },
    "basketball": {
        "nba": "https://www.zebet.fr/fr/competition/206-nba",
        "euroleague": "https://www.zebet.fr/fr/competition/12044-euroligue",
    },
}

session = aiohttp.ClientSession()


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
    html = BeautifulSoup(response.content, "html.parser")
    return html


async def get_games(competition):
    html = await get_page(competition)
    games = []
    game_elements = html.select(".pari-1")
    for el in game_elements:
        names = el.select(".pmq-cote-acteur")
        team1 = "".join(names[0].text.split())
        if competition["sport"] == "football":
            team2 = "".join(names[4].text.split())
        elif competition["sport"] == "basketball":
            team2 = "".join(names[2].text.split())
        odd_els = el.select(".pmq-cote")
        odds = []
        for odd_el in odd_els[::2]:
            odds.append(float(odd_el.text.replace(",", ".")))
        games.append({"team1": team1, "team2": team2, "odds": odds})
    return games
