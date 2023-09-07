from bs4 import BeautifulSoup
import requests
import json
import aiohttp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import asyncio
from selenium.webdriver.common.by import By

competition_urls = {
    "football": {
        "bundesliga": "https://sports.chipstars.bet/2dc4094d-74cb-44f0-8e70-675fa2c0a490/prematch/matches?period=0&tournamentId=4261&isTournament=false&stakeTypes=1&stakeTypes=702&stakeTypes=2&stakeTypes=3&stakeTypes=37&langId=2&partnerId=492&countryCode=GB",
        "ligue1": "https://sports.chipstars.bet/2dc4094d-74cb-44f0-8e70-675fa2c0a490/prematch/matches?period=0&tournamentId=4610&isTournament=false&stakeTypes=1&stakeTypes=702&stakeTypes=2&stakeTypes=3&stakeTypes=37&langId=2&partnerId=492&countryCode=GB",
        "liga": "https://sports.chipstars.bet/2dc4094d-74cb-44f0-8e70-675fa2c0a490/prematch/matches?period=0&tournamentId=4486&isTournament=false&stakeTypes=1&stakeTypes=702&stakeTypes=2&stakeTypes=3&stakeTypes=37&langId=2&partnerId=492&countryCode=GB",
        "premier-league": "https://sports.chipstars.bet/2dc4094d-74cb-44f0-8e70-675fa2c0a490/prematch/matches?period=0&tournamentId=4485&isTournament=false&stakeTypes=1&stakeTypes=702&stakeTypes=2&stakeTypes=3&stakeTypes=37&langId=2&partnerId=492&countryCode=GB",
        "serie-a": "https://sports.chipstars.bet/2dc4094d-74cb-44f0-8e70-675fa2c0a490/prematch/matches?period=0&tournamentId=4484&isTournament=false&stakeTypes=1&stakeTypes=702&stakeTypes=2&stakeTypes=3&stakeTypes=37&langId=2&partnerId=492&countryCode=GB",
        "primeira": "https://sports.chipstars.bet/2dc4094d-74cb-44f0-8e70-675fa2c0a490/prematch/matches?period=0&tournamentId=4565&isTournament=false&stakeTypes=1&stakeTypes=702&stakeTypes=2&stakeTypes=3&stakeTypes=37&langId=2&partnerId=492&countryCode=GB",
        "serie-a-brasil": "https://sports.chipstars.bet/2dc4094d-74cb-44f0-8e70-675fa2c0a490/prematch/matches?period=0&tournamentId=5566&isTournament=false&stakeTypes=1&stakeTypes=702&stakeTypes=2&stakeTypes=3&stakeTypes=37&langId=2&partnerId=492&countryCode=GB",
        "bundesliga-austria": "https://sports.chipstars.bet/2dc4094d-74cb-44f0-8e70-675fa2c0a490/prematch/matches?period=0&tournamentId=39659&isTournament=false&stakeTypes=1&stakeTypes=702&stakeTypes=2&stakeTypes=3&stakeTypes=37&langId=2&partnerId=492&countryCode=GB",
        "division-1a": "https://sports.chipstars.bet/2dc4094d-74cb-44f0-8e70-675fa2c0a490/prematch/matches?period=0&tournamentId=4550&isTournament=false&stakeTypes=1&stakeTypes=702&stakeTypes=2&stakeTypes=3&stakeTypes=37&langId=2&partnerId=492&countryCode=GB",
    },
    "basketball": {
        "nba": "https://sports.chipstars.bet/2dc4094d-74cb-44f0-8e70-675fa2c0a490/prematch/matches?period=0&tournamentId=998&isTournament=false&stakeTypes=1&stakeTypes=702&stakeTypes=2&stakeTypes=3&stakeTypes=37&langId=2&partnerId=492&countryCode=GB"
        # "nba": get_url(2980),
        # "euroleague": "https://www.betclic.fr/basket-ball-s4/euroligue-c14",
    },
    "tennis": {
        # "us-open-men": get_url(3027),
    },
}


async def get_page(competition):
    # async with aiohttp.ClientSession() as session:
    if (
        competition["sport"] in competition_urls
        and competition["competition"] in competition_urls[competition["sport"]]
    ):
        url = competition_urls[competition["sport"]][competition["competition"]]
    else:
        return None
    # async with session.get(
    #     url,
    #     headers={
    #         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    #     },
    # ) as response:
    #     response = await response.json()
    # return response
    options = Options()
    options.add_argument("--no-sandbox")
    # options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1, 1)
    driver.get(url)
    # await asyncio.sleep(5)
    page_source = driver.find_element(By.XPATH, "/html/body").text

    driver.quit()
    return json.loads(page_source)


async def get_games(competition):
    response = await get_page(competition)
    if response is None:
        return None
    game_elements = response["CNT"][0]["CL"][0]["E"]
    games = []
    for el in game_elements:
        try:
            # names = el.select(".betBox_contestantName")
            # team1 = "".join(names[0].text.split())
            # team2 = "".join(names[1].text.split())
            # odd_els = el.select(".oddValue")
            team1 = el["HT"]
            team2 = el["AT"]
            stake_types = el["StakeTypes"]
            for stake_type in stake_types:
                if stake_type["N"] == "Result":
                    inner_stakes = stake_type["Stakes"]
                    first = None
                    second = None
                    third = None
                    for inner_stake in inner_stakes:
                        if inner_stake["N"] == "Win1":
                            first = inner_stake["F"]
                        elif inner_stake["N"] == "X":
                            second = inner_stake["F"]
                        elif inner_stake["N"] == "Win2":
                            third = inner_stake["F"]

            if first and second and third and team1 and team2:
                odds = [float(first), float(second), float(third)]
                games.append({"team1": team1, "team2": team2, "odds": odds})
        except:
            continue
    return games
