from session_manager import get_session
import json


def get_url(competition):
    return f"https://www.cloudbet.com/sports-api/c/v6/sports/competitions/{competition}/events?markets=soccer.match_odds&locale=en"


competition_urls = {
    "football": {
        "bundesliga": "soccer-germany-bundesliga",
        "ligue1": "soccer-france-ligue-1",
        "liga": "soccer-spain-laliga",
        "premier-league": "soccer-england-premier-league",
        "serie-a": "soccer-italy-serie-a",
        "primeira": "soccer-portugal-primeira-liga",
        "serie-a-brasil": "soccer-brazil-brasileiro-serie-a",
        "bundesliga-austria": "soccer-austria-bundesliga",
        "division-1a": "soccer-belgium-first-division-a",
        "champions": "soccer-international-clubs-uefa-champions-league",
        "uefa": "soccer-international-clubs-uefa-europa-league",
        "ireland": "soccer-ireland-premier-division",
        "colombia": "soccer-colombia-primera-a-clausura",
        "canada": "soccer-canada-canadian-premier-league",
        "czech": "soccer-czech-republic-1-liga",
        "poland": "soccer-poland-ekstraklasa",
        "russia": "soccer-russia-premier-league",
        "mls": "soccer-usa-major-league-soccer",
        "super-lig": "soccer-turkey-super-lig",
        "arabia": "soccer-saudi-arabia-saudi-prof-league",
        "copa-argentina": "soccer-argentina-copa-diego-armando-maradona",
        "belarus": "soccer-belarus-vysshaya-liga",
        "canada": "soccer-canada-canadian-premier-league",
    },
    "basketball": {
        # "nba": "https://sportservice.inplaynet.tech/api/prematch/getprematchgameall/en/94/?games=,26389912,26389944,26390000,26393376,26393431,26393435,26379138,26390038,26390051,26390076,26390119,26390258,26390197,26390088,26346468,26347974,26347979,26347980,26348001,26348008,26348015,26348055,26348056,26348082,26348087,26348106,26348111,26348120,26348132,26348153,26348268,26348322,26348339,26348344,26348349,26348373,26348382,26348385,26348395,26348419,",
        # "euroleague": "https://www.betclic.fr/basket-ball-s4/euroligue-c14",
    },
    "tennis": {
        # "us-open-men": get_url(3027),
    },
}


async def get_page(competition):
    if (
        competition["sport"] in competition_urls
        and competition["competition"] in competition_urls[competition["sport"]]
    ):
        url = get_url(
            competition_urls[competition["sport"]][competition["competition"]]
        )
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
    games = []
    events = response["events"]
    for event in events:
        if event["home"] is None:
            continue

        home = event["home"]["name"]
        away = event["away"]["name"]
        markets = event["markets"]
        if "soccer.match_odds" not in markets:
            continue
        selections = markets["soccer.match_odds"]["submarkets"]["period=ft"][
            "selections"
        ]
        first = None
        second = None
        third = None
        active = False
        for selection in selections:
            if selection["outcome"] == "home":
                first = selection["price"]
                active = selection["status"] == "SELECTION_ENABLED"
            if selection["outcome"] == "draw":
                second = selection["price"]
                active = selection["status"] == "SELECTION_ENABLED"
            if selection["outcome"] == "away":
                third = selection["price"]
                active = selection["status"] == "SELECTION_ENABLED"
        if first and second and third:
            odds = [float(first), float(second), float(third)]
            games.append({"team1": home, "team2": away, "odds": odds, "active": active})
    return games
