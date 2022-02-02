

class Summoner:
    def __init__(self, **kwargs):
        self._id = kwargs.get('summonerId')
        self.summonerName = kwargs.get('summonerName', None)
        self.leagueId = kwargs.get('leagueId', None)
        self.tier = kwargs.get('tier', None)
        self.rank = kwargs.get('rank', None)
        self.LeaguePoints = kwargs.get('LeaguePoints', None)
        self.wins = kwargs.get('wins', None)
        self.losses = kwargs.get('losses', None)
        self.veteran = kwargs.get('veteran', None)
        self.inactive = kwargs.get('inactive', None)
        self.freshBlood = kwargs.get('freshBlood', None)
        self.hotStreak = kwargs.get('hotStreak', None)

        self.match_crawled = kwargs.get('match_crawled', False)
        self.league_page = kwargs.get('match_crawled', 1)

    def as_dict(self):
        return self.__dict__


class Match:
    def __init__(self, json):
        self.json = json

    @property
    def _id(self):
        return self.json['metadata']['matchId']

    def as_dict(self):
        return dict(self.json, _id=self._id)