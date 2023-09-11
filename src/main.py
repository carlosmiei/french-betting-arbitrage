# import bookmakers.winamax as winamax
# import bookmakers.pmu as pmu
# import bookmakers.betclic as betclic
# import bookmakers.zebet as zebet
# import bookmakers.netbet as netbet
# import bookmakers.ps3838 as ps3838
import bookmakers.stake as stake
import bookmakers.freshbet as freshbet
import bookmakers.jackbit as jackbit
import bookmakers.betplay as betplay
import bookmakers.trustdice as trustdice

# import bookmakers.sportsbetio as sportsbetio
import bookmakers.kineko as kineko

# import bookmakers.chipstars as chipstars
import bookmakers.vave3 as vave3
import bookmakers.betsio as betsio
import bookmakers.jazz as jazz
import bookmakers.xbit1 as xbit1
import bookmakers.bet7 as bet7
import bookmakers.bitsler as bitsler
import bookmakers.thunderpick as thunderpick
import arb
import sys
import log
import config
import traceback
import time
import asyncio
import sys
import aiohttp
from session_manager import set_session, close_session, proxies, set_german_session

log.init()

# wolf.bet can be added but the API is confusing


session = None


def is_valid_game(game, sport):
    try:
        if sport == "football":
            cond = (
                game is not None
                and game["odds"][0] > 1
                and game["odds"][1] > 1
                and game["odds"][2] > 1
                and game["team1"] is not None
                and game["team2"] is not None
            )
            return cond
        else:
            cond = (
                game is not None
                and game["odds"][0] > 1
                and game["odds"][1] > 1
                and game["team1"] is not None
                and game["team2"] is not None
            )
            return cond
    except:
        return False


async def get_competition_games(name, exchange, competition):
    try:
        res = await exchange.get_games(competition)
        if res is None:
            return None
        log.log(name + ": " + str(res))
        return [name, res]
    except:
        log.log(f"Cannot crawl {name}: " + traceback.format_exc())
    return None


async def check_competition(competition):
    now = time.time()
    results = await asyncio.gather(
        get_competition_games("kineko", kineko, competition),
        get_competition_games("trustdice", trustdice, competition),
        get_competition_games("betplay", betplay, competition),
        get_competition_games("freshbet", freshbet, competition),
        get_competition_games("stake", stake, competition),
        get_competition_games("vave3", vave3, competition),
        get_competition_games("jazz", jazz, competition),
        get_competition_games("xbit1", xbit1, competition),
        get_competition_games("bitsler", bitsler, competition),
        get_competition_games("thunderpick", thunderpick, competition),
        get_competition_games("bet7", bet7, competition),
        get_competition_games("betsio", betsio, competition),
    )
    after = time.time()
    log.log(f"Got data from competition: {competition} took {after - now} seconds")
    # # # get_competition_games(
    # # #     "jackbit", jackbit, competition
    # # # ),  # exactly the same as freshbet
    # # # # get_competition_games(
    # # # #     "sportsbetio", sportsbetio, competition
    # # # # ),  # exactly the same as stake
    # # get_competition_games("chipstars", chipstars, competition),  # requires seleniumk

    bookmakers = {}
    for result in results:
        if result is None:
            continue
        name = result[0]
        res = result[1]
        bookmakers[name] = res
    log.log("-- Competition: {} --".format(competition))
    most_games_bookmarker = None
    for bookmaker in bookmakers.keys():
        if most_games_bookmarker is None or len(bookmakers[bookmaker]) > len(
            bookmakers[most_games_bookmarker]
        ):
            most_games_bookmarker = bookmaker
    if most_games_bookmarker is None or (bookmakers[most_games_bookmarker]) is None:
        log.log(f"No games found for this competition: {competition}, skipping!")
        return
    for game in bookmakers[most_games_bookmarker]:
        games = {}
        for bookmaker in bookmakers:
            try:
                g = arb.get_game(game, bookmakers[bookmaker])
                if is_valid_game(g, competition["sport"]):
                    games[bookmaker] = g
            except:
                log.log(
                    "Error while retrieving games: {}".format(traceback.format_exc())
                )
        if competition["sport"] == "football":
            arb.arb_football(games)
        if (
            competition["sport"] == "basketball"
            or competition["sport"] == "american-football"
        ):
            arb.arb_basketball(games)

    after_arb = time.time()
    log.log(f"Arbitrage calculation took {after_arb - after} seconds")


async def start():
    tasks = []
    for competition in config.competitions:
        tasks.append(check_competition(competition))
    await asyncio.gather(*tasks)


async def main():
    sleep = 60
    if len(sys.argv) > 1:
        sleep = int(sys.argv[1])
    print("Will sleep {} seconds between each check".format(sleep))
    i = 0
    proxies_number = len(proxies)
    while True:
        try:
            before = time.time()
            print("Will start a new check")
            proxy_number = i % proxies_number
            set_session(
                proxies[proxy_number]
            )  # use a different proxy on each iteration
            set_german_session()  # some exchanges require a german ip
            await start()
            await close_session()
            after = time.time()
            print("Check finished in {:.2f} seconds".format(after - before))
            i += 1
        except:
            log.log("Final Error: {}".format(traceback.format_exc()))
        time.sleep(sleep)


asyncio.run(main())
