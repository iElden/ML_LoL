import itertools
import asyncio
from typing import List

from .pantheon.pantheon.pantheon import Pantheon
from .Database import Database
from .DbModel import Summoner, NON_APEX_TIERS, DIVS
from .exc import AntiTeubeException

API_KEY_PATH = "DataCrawler/private/riot_api_key.txt"

class DataCrawler:
    def __init__(self):
        with open(API_KEY_PATH) as fd:
            _api_key = fd.read()
        self.pantheon = Pantheon('euw1', 'europe', api_key=_api_key, errorHandling=True)
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

    async def fetch_player_page_from_league(self, tier : str, division : str, page : int) -> List[Summoner]:
        if self.db.database_already_have_page(tier, division, page):
            raise AntiTeubeException(f'Database already have {tier} {division} page {page}')
        print(f"Get page {page} of {tier} {division}")
        r = await self.pantheon.getLeaguePages(queue="RANKED_SOLO_5x5", tier=tier, division=division, page=page)
        return [Summoner(**i, league_page=page) for i in r]

    async def add_player_page_range_for_league(self, tier : str, division : str, pages : range) -> None:
        tasks = [self.fetch_player_page_from_league(tier, division, i) for i in pages]
        r = await asyncio.gather(*tasks)
        for i in itertools.chain(*r):
            self.db.insert_summoner(i)

    async def add_players_from_all_leagues_in_pages(self, pages : range) -> None:
        for tier in NON_APEX_TIERS:
            for division in DIVS:
                print(f"Getting page for {pages} in League {tier} {division}")
                await self.add_player_page_range_for_league(tier, division, pages)