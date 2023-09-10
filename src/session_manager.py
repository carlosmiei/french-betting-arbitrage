import aiohttp
from aiohttp_proxy import ProxyConnector, ProxyType
import random

proxies = [
    "http://koDbkTmF2l7boOp:kN2Fa6BHPGw0QCt@88.216.186.6:43432",
    "http://tgc6nN40m7thSXH:0l3pXaoc6VEoBzv@88.216.186.11:42556",
    "http://hEs5vN4OJKijbhC:XAIIU11ZAdkzRFG@87.248.158.23:42911",
    "http://O8hZf9yUdXX06SW:V0huuTfOoOdMMFr@87.248.158.35:41216",
    "http://3lHLuu3YLKXYMr4:NcJHUdDWAfOUTr4@87.248.158.66:45222",
]  # uk proxies


germany_proxies = [
    # None,  # vps ip also germany
    "http://ZQWbdwfub5DGua7:sUb3WKbjvxUHsmb@185.173.26.41:41164",
    "http://vM0hvFlg4VL6iuI:DMuhSI9nPVBXiIC@185.173.26.61:48656",
]

session = None
german_session = None


def get_session():
    return session


def get_german_session():
    return german_session


def set_german_session():
    global german_session
    proxy = germany_proxies[random.randint(0, len(germany_proxies) - 1)]
    if german_session is None:
        if proxy is None:
            s = aiohttp.ClientSession()
        else:
            s = aiohttp.ClientSession(connector=ProxyConnector.from_url(proxy))
        german_session = s


def set_session(proxy=None):
    global session
    if session is None or proxy is not None:
        if proxy is None:
            s = aiohttp.ClientSession()
        else:
            s = aiohttp.ClientSession(connector=ProxyConnector.from_url(proxy))
        session = s


async def close_session():
    global session
    global german_session
    if session is not None:
        await session.close()
        session = None
    if german_session is not None:
        await german_session.close()
        german_session = None
