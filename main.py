import asyncio
from statistics import mean, geometric_mean, harmonic_mean, median, mode, pvariance
from typing import Tuple

import sys
import json
from typing import List, Dict, Tuple, Any
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, SGDClassifier, LogisticRegression
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVC

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
    new_data["champion"] = match_data.get("championId", 0)
    # IsJgl
    new_data["is_jgl"] = match_data.get("individualPosition", 0) == "JUNGLE"
    # IsSupport
    new_data["is_sup"] = match_data.get("individualPosition", 0) == "UTILITY"
    # MatchLength
    new_data["game_len"] = match_data.get("gameDuration", 0)

    # assists/min
    new_data["assists"] = match_data.get("assists", 0) * 60 / match_data.get("gameDuration", 0)
    # deaths/min
    new_data["deaths"] = match_data.get("deaths", 0) * 60 / match_data.get("gameDuration", 0)
    # kills/min
    new_data["kills"] = match_data.get("kills", 0) * 60 / match_data.get("gameDuration", 0)
    # wardsKilled/min
    new_data["wards_killed"] = match_data.get("wardsKilled", 0) * 60 / match_data.get("gameDuration", 0)
    # wardsPlaced/min
    new_data["wards_placed"] = match_data.get("wardsPlaced", 0) * 60 / match_data.get("gameDuration", 0)
    # visionScore/min
    new_data["vision_score"] = match_data.get("visionScore", 0) * 60 / match_data.get("gameDuration", 0)
    # visionWardsBoughtInGame/min
    new_data["vision_wards_bought"] = match_data.get("visionWardsBoughtInGame", 0) * 60 / match_data.get("gameDuration", 0)
    # sightWardsBoughtInGame/min
    new_data["sight_wards_bought"] = match_data.get("sightWardsBoughtInGame", 0) * 60 / match_data.get("gameDuration", 0)
    # detectorWardsPlaced/min
    new_data["detector_wards_placed"] = match_data.get("detectorWardsPlaced", 0) * 60 / match_data.get("gameDuration", 0)
    # totalDamageDealt/min
    new_data["damage_dealt"] = match_data.get("totalDamageDealt", 0) * 60 / match_data.get("gameDuration", 0)
    # totalDamageTaken/min
    new_data["damage_taken"] = match_data.get("totalDamageTaken", 0) * 60 / match_data.get("gameDuration", 0)
    # totalMinionsKilled/min
    new_data["minions_killed"] = match_data.get("totalMinionsKilled", 0) * 60 / match_data.get("gameDuration", 0)
    # damageDealtToBuildings/min
    new_data["damage_to_buildings"] = match_data.get("damageDealtToBuildings", 0) * 60 / match_data.get("gameDuration", 0)
    # longestTimeSpentLiving in % of the game
    new_data["longest_time_alive"] = match_data.get("longestTimeSpentLiving", 0) * 60 / match_data.get("gameDuration", 0)
    # %game spent dead
    new_data["game_portion_dead"] = match_data.get("totalTimeSpentDead", 0) * 60 / match_data.get("gameDuration", 0)
    # summoner1 mean uptime
    new_data["summoner1_uptime"] = match_data.get("summoner1Casts", 0) / (match_data.get("gameDuration", 0) / cooldowns[str(match_data.get("summoner1Id", 0))])
    # summoner2 mean uptime
    new_data["summoner2_uptime"] = match_data.get("summoner2Casts", 0) / (match_data.get("gameDuration", 0) / cooldowns[str(match_data.get("summoner2Id", 0))])

    # baronKills
    new_data["baronKills"] = match_data.get("baronKills", 0)
    # dragonKills
    new_data["dragonKills"] = match_data.get("dragonKills", 0)
    # inhibitorsLost
    new_data["inhibitorsLost"] = match_data.get("inhibitorsLost", 0)
    # turretsLost
    new_data["turretsLost"] = match_data.get("turretsLost", 0)
    # largestKillingSpree
    new_data["largestKillingSpree"] = match_data.get("largestKillingSpree", 0)
    # gameEndedInEarlySurrender
    new_data["gameEndedInEarlySurrender"] = match_data.get("gameEndedInEarlySurrender", 0)
    # gameEndedInSurrender
    new_data["gameEndedInSurrender"] = match_data.get("gameEndedInSurrender", 0)
    # teamEarlySurrendered
    new_data["teamEarlySurrendered"] = match_data.get("teamEarlySurrendered", 0)
    # win
    new_data["win"] = match_data.get("win", 0.5)

    # Handle bouteille API
    for k, v in new_data.items():
        if v < 0:
            print(f"Bouteille API detected: got value {v} for {k}")
            new_data[k] = 0
    return new_data

