import asyncio
from typing import Tuple

import sys
import json
from typing import List, Dict, Tuple, Any
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

from DataCrawler.DataCrawler import DataCrawler
from DataCrawler.Database import Database
from DataCrawler.DbModel import Match, Summoner

db = Database()

RANK_TO_CLASS = {
    ('IRON', 'IV'): 0,
    ('IRON', 'III'): 1,
    ('IRON', 'II'): 2,
    ('IRON', 'I'): 3,
    ('BRONZE', 'IV'): 4,
    ('BRONZE', 'III'): 5,
    ('BRONZE', 'II'): 6,
    ('BRONZE', 'I'): 7,
    ('SILVER', 'IV'): 8,
    ('SILVER', 'III'): 9,
    ('SILVER', 'II'): 10,
    ('SILVER', 'I'): 11,
    ('GOLD', 'IV'): 12,
    ('GOLD', 'III'): 13,
    ('GOLD', 'II'): 14,
    ('GOLD', 'I'): 15,
    ('PLATINUM', 'IV'): 16,
    ('PLATINUM', 'III'): 17,
    ('PLATINUM', 'II'): 18,
    ('PLATINUM', 'I'): 19,
    ('DIAMOND', 'IV'): 20,
    ('DIAMOND', 'III'): 21,
    ('DIAMOND', 'II'): 22,
    ('DIAMOND', 'I'): 23,
    ('MASTER', 'I'): 24,
    ('GRANDMASTER', 'I'): 25,
    ('CHALLENGER', 'I'): 26,
}

NB_GAMES = 20

cooldowns = {
    "1": 210,   # SummonerBoost      Cleanse"
    "3": 210,   # SummonerExhaust    Exhaust"
    "4": 300,   # SummonerFlash      Flash"
    "6": 210,   # SummonerHaste      Ghost"
    "7": 240,   # SummonerHeal       Heal"
    "11": 15,   # SummonerSmite      Smite"
    "12": 360,    # SummonerTeleport   Teleport"
    "13": 240,  # SummonerMana       Clarity"
    "14": 180,  # SummonerDot        Ignite"
    "21": 180,  # SummonerBarrier    Barrier"
    "30": 10,   # SummonerPoroRecall To the King!"
    "31": 20,   # SummonerPoroThrow  Poro Toss"
    "32": 80,   # SummonerSnowball   Mark"
    "39": 80,   # SummonerSnowURFSnowball_Mark     Mark
    "54": 1,    # Summoner_UltBookPlaceholder      Placeholder
    "55": 1,    # Summoner_UltBookSmitePlaceholder Placeholder and Attack-Smite
}

participant_all_fields = [
    "assists",
    "baronKills",
    "bountyLevel",
    "champExperience",
    "champLevel",
    "championId",
    "championName",
    "championTransform",
    "consumablesPurchased",
    "damageDealtToBuildings",
    "damageDealtToObjectives",
    "damageDealtToTurrets",
    "damageSelfMitigated",
    "deaths",
    "detectorWardsPlaced",
    "doubleKills",
    "dragonKills",
    "firstBloodAssist",
    "firstBloodKill",
    "firstTowerAssist",
    "firstTowerKill",
    "gameEndedInEarlySurrender",
    "gameEndedInSurrender",
    "goldEarned",
    "goldSpent",
    "individualPosition",
    "inhibitorKills",
    "inhibitorTakedowns",
    "inhibitorsLost",
    "item0",
    "item1",
    "item2",
    "item3",
    "item4",
    "item5",
    "item6",
    "itemsPurchased",
    "killingSprees",
    "kills",
    "lane",
    "largestCriticalStrike",
    "largestKillingSpree",
    "largestMultiKill",
    "longestTimeSpentLiving",
    "magicDamageDealt",
    "magicDamageDealtToChampions",
    "magicDamageTaken",
    "neutralMinionsKilled",
    "nexusKills",
    "nexusLost",
    "nexusTakedowns",
    "objectivesStolen",
    "objectivesStolenAssists",
    "participantId",
    "pentaKills",
    "perks",
    "physicalDamageDealt",
    "physicalDamageDealtToChampions",
    "physicalDamageTaken",
    "profileIcon",
    "puuid",
    "quadraKills",
    "riotIdName",
    "riotIdTagline",
    "role",
    "sightWardsBoughtInGame",
    "spell1Casts",
    "spell2Casts",
    "spell3Casts",
    "spell4Casts",
    "summoner1Casts",
    "summoner1Id",
    "summoner2Casts",
    "summoner2Id",
    "summonerId",
    "summonerLevel",
    "summonerName",
    "teamEarlySurrendered",
    "teamId",
    "teamPosition",
    "timeCCingOthers",
    "timePlayed",
    "totalDamageDealt",
    "totalDamageDealtToChampions",
    "totalDamageShieldedOnTeammates",
    "totalDamageTaken",
    "totalHeal",
    "totalHealsOnTeammates",
    "totalMinionsKilled",
    "totalTimeCCDealt",
    "totalTimeSpentDead",
    "totalUnitsHealed",
    "tripleKills",
    "trueDamageDealt",
    "trueDamageDealtToChampions",
    "trueDamageTaken",
    "turretKills",
    "turretTakedowns",
    "turretsLost",
    "unrealKills",
    "visionScore",
    "visionWardsBoughtInGame",
    "wardsKilled",
    "wardsPlaced",
    "win"
]
participant_fields = [
    "assists",
    "baronKills",
    "championId",
    "damageDealtToBuildings",
    "deaths",
    "detectorWardsPlaced",
    "dragonKills",
    "gameEndedInEarlySurrender",
    "gameEndedInSurrender",
    "individualPosition",
    "inhibitorsLost",
    "kills",
    "largestKillingSpree",
    "longestTimeSpentLiving",
    "sightWardsBoughtInGame",
    "summoner1Casts",
    "summoner1Id",
    "summoner2Casts",
    "summoner2Id",
    "teamEarlySurrendered",
    "timePlayed",
    "totalDamageDealt",
    "totalDamageTaken",
    "totalMinionsKilled",
    "totalTimeSpentDead",
    "turretsLost",
    "visionScore",
    "visionWardsBoughtInGame",
    "wardsKilled",
    "wardsPlaced",
    "win",
    "teamId"
]

