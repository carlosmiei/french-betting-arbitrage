from session_manager import get_session
from datetime import datetime
import time

headers = {
    "authority": "sports-mts-services-api.gb.nsoftcdn.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-GB,en;q=0.7",
    "origin": "https://betcoinsports.web.7platform.net",
    "referer": "https://betcoinsports.web.7platform.net/",
    "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Brave";v="116"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
}


def convert_ts(ts):
    dt_object = datetime.fromtimestamp(ts)
    formatted_date = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date


def get_params(tournment_id):
    current_ts = time.time()
    ts_7_days_ahead = current_ts + 518400
    init_date = convert_ts(current_ts)
    end_date = convert_ts(ts_7_days_ahead)
    ids = ""
    if isinstance(tournment_id, str):
        ids = '"%s"' % tournment_id
    else:
        ids = ",".join(['"%s"' % id for id in tournment_id])
    params = {
        "params": '{"start_date":"%s","end_date":"%s","bet_count":3,"include_meta":true,"id_tournament":[%s],"delivery_platform":"Web","company_uuid":"7defd1e3-cbe8-42d5-b96e-0757f8ac90e0"}'
        % (init_date, end_date, ids),
        "dataFormat": '{"default":"object","sports":"object","categories":"object","tournaments":"object","matches":"array","betGroups":"array"}',
        "language": '{"default":"en"}',
        "dataShrink": "true",
        "cacheRedirect": "1",
    }
    return params


competition_urls = {
    "football": {
        "bundesliga": "fa25da39-ff29-4a0e-935c-4b950ecada50",
        "ligue1": "fcf566bb-a318-4e64-9057-e198ff3d2d4c",
        "liga": "5b96d89e-c8cc-4ef5-aca7-eb3494c28b3a",
        "premier-league": "620490dd-916c-406a-8c74-e7dbeb9dae2b",
        "serie-a": "2ecf42af-e560-434e-8928-b534ac09b04d",
        "primeira": "267f66fe-29d2-445a-8b94-2406f8fdbd18",
        "mls": "afadfc9f-686e-4aa5-a3b0-e80458159990",
        "champions": [
            "8dddea21-3ef7-406e-8aa1-2e25aaba91d3",
            "d6bb01fb-c05d-4f91-8e97-27b3ed1a85b9",
            "52fd6a09-687a-49f3-b8a0-db72319f6791",
            "c0cd450c-5867-4e21-9140-74d5e644f618",
            "4cb946fe-4c35-42c2-a49b-d8cf5136ee76",
            "731ebdbb-1748-48c8-90c1-c84e548518a4",
            "cd2971cf-28a4-4750-b8e0-f1ba7721db39",
            "22f4abb4-a0ef-4fad-baaf-e48eb3a12334",
        ],
        "uefa": [
            "2c779528-c87e-404d-9508-e31785c2953b",
            "6c2d227e-b23a-410f-9b06-7cb7dcb9901f",
            "32a3a445-d1a9-41f2-a56b-d4a04ea85923",
            "c78f5af8-20ac-4290-948c-62375350f4e6",
            "96244be8-7f25-43b3-a78e-a18be763112d",
            "59fa0436-fe4b-4342-ab8e-22e24ce49d47",
            "b342cb51-143b-4d59-936f-bd9376374976",
            "56679222-ba42-4f33-8627-97f2f5f367f5",
        ],
        "eredivise": "ba4f083f-4c9a-40b0-bd36-41e9ebe67305",
        "chile": "b9558e2f-d158-492c-a232-ae18ef727fbb",
        "serie-a-brasil": "3d2e9f8c-30bc-495a-8d58-af18da971b0e",
        "arabia": "c3f9ed44-0e30-44e4-b8cc-703931689409",
        "bundesliga-austria": "f96d7b5f-d82e-4e6b-949b-0e48f540986c",
        "super-lig": "87c17cfc-45c2-4f16-892e-eae8e0b274b8",
        "poland": "a153b093-3388-49e8-8a02-777650cceb75",
        "czech": "c4f0ec8b-1a08-485a-a71a-655cac3b85c1",
        "colombia": "e4753884-8c53-433d-8130-cbab5c60e852",
        "division-1a": "10453212-38dc-4f57-94d7-0a4ae78b2685",
        "belarus": "c1b2015d-0686-47be-848b-e982e93b8043",
        "russia": "915453b3-1cb7-4192-9b97-f16fc48cfd3a",
    },
    "basketball": {
        # "nba": 3,
        # "euroleague": "https://www.betclic.fr/basket-ball-s4/euroligue-c14",
    },
    "tennis": {
        # "us-open-men": get_url(3027),
    },
}


async def get_page(competition):
    url = "https://sports-mts-services-api.gb.nsoftcdn.com/prematchOffer/getMatches"
    if (
        competition["sport"] in competition_urls
        and competition["competition"] in competition_urls[competition["sport"]]
    ):
        id = competition_urls[competition["sport"]][competition["competition"]]
        params = get_params(id)
    else:
        return None
    async with get_session().get(
        url,
        headers=headers,
        params=params,
    ) as response:
        response = await response.json()
    return response


async def get_games(competition):
    response = await get_page(competition)
    if response is None:
        return None

    data = response["m"]
    if len(data) == 0:
        return None
    games = []
    for event in data:
        team1 = None
        team2 = None
        participants = event["k"]
        for p in participants:
            if int(p["e"]) == 1:
                team1 = p["b"]
            if int(p["e"]) == 2:
                team2 = p["b"]
        markets = event["l"]

        if team1 is None or team2 is None:
            continue

        for market in markets:
            first = None
            second = None
            third = None
            if market["n"] == "Three  Way":
                for odd in market["i"]:
                    if odd["c"] == "1":
                        first = odd["g"]
                    elif odd["c"] == "X":
                        second = odd["g"]
                    elif odd["c"] == "2":
                        third = odd["g"]
                # first = market["i"][0]["g"]
                # second = market["i"][1]["g"]
                # third = market["i"][2]["g"]
                if first and second and third:
                    odds = [float(first), float(second), float(third)]
                    games.append({"team1": team1, "team2": team2, "odds": odds})
                    break
    return games
