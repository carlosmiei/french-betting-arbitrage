from difflib import SequenceMatcher
import log
from itertools import permutations
from itertools import product
import time
import cache

mismatch_pairs = [
    ["MelbourneCity", "MelbourneVictory"],
    ["MelbourneCityFC", "MelbourneVictoryFC"],
]


def str_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def get_game(game, others):
    if len(others) == 0 or game == None:
        return None
    m = 0
    m_obj = None
    for other in others:
        sim = str_similarity(game["team1"], other["team1"]) + str_similarity(
            game["team2"], other["team2"]
        )
        if sim > m:
            m = sim
            m_obj = other
    if m_obj is None:
        return None
    if str_similarity(game["team1"], m_obj["team1"]) < 0.81:
        return None
    if str_similarity(game["team2"], m_obj["team2"]) < 0.81:
        return None
    for mismatch in mismatch_pairs:
        if [game["team1"], m_obj["team1"]] == mismatch or [
            m_obj["team1"],
            game["team1"],
        ] == mismatch:
            return None
        if [game["team2"], m_obj["team2"]] == mismatch or [
            m_obj["team2"],
            game["team2"],
        ] == mismatch:
            return None
    return m_obj


def arb3(a, n, b):
    return (1 - (1 / a + 1 / n + 1 / b)) * 100


def arb2(a, b):
    return (1 - (1 / a + 1 / b)) * 100


def dec_to_base(num, base):
    base_num = ""
    while num > 0:
        dig = int(num % base)
        if dig < 10:
            base_num += str(dig)
        else:
            base_num += chr(ord("A") + dig - 10)
        num //= base
    base_num = base_num[::-1]
    return base_num


def complete_check(games):
    nb_bookmakers = len(games)
    # combinations = nb_bookmakers**3
    comb = list(product(list(games.keys()), repeat=3))
    for i, (b1, b2, b3) in enumerate(comb):
        combination = str(dec_to_base(i, nb_bookmakers)).zfill(3)
        # b1 = list(games.keys())[int(combination[0])]
        # b2 = list(games.keys())[int(combination[1])]
        # b3 = list(games.keys())[int(combination[2])]
        profit = arb3(
            games[b1]["odds"][0],
            games[b2]["odds"][1],
            games[b3]["odds"][2],
        )
        if profit > 0:
            stakes = get_stakes3(
                games[b1]["odds"][0], games[b2]["odds"][1], games[b3]["odds"][2], 10
            )

            log.log("FOUND!!!!")
            message = "Abritrage found for [{}-{}] with [{}/{}/{}] with odds [{}/{}/{}]: {:.2f}%".format(
                games[b1]["team1"],
                games[b1]["team2"],
                b1,
                b2,
                b3,
                games[b1]["odds"][0],
                games[b2]["odds"][1],
                games[b3]["odds"][2],
                profit,
            )
            if message not in cache:
                stake_message = "> Stakes: **{}**@{} on {} for A, **{}**@{} on {} for N, **{}**@{} on {} for B".format(
                    stakes["rounded"][0],
                    games[b1]["odds"][0],
                    b1,
                    stakes["rounded"][1],
                    games[b2]["odds"][1],
                    b2,
                    stakes["rounded"][2],
                    games[b3]["odds"][2],
                    b3,
                )
                cache.append(message)
                log.discord(message)
                log.discord(stake_message)
                log.log(message)
                log.log(stake_message)
            else:
                log.log(f"Duplicated opportunity, cache length: {len(cache)}")
            log.log(
                "{}: ({:10}/{:10}/{:10}) {:.2f}%".format(
                    " ".join(combination.split()), b1, b2, b3, profit
                )
            )


def optimized_check(games):
    games_with_bookmarker = [
        {"bookmarker": key, **value} for key, value in games.items()
    ]

    repeated_opportunities = []
    old_opportunities = []
    comb = list(product(list(games.keys()), repeat=3))
    for _i, (b1, b2, b3) in enumerate(comb):
        t1 = games[b1]["team1"]
        t2 = games[b1]["team2"]
        key = f"{t1}-{t2}-{b1}-{b2}-{b3}"
        entry = cache.get_cache_entry(t1, t2, b1, b2, b3)
        if entry is not None:
            profits = list(entry.keys())
            for profit in profits:
                value = cache.get_cache_entry(t1, t2, b1, b2, b3, profit)
                if value["active"]:
                    old_opportunities.append(value)

    N = 2
    best_first_odds = sorted(
        games_with_bookmarker, key=lambda x: x["odds"][0], reverse=True
    )[:N]
    best_second_odds = sorted(
        games_with_bookmarker, key=lambda x: x["odds"][1], reverse=True
    )[:N]
    best_third_odds = sorted(
        games_with_bookmarker, key=lambda x: x["odds"][2], reverse=True
    )[:N]

    for first_team in best_first_odds:
        if "active" in first_team and first_team["active"] == False:
            continue
        b1 = first_team["bookmarker"]
        for second_team in best_second_odds:
            if "active" in second_team and second_team["active"] == False:
                continue
            b2 = second_team["bookmarker"]
            for third_team in best_third_odds:
                b3 = third_team["bookmarker"]

                odds1 = first_team["odds"][0]
                odds2 = second_team["odds"][1]
                odds3 = third_team["odds"][2]

                team1 = first_team["team1"]
                team2 = second_team["team2"]

                profit = arb3(odds1, odds2, odds3)
                profit = round(profit, 3)
                if profit > 0.6:
                    # stakes = get_stakes3(odds1, odds2, odds3, 10)
                    # log.log("FOUND!!!!")
                    message = "Abritrage found for [{}-{}] with [{}/{}/{}] with odds [{}/{}/{}]: {:.2f}%".format(
                        team1,
                        team2,
                        b1,
                        b2,
                        b3,
                        odds1,
                        odds2,
                        odds3,
                        profit,
                    )
                    prev_op = cache.get_cache_entry(team1, team2, b1, b2, b3, profit)

                    if prev_op is None:
                        cache.save_to_cache(
                            team1, team2, b1, b2, b3, profit, [odds1, odds2, odds3]
                        )
                        log.discord(message)
                        log.log(message)
                    else:
                        repeated_opportunities.append(
                            f"{team1}-{team2}-{b1}-{b2}-{b3}-{profit}"
                        )
                    log.log("({:10}/{:10}/{:10}) {:.2f}%".format(b1, b2, b3, profit))

    detect_opportunities_gone(old_opportunities, repeated_opportunities, games)


