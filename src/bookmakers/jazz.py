from bs4 import BeautifulSoup

# import requests
import json
import aiohttp


headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-GB,en;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Origin": "https://betslip.jazzcasino.com",
    "Referer": "https://betslip.jazzcasino.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Sec-GPC": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "jz-signature": "495c985a673ff4477696d1018129c48eeedec89f7fcd4a987e12855110483ac7",
    "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
}


def get_data(id):
    json_data = {
        "Gmt": -100,
        "NextHour": False,
        "SiteId": 786,
        "IdPlayer": 0,
        "Player": "ECO123",
        "LineStyle": "D",
        "LeagueList": [
            id,
        ],
    }
    return json_data


# response = requests.post(
#     "https://betslipapi.isppro.net/api/Guest/GetNewLines",
#     headers=headers,
#     json=json_data,
# )

competition_urls = {
    "football": {
        "bundesliga": 334,
        # "ligue1": "",
        "liga": 68,
        "premier-league": 59,
        "serie-a": 60,
        "primeira": 179,
        "mls": 115,
        # "serie-a-brasil": "",
        # "bundesliga-austria": "",
        # "division-1a": "",
    },
    "basketball": {
        "nba": 3,
        # "euroleague": "https://www.betclic.fr/basket-ball-s4/euroligue-c14",
    },
    "tennis": {
        # "us-open-men": get_url(3027),
    },
}


async def get_page(competition):
    url = "https://betslipapi.isppro.net/api/Guest/GetNewLines"
    async with aiohttp.ClientSession() as session:
        if (
            competition["sport"] in competition_urls
            and competition["competition"] in competition_urls[competition["sport"]]
        ):
            id = competition_urls[competition["sport"]][competition["competition"]]
            body = get_data(id)
        else:
            return None
        async with session.post(
            url,
            data=body,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
            },
        ) as response:
            response = await response.json()
        return response


def american_to_decimal(american_odds):
    if str(american_odds)[0] == "-" or str(american_odds)[0] == "+":
        american_odds = float(american_odds)
        if american_odds > 0:
            return round(american_odds / 100 + 1, 2)
        else:
            return round(100 / abs(american_odds) + 1, 2)
    return float(american_odds)


async def get_games(competition):
    response = await get_page(competition)
    result = response[0]["Games"]
    games = []
    for el in result:
        first = None
        second = None
        third = None
        team1 = el["Vtm"].lower()
        team2 = el["Htm"].lower()
        lines = el["Lines"]
        if len(lines) < 2:
            continue
        second_line = lines[1]
        first = american_to_decimal(second_line["Hoddsh"])
        second = american_to_decimal(second_line["Vsph"])
        third = american_to_decimal(second_line["Voddsh"])

        if first and second and third:
            odds = [float(first), float(second), float(third)]
            games.append({"team1": team1, "team2": team2, "odds": odds})
    return games
