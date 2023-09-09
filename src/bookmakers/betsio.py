from bs4 import BeautifulSoup

# import requests
import json
import aiohttp

# https://api.kineko.com/events?time=all&leagues%5B%5D=206230140992253952

# first
# https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=stake&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=stake&sportids=66&categoryids=0&champids=2936&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-05T16%3A20%3A00.000Z&endDate=2023-09-12T16%3A20%3A00.000Z
# https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-60&langId=8&skinName=stake&configId=12&culture=en-GB&countryCode=GB&deviceType=Desktop&numformat=en&integration=stake&sportids=66&categoryids=0&champids=2936&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-09-05T16:20:00.000Z&endDate=2023-09-12T16:20:00.000Z
competition_urls = {
    "football": {
        "bundesliga": "https://sport.bets.io/api/v2/matches?bettable=true&limit=100&match_status=0&sort_by=tournament.priority%3Aasc&sort_by=tournament.id%3Aasc&sort_by=start_time%3Aasc&sort_by=bets_count%3Adesc&tournament_id=15&type=match",
        "ligue1": "https://sport.bets.io/api/v2/matches?bettable=true&limit=100&match_status=0&sort_by=tournament.priority%3Aasc&sort_by=tournament.id%3Aasc&sort_by=start_time%3Aasc&sort_by=bets_count%3Adesc&tournament_id=18&type=match",
        "liga": "https://sport.bets.io/api/v2/matches?bettable=true&limit=100&match_status=0&sort_by=tournament.priority%3Aasc&sort_by=tournament.id%3Aasc&sort_by=start_time%3Aasc&sort_by=bets_count%3Adesc&tournament_id=17&type=match",
        "premier-league": "https://sport.bets.io/api/v2/matches?bettable=true&limit=100&match_status=0&sort_by=tournament.priority%3Aasc&sort_by=tournament.id%3Aasc&sort_by=start_time%3Aasc&sort_by=bets_count%3Adesc&tournament_id=14&type=match",
        "serie-a": "https://sport.bets.io/api/v2/matches?bettable=true&limit=100&match_status=0&sort_by=tournament.priority%3Aasc&sort_by=tournament.id%3Aasc&sort_by=start_time%3Aasc&sort_by=bets_count%3Adesc&tournament_id=16&type=match",
        "primeira": "https://sport.bets.io/api/v2/matches?bettable=true&limit=100&match_status=0&sort_by=tournament.priority%3Aasc&sort_by=tournament.id%3Aasc&sort_by=start_time%3Aasc&sort_by=bets_count%3Adesc&tournament_id=51&type=match",
        "serie-a-brasil": "https://sport.bets.io/api/v2/matches?bettable=true&limit=100&match_status=0&sort_by=tournament.priority%3Aasc&sort_by=tournament.id%3Aasc&sort_by=start_time%3Aasc&sort_by=bets_count%3Adesc&tournament_id=178&type=match",
        "bundesliga-austria": "https://sport.bets.io/api/v2/matches?bettable=true&limit=100&match_status=0&sort_by=tournament.priority%3Aasc&sort_by=tournament.id%3Aasc&sort_by=start_time%3Aasc&sort_by=bets_count%3Adesc&tournament_id=177&type=match",
        "division-1a": "https://sport.bets.io/api/v2/matches?bettable=true&limit=100&match_status=0&sort_by=tournament.priority%3Aasc&sort_by=tournament.id%3Aasc&sort_by=start_time%3Aasc&sort_by=bets_count%3Adesc&tournament_id=176&type=match",
        "super-lig": "https://sport.bets.io/api/v2/matches?bettable=true&limit=100&match_status=0&sort_by=tournament.priority%3Aasc&sort_by=tournament.id%3Aasc&sort_by=start_time%3Aasc&sort_by=bets_count%3Adesc&tournament_id=179&type=match",
        "croatia": "https://sport.bets.io/api/v2/matches?bettable=true&limit=100&match_status=0&sort_by=tournament.priority%3Aasc&sort_by=tournament.id%3Aasc&sort_by=start_time%3Aasc&sort_by=bets_count%3Adesc&tournament_id=189&type=match",
        "copa-argentina": "https://sport.bets.io/api/v2/matches?limit=100&match_status=2&match_status=3&match_status=4&match_status=5&sort_by=start_time%3Adesc&start_to=2023-09-07T15%3A06%3A36.748Z&tournament_id=1402&type=match",
        "eredivise": "https://sport.bets.io/api/v2/matches?bettable=true&limit=100&match_status=0&sort_by=tournament.priority%3Aasc&sort_by=tournament.id%3Aasc&sort_by=start_time%3Aasc&sort_by=bets_count%3Adesc&tournament_id=50&type=match",
        "arabia": "https://sport.bets.io/api/v2/matches?limit=100&match_status=2&match_status=3&match_status=4&match_status=5&sort_by=start_time%3Adesc&start_to=2023-09-07T20%3A51%3A55.822Z&tournament_id=2142&type=match",
        "poland": "https://sport.bets.io/api/v2/matches?limit=100&match_status=2&match_status=3&match_status=4&match_status=5&sort_by=start_time%3Adesc&start_to=2023-09-07T20%3A54%3A08.987Z&tournament_id=453&type=match",
        "champions": "https://sport.bets.io/api/v2/matches?limit=100&match_status=2&match_status=3&match_status=4&match_status=5&sort_by=start_time%3Adesc&start_to=2023-09-09T14%3A05%3A27.852Z&tournament_id=3&type=match",
        "uefa": "https://sport.bets.io/api/v2/matches?limit=100&match_status=2&match_status=3&match_status=4&match_status=5&sort_by=start_time%3Adesc&start_to=2023-09-09T14%3A06%3A48.449Z&tournament_id=35&type=match",
    },
    "basketball": {
        # "nba": "https://sport.bets.io/api/v2/matches?bettable=true&limit=100&match_status=0&sort_by=tournament.priority%3Aasc&sort_by=tournament.id%3Aasc&sort_by=start_time%3Aasc&sort_by=bets_count%3Adesc&tournament_id=12&type=match",
        # "euroleague": "https://www.betclic.fr/basket-ball-s4/euroligue-c14",
    },
    "tennis": {
        # "us-open-men": get_url(3027),
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
    if response is None:
        return None
    result = response["data"]
    games = []
    for el in result:
        team1 = el["competitors"]["home"]["name"]
        team2 = el["competitors"]["away"]["name"]
        first = None
        second = None
        third = None
        market = el["main_market"]
        if market is None:
            continue
        outcomes = market["outcomes"]
        for outcome in outcomes:
            if outcome["outcome_external_id"] == "1":
                first = outcome["odds"] / 1000
            if outcome["outcome_external_id"] == "2":
                second = outcome["odds"] / 1000
            if outcome["outcome_external_id"] == "3":
                third = outcome["odds"] / 1000

        if team1 and team2 and first and second and third:
            odds = [float(first), float(second), float(third)]
            games.append({"team1": team1, "team2": team2, "odds": odds})
    return games