def detect_opportunities_gone(old_opportunities, repeated_opportunities, games):
    # detect missing opportunities since the last run
    for old in old_opportunities:  # {t1,t2,b1,b2,b3, init_time, profit}
        key = f"{old['t1']}-{old['t2']}-{old['b1']}-{old['b2']}-{old['b3']}"
        key_with_profit = f"{key}-{old['profit']}"
        if key_with_profit not in repeated_opportunities:
            init = old["init_time"]
            now = round(time.time())
            elapsed = now - init
            # get current odds:
            b1_odds = games[old["b1"]]["odds"]
            b2_odds = games[old["b2"]]["odds"]
            b3_odds = games[old["b3"]]["odds"]
            odds = [b1_odds[0], b2_odds[1], b3_odds[2]]
            profit_on_close = round(arb3(odds[0], odds[1], odds[2]), 3)
            cache.close_opportunity(
                old["t1"],
                old["t2"],
                old["b1"],
                old["b2"],
                old["b3"],
                old["profit"],
                now,
                elapsed,
                odds,
                profit_on_close,
            )
            log.discord(
                f"[Gone] [{old['t1']}-{old['t2']}] [{old['b1']}/{old['b2']}/{old['b3']}] Initial profit: {old['profit']:.2}% Profit on close: {profit_on_close:.2}% gone after ({elapsed:.2f} seconds. Initial odds: {old['init_odds']}, current odds: {odds}"
            )
        # else:
        #     # log.log(f"Opportunity {key_with_profit} is still active")
        #     pass


def arb_football(games):
    nb_bookmakers = len(games)
    if nb_bookmakers == 1:
        return
    combinations = nb_bookmakers**3
    log.log("-- Arbitrage on:")
    for game in games:
        try:
            log.log(
                "{:10}: {} - {} @{}/{}/{}".format(
                    game,
                    games[game]["team1"],
                    games[game]["team2"],
                    games[game]["odds"][0],
                    games[game]["odds"][1],
                    games[game]["odds"][2],
                )
            )
        except:
            log.log(f"Error while logging game: {game}")
    log.log("{} combinations possible --".format(combinations))
    optimized_check(games)
    # complete_check(games)


def arb_basketball(games):
    nb_bookmakers = len(games)
    if nb_bookmakers == 1:
        return
    combinations = nb_bookmakers**2
    log.log("-- Arbitrage on: ")
    for game in games:
        log.log(
            "{:10}: {} - {} @{}/{}".format(
                game,
                games[game]["team1"],
                games[game]["team2"],
                games[game]["odds"][0],
                games[game]["odds"][1],
            )
        )
    log.log("{} combinations possible --".format(combinations))
    for i in range(combinations):
        combination = str(dec_to_base(i, nb_bookmakers)).zfill(2)
        b1 = list(games.keys())[int(combination[0])]
        b2 = list(games.keys())[int(combination[1])]
        profit = arb2(
            games[b1]["odds"][0],
            games[b2]["odds"][1],
        )
        profit = round(profit, 3)
        if profit > 0.8:
            log.log("FOUND!!!!")
            # stakes = get_stakes2(games[b1]["odds"][0], games[b2]["odds"][1], 10)
            log.discord(
                "Abritrage found for **{}**-**{}** with **{}/{}** with odds {}/{}: {:.2f}%".format(
                    games[b1]["team1"],
                    games[b1]["team2"],
                    b1,
                    b2,
                    games[b1]["odds"][0],
                    games[b2]["odds"][1],
                    profit,
                )
            )
            # log.discord(
            #     "> Stakes: **{}**@{} on {} for A, **{}**@{} on {} for B".format(
            #         stakes["rounded"][0],
            #         games[b1]["odds"][0],
            #         b1,
            #         stakes["rounded"][1],
            #         games[b2]["odds"][1],
            #         b2,
            #     )
            # )

            log.log(
                "{}: ({:10}/{:10}) {:.2f}%".format(
                    " ".join(combination.split()), b1, b2, profit
                )
            )


def get_stakes3(a, n, b, investment):
    amount = arb3(a, n, b)
    tmp = (100 - amount) / 100
    return {
        "raw": (investment / (tmp * a), investment / (tmp * n), investment / (tmp * b)),
        "rounded": (
            round(investment / (tmp * a) * 10) / 10,
            round(investment / (tmp * n) * 10) / 10,
            round(investment / (tmp * b) * 10) / 10,
        ),
    }


def get_stakes2(a, b, investment):
    amount = arb2(a, b)
    tmp = (100 - amount) / 100
    return {
        "raw": (investment / (tmp * a), investment / (tmp * b)),
        "rounded": (
            round(investment / (tmp * a) * 10) / 10,
            round(investment / (tmp * b) * 10) / 10,
        ),
    }
