import pymongo.errors
from pymongo import MongoClient

from .DbModel import Summoner, Match

class Database(MongoClient):

    DB = 'SoloQ'

    def __init__(self):
        super().__init__("mongodb://127.0.0.1:27017")

    def is_match_in_database(self, match_id):
        ...

    def is_summoner_in_database_by_summoner_id(self, summoner_id : str) -> bool:
        r = self[self.DB]['summoner'].find_one({'_id': summoner_id})
        return r is not None

    def is_summoner_in_database_by_summoner_puuid(self, puuid):
        ...

    def database_already_have_tier(self, tier : str) -> bool:
        r = self[self.DB]['summoner'].find_one({'tier': tier})
        return r is not None

    def database_already_have_page(self, tier, rank, league_page) -> bool:
        r = self[self.DB]['summoner'].find_one({'tier': tier, 'rank': rank, 'league_page': league_page})
        return r is not None

    def insert_match(self, match : Match):
        try:
            self[self.DB]['match'].insert(match.as_dict())
        except pymongo.errors.DuplicateKeyError:
            pass

    def insert_summoner(self, summoner : Summoner) -> None:
        try:
            self[self.DB]['summoner'].insert(summoner.as_dict())
        except pymongo.errors.DuplicateKeyError:
            pass