def get_all_data(matches : List[Dict[str, Any]]) -> Dict[str, list]:
    summed_up = {}
    for match in matches:
        for key, value in match.items():
            if key not in summed_up:
                summed_up[key] = [float(value)]
            else:
                summed_up[key].append(float(value))
    return summed_up

def calc_stats_on_matches(matches, name, fct):
    champions = [m["champion"] for m in matches]
    result = {(name + key): fct(value) for key, value in get_all_data(matches).items()}
    result["champion"] = max(champions, key=lambda d: champions.count(d))
    return result

def calc_all_stats_matches(matches):
    fcts = {"mean": mean, "hmean": harmonic_mean, "median": median, "mode": mode, "variance": pvariance}
    stats = [calc_stats_on_matches(matches, k, i) for k, i in fcts.items()]
    return {k: v for d in stats for k, v in d.items()}

HISTORY = List[dict]
RANK_ID = int

def prepare_data(df):
    print("Get all histories, ....")
    histories : List[Tuple[RANK_ID, HISTORY]] = []
    for s, m in db.get_all_histories(match_limit=NB_GAMES):
        try:
            histories.append( (RANK_TO_CLASS[s.tier, s.rank], [preprocess_match(i, s) for i in m]) )
        except Exception as e:
            print(f"Unknown exception during process of summoner \"{s.summonerName}\"\n{e.__class__.__name__}: {e}")
    print("Calc mean history")
    mean_histories = [calc_all_stats_matches(matches) for _, matches in histories]
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

    print("fit transforming")
    # generate binary values using get_dummies
    X_train = scaler.fit_transform(data)
    y_train = ranks
    regs = {
        "RandomForestRegressor": RandomForestRegressor(max_depth=10),
        "RandomForestClassifier": RandomForestClassifier(n_estimators=500, max_depth=20, criterion='gini', max_features="auto", max_samples=None, verbose=0),
#        "SGDClassifier": SGDClassifier(loss='hinge', verbose=0).fit(X_train, y_train),
        "OneVsRestClassifier(LogisticRegression)": OneVsRestClassifier(LogisticRegression(C=1.0, max_iter=10, n_jobs=-1, verbose=0, solver='sag')),
        "OneVsOneClassifier(LogisticRegression)": OneVsOneClassifier(LogisticRegression(C=1.0, max_iter=100, n_jobs=-1, verbose=0, solver='newton-cg')),
        "KNeighborsClassifier": KNeighborsClassifier(n_neighbors=4, weights='distance'),
        "OneVsRestClassifier(SVC)": OneVsRestClassifier(SVC(C=3.0, verbose=0)),
        "OneVsOneClassifier(SVC)": OneVsOneClassifier(SVC(C=3.0, verbose=0)),
    }
    regs_fitted = dict()
    for i, k in regs.items():
        print(f"Start training {i}...")
        regs_fitted[i] = k.fit(X_train, y_train)
        print("Mean squared error:", mean_squared_error(y_train, regs_fitted[i].predict(X_train)) ** 0.5)
    return regs_fitted, scaler


def submit(regs, scaler, target_summoner : Summoner, target_matches : List[Match]):
    df_test = pd.DataFrame()

    preprocess_matchs = [preprocess_match(match, target_summoner) for match in target_matches]
    for key, value in calc_all_stats_matches(preprocess_matchs).items():
        df_test[key] = [value]

    print(df_test)
    X_test = scaler.transform(df_test.values)
    for i, k in regs.items():
        rank = k.predict(X_test)
        print(f"{i}: {target_summoner.summonerName} is {ranksNames[int(rank)] if rank < len(ranksNames) else 'rank'+str(rank)}")

def process_summoners_from_argv(r, s, data_crawler, loop):
    for summoner_name in sys.argv[1:]:
        try:
            print(f"Fetching match for {summoner_name} from Riot API")
            target_summoner, target_matches = loop.run_until_complete(data_crawler.get_matches_for_summoner_name(summoner_name, NB_GAMES))
            submit(r, s, target_summoner, target_matches)
        except Exception as e:
            print(f"Caught exception while processing summoner {summoner_name}. {e.__class__.__name__}: {e}")

def process_summoners_from_input_line(r, s, data_crawler, loop):
    try:
        summoner_name = input("Summoner name: ")
        try:
            print(f"Fetching match for {summoner_name} from Riot API")
            target_summoner, target_matches = loop.run_until_complete(data_crawler.get_matches_for_summoner_name(summoner_name, NB_GAMES))
            submit(r, s, target_summoner, target_matches)
        except Exception as e:
            print(f"Caught exception while processing summoner {summoner_name}. {e.__class__.__name__}: {e}")
    except EOFError:
        pass

def main():
    data_crawler = DataCrawler()
    loop = asyncio.get_event_loop()
    r, s = train()
    process_summoners_from_argv(r, s, data_crawler, loop)
    process_summoners_from_input_line(r, s, data_crawler, loop)

if __name__ == '__main__':
    main()
