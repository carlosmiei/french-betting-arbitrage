import bookmakers.winamax as winamax
import bookmakers.pmu as pmu
import bookmakers.betclic as betclic
import bookmakers.zebet as zebet
import bookmakers.netbet as netbet
import bookmakers.ps3838 as ps3838
import arb
import sys
import log
import config

# print(ps3838.get_games({'competition': 'nba', 'sport': 'basketball'}))
# exit(0)
log.init()

progress = 0
for competition in config.competitions:
	progress += 1
	bookmakers = {}
	try:
		bookmakers['winamax'] = winamax.get_games(competition)
		log.log("winamax: " + str(bookmakers['winamax']))
	except:
		log.log("Cannot crawl winamax: " + sys.exc_info()[0])
	try:
		bookmakers['pmu'] = pmu.get_games(competition)
		log.log("pmu: " + str(bookmakers['pmu']))
	except:
		log.log("Cannot crawl pmu: " + sys.exc_info()[0])
	try:
		bookmakers['betclic'] = betclic.get_games(competition)
		log.log("betclic: " + str(bookmakers['betclic']))
	except:
		log.log("Cannot crawl betclic: " + sys.exc_info()[0])
	try:
		bookmakers['zebet'] = zebet.get_games(competition)
		log.log("zebet: " + str(bookmakers['zebet']))
	except:
		log.log("Cannot crawl zebet: " + sys.exc_info()[0])
	try:
		bookmakers['netbet'] = netbet.get_games(competition)
		log.log("netbet: " + str(bookmakers['netbet']))
	except:
		log.log("Cannot crawl netbet: " + sys.exc_info()[0])
	try:
		bookmakers['ps3838'] = ps3838.get_games(competition)
		log.log("ps3838: " + str(bookmakers['ps3838']))
	except:
		log.log("Cannot crawl ps3838: " + sys.exc_info()[0])
	log.log("-- Competition: {} --".format(competition))
	for game in bookmakers['winamax']:
		games = {}
		for bookmaker in bookmakers:
			try:
				g = arb.get_game(game, bookmakers[bookmaker])
				if (g):
					games[bookmaker] = g
			except:
				log.log("Error while retrieving games: {}".format(sys.exc_info()[0]))
		if (competition["sport"] == "football"):
			arb.arb_football(games)
		if (competition["sport"] == "basketball"):
			arb.arb_basketball(games)
	print("Progess: {:.2f}%".format(progress / len(config.competitions) * 100))