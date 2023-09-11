from session_manager import get_session

# https://api.kineko.com/events?time=all&leagues%5B%5D=206230140992253952

# first
# https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=stake&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=stake&sportids=66&categoryids=0&champids=2936&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-05T16%3A20%3A00.000Z&endDate=2023-09-12T16%3A20%3A00.000Z
# https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=stake&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=stake&sportids=66&categoryids=0&champids=2936&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-05T16:20:00.000Z&endDate=2023-09-12T16:20:00.000Z
competition_urls = {
    "football": {
        "bundesliga": "https://api.kineko.com/events?time=all&leagues%5B%5D=207869682019102720",
        "ligue1": "https://api.kineko.com/events?time=all&leagues%5B%5D=208789850726486016",
        "liga": "https://api.kineko.com/events?time=all&leagues%5B%5D=207515800771391488",
        "premier-league": "https://api.kineko.com/events?time=all&leagues%5B%5D=206230140992253952",
        "serie-a": "https://api.kineko.com/events?time=all&leagues%5B%5D=207870093454110720",
        "primeira": "https://api.kineko.com/events?time=all&leagues%5B%5D=208790648538681344",
        "serie-a-brasil": "https://api.kineko.com/events?time=all&leagues%5B%5D=196545288139337728",
        "bundesliga-austria": "https://api.kineko.com/events?time=all&leagues%5B%5D=209214137756176384",
        "division-1a": "https://api.kineko.com/events?time=all&leagues%5B%5D=208680229196156928",
        "mls": "https://api.kineko.com/events?time=all&leagues%5B%5D=193475268207341568",
        "copa-argentina": "https://api.kineko.com/events?time=all&leagues%5B%5D=193998709095297024",
        "croatia": "https://api.kineko.com/events?time=all&leagues%5B%5D=209233409853247488",
        "eredivise": "https://api.kineko.com/events?time=all&leagues%5B%5D=208790444601135104",
        "super-lig": "https://api.kineko.com/events?time=all&leagues%5B%5D=209993008641363968",
        "russia": "https://api.kineko.com/events?time=all&leagues%5B%5D=208858552861872128",
        "champions": "https://api.kineko.com/events?time=all&leagues%5B%5D=206677483662241792",
        "euro": "https://api.kineko.com/events?time=all&leagues%5B%5D=193484342966775808",
        "chile": "https://api.kineko.com/events?time=all&leagues%5B%5D=193191553998680320",
        "belarus": "https://api.kineko.com/events?time=all&leagues%5B%5D=198399782630354944",
        "colombia": "https://api.kineko.com/events?time=all&leagues%5B%5D=193916186125299712",
        "ireland": "https://api.kineko.com/events?time=all&leagues%5B%5D=187291626410921984",
        "uruguai": "https://api.kineko.com/events?time=all&leagues%5B%5D=208858594166329344",
        "scotland": "https://api.kineko.com/events?time=all&leagues%5B%5D=209887985035005952",
        "czech": "https://api.kineko.com/events?time=all&leagues%5B%5D=208683427060404224",
    },
    "american-football": {
        "nfl": "https://api.kineko.com/events?time=all&leagues%5B%5D=196001834805129216"
    },
    "basketball": {
        # "nba": "https://api.trustdice.win/sports/tournament/?lang=en&sport=basketball&tag=upcoming&category=usa&tournament=nba&count=100",
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
        response = await response.json()
    return response


async def get_games(competition):
    response = await get_page(competition)
    if response is None:
        return None
    result = response["data"][0]["data"][0]["data"]
    games = []
    for el in result:
        first = None
        second = None
        third = None
        team1 = el["participants"][0]["name"]
        id1 = el["participants"][0]["id"]
        id2 = el["participants"][1]["id"]
        team2 = el["participants"][1]["name"]
        markets = el["markets"]
        if "winner" in markets:
            winner = markets["winner"]
            outcomes = winner["outcomes"]
            for outcome in outcomes:
                participant = None
                if outcome["name"].startswith("Winner"):
                    participant = outcome["participants"][0]["id"]
                if participant == id1:
                    first = outcome["odds"]
                elif participant == id2:
                    third = outcome["odds"]
                else:
                    second = outcome["odds"]
            if len(outcomes) == 2:
                if first and third:
                    odds = [float(first), float(third)]
                    games.append({"team1": team1, "team2": team2, "odds": odds})
            else:
                if first and second and third:
                    odds = [float(first), float(second), float(third)]
                    games.append({"team1": team1, "team2": team2, "odds": odds})
    return games
