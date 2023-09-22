from session_manager import get_session


def get_url(id):
    return f"https://sb2frontend-altenar2.biahosted.com/api/widget/GetEvents?culture=en-GB&timezoneOffset=-60&integration=spinbet&deviceType=1&numFormat=en-GB&countryCode=DE&eventCount=0&sportId=0&champIds={id}"


competition_urls = {
    "football": {
        "ligue1": 2943,
        "liga": 2941,
        "premier-league": 2936,
        "serie-a": 2942,
        "primeira": 3152,
        "serie-a-brasil": 11318,
        "bundesliga-austria": 2950,
        "division-1a": 2965,
        "mls": 4610,
        "eredivise": 3065,
        "copa-argentina": 3916,
        "colombia": 3857,
        "arabia": 2934,
        "division-1a": 2965,
        "chile": 3837,
        "belarus": 5285,
        "czech": 3105,
        "russia": 3140,
        "canada": 5086,
        "super-lig": 2951,
    },
    "basketball": {},
    "tennis": {},
}


async def get_page(competition):
    if (
        competition["sport"] in competition_urls
        and competition["competition"] in competition_urls[competition["sport"]]
    ):
        id = competition_urls[competition["sport"]][competition["competition"]]
        url = get_url(id)
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
    json = await get_page(competition)
    if json is None:
        return None
    games = []

    competitors = {}
    for team in json["competitors"]:
        competitors[team["id"]] = team["name"]

    for event in json["events"]:
        team1 = competitors[event["competitorIds"][0]]
        team2 = competitors[event["competitorIds"][1]]
        if len(event["marketIds"]) == 0:
            continue
        odd_id = event["marketIds"][0]
        ids = []
        for market in json["markets"]:
            if market["id"] == odd_id:
                ids = market["oddIds"]
                break
        first = None
        second = None
        third = None
        for odd in json["odds"]:
            if odd["id"] in ids:
                if odd["typeId"] == 1:
                    first = odd["price"]
                elif odd["typeId"] == 2:
                    second = odd["price"]
                elif odd["typeId"] == 3:
                    third = odd["price"]
        if first and second and third:
            odds = [float(first), float(second), float(third)]
            games.append(
                {
                    "team1": team1,
                    "team2": team2,
                    "odds": odds,
                }
            )
    return games
