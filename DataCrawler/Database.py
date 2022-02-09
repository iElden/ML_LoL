import pymongo.errors
from pymongo import MongoClient
from typing import List, Generator, Tuple, Iterator

from .DbModel import Summoner, Match

class Database(MongoClient):

    DB = 'SoloQ'

    def __init__(self):
        super().__init__("mongodb://127.0.0.1:27017")

    def is_match_in_database(self, match_id : str):
        r = self[self.DB]['match'].find_one({'_id': match_id})
        return r is not None

    def is_summoner_in_database_by_summoner_id(self, summoner_id : str) -> bool:
        r = self[self.DB]['summoner'].find_one({'_id': summoner_id})
        return r is not None

    def is_summoner_in_database_by_summoner_puuid(self, puuid):
        ...

    def edit_summoner(self, summoner : Summoner) -> None:
        self[self.DB]['summoner'].find_one_and_replace({'_id': summoner.id}, summoner.as_dict())

    def get_all_summoner(self) -> List[Summoner]:
        r = self[self.DB]['summoner'].find({})
        return [Summoner(**i) for i in r]

    def get_all_summoner_without_puuid(self) -> List[Summoner]:
        r = self[self.DB]['summoner'].find({'puuid': {'$exists': False}})
        return [Summoner(**i) for i in r]

    def get_all_summoner_with_match_uncrawled(self, page_min : int=1, page_max : int=100) -> List[Summoner]:
        r = self[self.DB]['summoner'].find({'match_crawled': False, 'league_page': {'$gte':page_min, '$lte' : page_max} })
        return [Summoner(**i) for i in r]

    def get_all_summoner_with_crawled_match(self, limit=0) -> Iterator[Summoner]:
        r = self[self.DB]['summoner'].find({'match_crawled': True}).limit(limit)
        return (Summoner(**i) for i in r)

    def database_already_have_tier(self, tier : str) -> bool:
        r = self[self.DB]['summoner'].find_one({'tier': tier})
        return r is not None

    def database_already_have_page(self, tier, rank, league_page) -> bool:
        r = self[self.DB]['summoner'].find_one({'tier': tier, 'rank': rank, 'league_page': league_page})
        return r is not None

    def get_match_for_summoner(self, summoner : Summoner, limit : int=20, debug_index=None) -> List[Match]:
        if debug_index is not None and debug_index % 50 == 0:
            print(f"Summoners requested : {debug_index}")
        r = self[self.DB]['match'].find({"metadata.participants": summoner.puuid}).limit(limit)
        return [Match(i) for i in r]

    def get_all_histories(self, match_limit : int=20, summoner_limit : int=4000) -> Iterator[Tuple[Summoner, List[Match]]]:
        summoners = self.get_all_summoner_with_crawled_match(limit=summoner_limit)
        return ((s, self.get_match_for_summoner(s, limit=match_limit, debug_index=i)) for i, s in enumerate(summoners))

    def insert_match(self, match : Match):
        try:
            self[self.DB]['match'].insert(match.as_dict())
        except pymongo.errors.DuplicateKeyError:
            print("WARNING: Tryed to push match that already exist in db")
            pass

    def insert_summoner(self, summoner : Summoner) -> None:
        try:
            self[self.DB]['summoner'].insert(summoner.as_dict())
        except pymongo.errors.DuplicateKeyError:
            pass
