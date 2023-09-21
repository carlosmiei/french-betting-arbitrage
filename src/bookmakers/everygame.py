from session_manager import get_session
import json
from bs4 import BeautifulSoup

competition_urls = {
    "football": {
        "bundesliga": "https://sports.everygame.eu/en/Bets/Soccer/German-1st-Bundesliga/934",
        "ligue1": "https://sports.everygame.eu/en/Bets/Soccer/French-Ligue-1/942",
        "liga": "https://sports.everygame.eu/en/Bets/Soccer/Spanish-LaLiga/944",
        "premier-league": "https://sports.everygame.eu/en/Bets/Soccer/English-Premier-League/923",
        "serie-a": "https://sports.everygame.eu/en/Bets/Soccer/Italian-Serie-A/943",
        "primeira": "https://sports.everygame.eu/en/Bets/Soccer/Portuguese-Primeira-Liga/945",
        "serie-a-brasil": "https://sports.everygame.eu/en/Bets/Soccer/Brazilian-Serie-A/1023",
        "champions": "https://sports.everygame.eu/en/Bets/Soccer/UEFA-Champions-League/922",
        "uefa": "https://sports.everygame.eu/en/Bets/Soccer/UEFA-Europa-League/921",
        "mls": "https://sports.everygame.eu/en/Bets/Soccer/US-MLS/858",
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
        url = competition_urls[competition["sport"]][competition["competition"]]
    else:
        return None
    async with get_session().get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        },
    ) as response:
        response = await response.text()
    return response


async def get_games(competition):
    response = await get_page(competition)
    if response is None:
        return None
    games = []
    soup = BeautifulSoup(response, "html.parser")
    results = soup.find(id="page")
    content = results.find(id="content")
    center_content = content.find(id="center-col-content")
    competition = center_content.find(id="competition-view-content")
    table = competition.find_all("ul")[0]
    entries = table.find_all("li")
    match_winner = entries[0]
    events = match_winner.find_all("div", class_="onemarket tr")
    for event in events:
        first = None
        second = None
        third = None
        team1 = None
        team2 = None
        trw = event.find("div", class_="trw")
        childs = trw.findChildren("div", recursive=False)
        i = 0
        for child in childs:
            if i == 0:
                name = child.find("b").text
                parts = name.split(" v ")
                team1 = parts[0]
                team2 = parts[1]
            elif i == 1:
                first = float(child.find("span").text)
            elif i == 2:
                second = float(child.find("span").text)
            elif i == 3:
                third = float(child.find("span").text)
            i += 1
        if first and second and third and team1 and team2:
            odds = [first, second, third]
            games.append({"team1": team1, "team2": team2, "odds": odds})

    #     if first and second and third:
    #         odds = [float(first), float(second), float(third)]
    #         games.append({"team1": home, "team2": away, "odds": odds, "active": active})
    return games
