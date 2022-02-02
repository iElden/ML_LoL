import itertools

from .pantheon.pantheon.pantheon import Pantheon
from .Database import Database
from .DbModel import Summoner
from .exc import AntiTeubeException

API_KEY_PATH = "DataCrawler/private/riot_api_key.txt"

class DataCrawler:
    def __init__(self):
        with open(API_KEY_PATH) as fd:
            _api_key = fd.read()
        self.pantheon = Pantheon('euw1', 'europe', api_key=_api_key, errorHandling=False)
        self.db = Database()

    async def add_apex_players(self):
        if self.db.database_already_have_tier('CHALLENGER'):
            raise AntiTeubeException('A Challenger is already in the summoner database')
        challenger_league_json = await self.pantheon.getChallengerLeague('RANKED_SOLO_5x5')
        print(f"Got {len(challenger_league_json['entries'])} challenger_league_json entries")
        grandmaster_league_json = await self.pantheon.getGrandmasterLeague('RANKED_SOLO_5x5')
        print(f"Got {len(grandmaster_league_json['entries'])} grandmaster_league_json entries")
        master_league_json = await self.pantheon.getMasterLeague('RANKED_SOLO_5x5')
        print(f"Got {len(master_league_json['entries'])} master_league_json entries")
        challenger_summoner = (Summoner(**summoner_json, tier='CHALLENGER') for summoner_json in challenger_league_json['entries'])
        grandmaster_summoner = (Summoner(**summoner_json, tier='GRANDMASTER') for summoner_json in grandmaster_league_json['entries'])
        master_summoner = (Summoner(**summoner_json, tier='MASTER') for summoner_json in master_league_json['entries'])
        for i in itertools.chain(challenger_summoner, grandmaster_summoner, master_summoner):
            self.db.insert_summoner(i)