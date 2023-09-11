from session_manager import get_session
import json

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
        "mls": "https://sportservice.inplaynet.tech/api/prematch/getprematchgameall/de/52/?games=,25038268,25038271,25318690,25038269,25060107,25185990,25191371,25191369,25191370,25191372,25191373,25191374,25191375,25191377,25191378,25191380,25191379,25191381,25213113,",
        "russia": "https://sportservice.inplaynet.tech/api/prematch/getprematchgameall/de/52/?games=,26429482,26429484,26429486,26795875,26429481,26429495,26429483,26429480,26429489,26429493,26429494,26429490,26429491,26429492,26754272,26429496,",
        "arabia": "https://sportservice.inplaynet.tech/api/prematch/getprematchgameall/de/52/?games=,26841176,26841075,26841174,26841101,26841216,26841102,26841175,26841221,26841222,",
        "canada-premier": "https://sportservice.inplaynet.tech/api/prematch/getprematchgameall/de/52/?games=,26792516,26813779,26812483,26813733,",
        "poland": "https://sportservice.inplaynet.tech/api/prematch/getprematchgameall/de/52/?games=,26496940,26496944,26496942,26496945,26496904,26496946,26629339,26629340,26679726,",
        "champions": "https://sportservice.inplaynet.tech/api/prematch/getprematchgameall/en/52/?games=,26722899,26723067,26722900,26722998,26723001,26723070,26723187,26723190,26723250,26723458,26723253,26723349,26723350,26723459,26723776,26723777,-9968988,-11508514,-11508747,-11601270,-11514577,-11600641,-11515934,-11601043,-11514627,-11600642,-11515935,-11601044,-11514576,-11600635,-11515970,-11601045,-11514530,-11600638,-11516007,-11601047,-11514730,-11600639,-11516008,-11601048,",
        "uefa": "https://sportservice.inplaynet.tech/api/prematch/getprematchgameall/en/52/?games=,26742674,26742694,26742789,26742794,26742897,26742898,26742959,26742960,26741367,26741389,26741882,26741883,26742203,26742204,26742459,26742480,-10731538,-11528502,-11604471,-11583494,-11604559,-11528503,-11604470,-11583493,-11604556,-11528504,-11604543,-11583491,-11604557,-11528501,-11604544,-11583492,-11604562,-11528511,-11604545,-11583495,-11604561,-11528543,-11604546,-11583498,",
        "belarus": "https://sportservice.inplaynet.tech/api/prematch/getprematchgameall/en/52/?games=,26844116,26844114,26844117,26844115,26866986,",
        "euro": "https://sportservice.inplaynet.tech/api/prematch/getprematchgameall/de/52/?games=,-1686805,-5438584,-5458599,-5438586,-5438588,-5494458,-5438592,-5458637,-5438583,-5438585,-5494454,-5438587,-5438589,-5438590,-5494456,-5438591,-5494457,",
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
    try:
        return json.loads(response)
    except:
        return response


async def get_games(competition):
    response = await get_page(competition)
    if response is None:
        return None

    try:
        game_elements = json.loads(response["game"])
    except:
        game_elements = response["game"]
    teams = json.loads(response["teams"])
    names = {}
    for team in teams:
        names[team["ID"]] = team["Name"]
    games = []
    for el in game_elements:
        try:
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
            if first and second and third and team1 and team2:
                odds = [float(first), float(second), float(third)]
                games.append({"team1": team1, "team2": team2, "odds": odds})
        except:
            continue
    return games