info_all_fields = [
    "gameCreation",
    "gameDuration",
    "gameEndTimestamp",
    "gameId",
    "gameMode",
    "gameName",
    "gameStartTimestamp",
    "gameType",
    "gameVersion",
    "mapId",
    "participants",
    "platformId",
    "queueId",
    "teams",
    "tournamentCode"
]
info_fields = [
    "gameDuration",
    "teams",
]

ranksNames = [
    "Iron IV",
    "Iron III",
    "Iron II",
    "Iron I",
    "Bronze IV",
    "Bronze III",
    "Bronze II",
    "Bronze I",
    "Silver IV",
    "Silver III",
    "Silver II",
    "Silver I",
    "Gold IV",
    "Gold III",
    "Gold II",
    "Gold I",
    "Platinum IV",
    "Platinum III",
    "Platinum II",
    "Platinum I",
    "Diamond IV",
    "Diamond III",
    "Diamond II",
    "Diamond I",
    "Master",
    "Grandmaster",
    "Challenger"
]

def get_match(summoner, match):
    data = match['info']
    participant : Dict[str, Any] = [k for k in data["participants"] if k["puuid"] == summoner.puuid][0]
    realData = {i: k for i, k in participant.items() if i in participant_fields}
    for i in info_fields:
        realData[i] = data[i]
    return realData

