# by: iElden


APEX_TIERS = ['MASTER', 'GRANDMASTER', 'CHALLENGER']
NON_APEX_TIERS = ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND']
TIERS = NON_APEX_TIERS + APEX_TIERS
DIVS = ['IV', 'III', 'II', 'I']

class Summoner:
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id', None) or kwargs.get('summonerId')
        self.puuid = kwargs.get('puuid', None)
        self.summonerName = kwargs.get('summonerName', None) or kwargs.get('name', None)
        self.leagueId = kwargs.get('leagueId', None)
        self.tier = kwargs.get('tier', None)
        self.rank = kwargs.get('rank', None)
        self.leaguePoints = kwargs.get('leaguePoints', None)
        self.wins = kwargs.get('wins', None)
        self.losses = kwargs.get('losses', None)
        self.veteran = kwargs.get('veteran', None)
        self.inactive = kwargs.get('inactive', None)
        self.freshBlood = kwargs.get('freshBlood', None)
        self.hotStreak = kwargs.get('hotStreak', None)

        self.match_crawled = kwargs.get('match_crawled', False)
        self.league_page = kwargs.get('league_page', 1)

    @property
    def id(self):
        return self._id

    def as_dict(self):
        return self.__dict__


class Match:
    def __init__(self, json):
        self.json = json

    def __getitem__(self, item):
        return self.json[item]

    @property
    def _id(self):
        return self.json['metadata']['matchId']

    def as_dict(self):
        return dict(self.json, _id=self._id)