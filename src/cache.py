import time
import json
import os

filename = "cache.json"

cache_info = {}


def load():
    global cache_info
    if not os.path.exists(filename):
        with open(filename, "w") as file:
            file.write("{}")
            return
    try:
        with open(filename, "r") as file:
            cache_info = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_file():
    with open(filename, "w") as f:
        f.write(json.dumps(cache_info))


def delete_entry(key, profit):
    global cache_info
    if key in cache_info:
        if cache_info[key][0] == profit:
            del cache_info[key]
            save_file()


def get_cache_opportunities(t1, t2):
    keys = list(cache_info.keys())
    res = []
    for key in keys:
        if t1 in key and t2 in key:
            res.append([key, cache_info[key]])
    return res


def get_cache_entry(t1, t2, b1, b2, b3, profit=None):
    key = f"{t1}-{t2}-{b1}-{b2}-{b3}"
    if key in cache_info:
        if profit is not None and str(profit) in cache_info[key]:
            return cache_info[key][str(profit)]
        return cache_info[key]
    return None


def save_to_cache(team1, team2, b1, b2, b3, profit, init_odds):
    global cache_info
    key = f"{team1}-{team2}-{b1}-{b2}-{b3}"
    now = round(time.time())
    if key not in cache_info:
        cache_info[key] = {}

    cache_info[key][str(profit)] = {
        "profit": profit,
        "init_time": now,
        "init_date": time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(now)),
        "active": True,
        "t1": team1,
        "t2": team2,
        "b1": b1,
        "b2": b2,
        "b3": b3,
        "init_odds": init_odds,
    }
    save_file()


def close_opportunity(t1, t2, b1, b2, b3, profit, end, duration, odds, profit_on_close):
    key = f"{t1}-{t2}-{b1}-{b2}-{b3}"
    profit_str = str(profit)
    if key in cache_info:
        if profit_str in cache_info[key]:
            cache_info[key][profit_str]["end_odds"] = odds
            cache_info[key][profit_str]["profit_on_close"] = profit_on_close
            cache_info[key][profit_str]["active"] = False
            cache_info[key][profit_str]["end_time"] = end
            cache_info[key][profit_str]["end_date"] = time.strftime(
                "%d/%m/%Y %H:%M:%S", time.localtime(end)
            )
            cache_info[key][profit_str]["duration"] = round(duration, 2)
            if "closed" not in cache_info:
                cache_info["closed"] = []

            cache_info["closed"].append(cache_info[key][profit_str])
            del cache_info[key][profit_str]
            keys = list(cache_info[key].keys())
            if len(keys) == 0:
                del cache_info[key]
            save_file()
            return True
    return False