def preprocess_match(match : Match, summoner : Summoner) -> dict:
    match_data = get_match(summoner, match)
    new_data = {}
    # Lvl6Time

    # Champion
    new_data["champion"] = match_data["championId"]
    # IsJgl
    new_data["is_jgl"] = match_data["individualPosition"] == "JUNGLE"
    # IsSupport
    new_data["is_sup"] = match_data["individualPosition"] == "UTILITY"
    # MatchLength
    new_data["game_len"] = match_data["gameDuration"]

    # assists/min
    new_data["assists"] = match_data["assists"] * 60 / match_data["gameDuration"]
    # deaths/min
    new_data["deaths"] = match_data["deaths"] * 60 / match_data["gameDuration"]
    # kills/min
    new_data["kills"] = match_data["kills"] * 60 / match_data["gameDuration"]
    # wardsKilled/min
    new_data["wards_killed"] = match_data["wardsKilled"] * 60 / match_data["gameDuration"]
    # wardsPlaced/min
    new_data["wards_placed"] = match_data["wardsPlaced"] * 60 / match_data["gameDuration"]
    # visionScore/min
    new_data["vision_score"] = match_data["visionScore"] * 60 / match_data["gameDuration"]
    # visionWardsBoughtInGame/min
    new_data["vision_wards_bought"] = match_data["visionWardsBoughtInGame"] * 60 / match_data["gameDuration"]
    # sightWardsBoughtInGame/min
    new_data["sight_wards_bought"] = match_data["sightWardsBoughtInGame"] * 60 / match_data["gameDuration"]
    # detectorWardsPlaced/min
    new_data["detector_wards_placed"] = match_data["detectorWardsPlaced"] * 60 / match_data["gameDuration"]
    # totalDamageDealt/min
    new_data["damage_dealt"] = match_data["totalDamageDealt"] * 60 / match_data["gameDuration"]
    # totalDamageTaken/min
    new_data["damage_taken"] = match_data["totalDamageTaken"] * 60 / match_data["gameDuration"]
    # totalMinionsKilled/min
    new_data["minions_killed"] = match_data["totalMinionsKilled"] * 60 / match_data["gameDuration"]
    # damageDealtToBuildings/min
    new_data["damage_to_buildings"] = match_data["damageDealtToBuildings"] * 60 / match_data["gameDuration"]
    # longestTimeSpentLiving in % of the game
    new_data["longest_time_alive"] = match_data["longestTimeSpentLiving"] * 60 / match_data["gameDuration"]
    # %game spent dead
    new_data["game_portion_dead"] = match_data["totalTimeSpentDead"] * 60 / match_data["gameDuration"]
    # summoner1 mean uptime
    new_data["summoner1_uptime"] = match_data["summoner1Casts"] / (match_data["gameDuration"] / cooldowns[str(match_data["summoner1Id"])])
    # summoner2 mean uptime
    new_data["summoner2_uptime"] = match_data["summoner2Casts"] / (match_data["gameDuration"] / cooldowns[str(match_data["summoner2Id"])])

    # baronKills
    new_data["baronKills"] = match_data["baronKills"]
    # dragonKills
    new_data["dragonKills"] = match_data["dragonKills"]
    # inhibitorsLost
    new_data["inhibitorsLost"] = match_data["inhibitorsLost"]
    # turretsLost
    new_data["turretsLost"] = match_data["turretsLost"]
    # time afk
    new_data["time_afk"] = match_data["timePlayed"] - match_data["gameDuration"]
    # largestKillingSpree
    new_data["largestKillingSpree"] = match_data["largestKillingSpree"]
    # gameEndedInEarlySurrender
    new_data["gameEndedInEarlySurrender"] = match_data["gameEndedInEarlySurrender"]
    # gameEndedInSurrender
    new_data["gameEndedInSurrender"] = match_data["gameEndedInSurrender"]
    # teamEarlySurrendered
    new_data["teamEarlySurrendered"] = match_data["teamEarlySurrendered"]
    # win
    new_data["win"] = match_data["win"]
    return new_data

def calc_mean_matches(matches):
    summed_up = {}
    for match in matches:
        for key, value in match.items():
            if key not in summed_up:
                summed_up[key] = value
            else:
                summed_up[key] += value
    return {key: value / len(matches) for key, value in summed_up.items()}

HISTORY = List[dict]
RANK_ID = int

def prepare_data(df):
    print("Get all histories, ....")
    histories : List[Tuple[RANK_ID, HISTORY]]= [(RANK_TO_CLASS[s.tier, s.rank], [preprocess_match(i, s) for i in m]) for s, m in db.get_all_histories(match_limit=NB_GAMES)]
    print("Calc mean history")
    mean_histories = [calc_mean_matches(matches) for _, matches in histories]
    print("Done")
    values = {}

    for history in mean_histories:
        for key, value in history.items():
            if key not in values:
                values[key] = [value]
            else:
                values[key].append(value)

    for key, value in values.items():
        df[key] = value
    # merge with main df bridge_df on key values
    X = df.values
    print("Finishing data preparation")
    return X, [i for i, _ in histories]


def train():
    df_train = pd.DataFrame()
    scaler = StandardScaler()
    data, ranks = prepare_data(df_train)

    print("fit tranforming")
    # generate binary values using get_dummies
    X_train = scaler.fit_transform(data)
    y_train = ranks
    print("Start training ...")
    reg = RandomForestRegressor(max_depth=10).fit(X_train, y_train)
    print("Mean squared error:", mean_squared_error(y_train, reg.predict(X_train)) ** 0.5)
    return reg, scaler


def submit(reg, scaler, target_summoner : Summoner, target_matches : List[Match]):
    df_test = pd.DataFrame()

    preprocess_matchs = [preprocess_match(match, target_summoner) for match in target_matches]
    for key, value in calc_mean_matches(preprocess_matchs).items():
        df_test[key] = [value]

    print(df_test)
    X_test = scaler.transform(df_test.values)
    rank = reg.predict(X_test)
    print(f"{target_summoner.summonerName} is {ranksNames[int(rank)] if rank < len(ranksNames) else 'rank'+str(rank)}")

def main():
    data_crawler = DataCrawler()
    loop = asyncio.get_event_loop()
    print(f"Fetching match for {sys.argv[1]} from Riot API")
    target_summoner, target_matches = loop.run_until_complete(data_crawler.get_matches_for_summoner_name(sys.argv[1], NB_GAMES))
    r, s = train()
    submit(r, s, target_summoner, target_matches)

if __name__ == '__main__':
    main()