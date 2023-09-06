import bookmakers.winamax as winamax
import bookmakers.pmu as pmu
import bookmakers.betclic as betclic
import bookmakers.zebet as zebet
import bookmakers.netbet as netbet
import bookmakers.ps3838 as ps3838
import bookmakers.stake as stake
import bookmakers.freshbet as freshbet
import bookmakers.jackbit as jackbit
import bookmakers.betplay as betplay
import bookmakers.trustdice as trustdice
import bookmakers.sportsbetio as sportsbetio
import bookmakers.kineko as kineko
import arb
import sys
import log
import config
import traceback
import time
import asyncio

log.init()


def is_valid_game(game):
    try:
        cond = (
            game is not None
            and game["odds"][0] > 1
            and game["odds"][1] > 1
            and game["odds"][2] > 1
            and game["team1"] is not None
            and game["team2"] is not None
        )
        return cond
    except:
        return False


async def get_competition_games(name, exchange, competition):
    try:
        res = await exchange.get_games(competition)
        log.log(name + ": " + str(res))
        return [name, res]
    except:
        log.log(f"Cannot crawl {name}: " + traceback.format_exc())
    return None


async def check_competition(competition):
    log.log("Checking competition: {}".format(competition))
    print("Checking competition: {}".format(competition))
    results = await asyncio.gather(
        get_competition_games("kineko", kineko, competition),
        get_competition_games("sportsbetio", sportsbetio, competition),
        get_competition_games("trustdice", trustdice, competition),
        get_competition_games("betplay", betplay, competition),
        get_competition_games("jackbit", jackbit, competition),
        get_competition_games("freshbet", freshbet, competition),
        get_competition_games("stake", stake, competition),
    )
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
    if most_games_bookmarker is None:
        log.log(f"No games found for this competition: {competition}, skipping!")
        return
    for game in bookmakers[most_games_bookmarker]:
        games = {}
        for bookmaker in bookmakers:
            try:
                g = arb.get_game(game, bookmakers[bookmaker])
                if is_valid_game(g):
                    games[bookmaker] = g
                else:
                    log.log(f"[{bookmaker}][{competition}] Invalid game, skipping: {g}")
            except:
                log.log(
                    "Error while retrieving games: {}".format(traceback.format_exc())
                )
        if competition["sport"] == "football":
            arb.arb_football(games)
        if competition["sport"] == "basketball":
            arb.arb_basketball(games)


async def start():
    # progress = 0
    tasks = []
    for competition in config.competitions:
        tasks.append(check_competition(competition))
    await asyncio.gather(*tasks)


async def main():
    while True:
        try:
            before = time.time()
            print("Will start a new check")
            await start()
            after = time.time()
            print("Check finished in {:.2f} seconds".format(after - before))
        except:
            log.log("Final Error: {}".format(traceback.format_exc()))
        time.sleep(10)


asyncio.run(main())
