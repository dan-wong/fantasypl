import requests
import json
import csv

FPL_URL = "https://fantasy.premierleague.com/drf/"
CURRENT_GAMEWEEK = 38

# Daniel, Jayden, James
PLAYER_NAMES = ["Gameweek", "Daniel", "Jayden", "James"]
PLAYER_IDS = [226252, 815677, 2229616]

def getDataForGameweek(player_id, gameweek):
    r = requests.get(FPL_URL + "entry/" + str(player_id) + "/event/" + str(gameweek) + "/picks")
    jsonResponse = r.json()

    data = []
    data.append(jsonResponse["entry_history"]["points"])
    data.append(jsonResponse["entry_history"]["total_points"])
    data.append(jsonResponse["entry_history"]["points_on_bench"])

    return data

def getDataObjectForSeason(player_id):
    data_for_player = []
    for i in range(1, CURRENT_GAMEWEEK):
        data_for_player.append(getDataForGameweek(player_id, i))
    return data_for_player

def getData(data_object, index):
    pointsList = []
    for player_index in range(0, 3):
        temp = []
        for i in range(0, CURRENT_GAMEWEEK):
            temp.append(data_object[player_index][i][index])
        pointsList.append(temp)
    
    return pointsList

def getGameweekPoints(data_object):
    return getData(data_object, 0)

def getCumulativeGameweekPoints(data_object):
    return getData(data_object, 1)

def getBenchGameweekPoints(data_object):
    return getData(data_object, 2)

def getCombinedGameweekAndBenchPoints(data_object):
    gameweek_points = getGameweekPoints(data_object)
    bench_points = getBenchGameweekPoints(data_object)

    pointsList = []
    for player_index in range(0,3):
        temp = []
        for i in range(0, CURRENT_GAMEWEEK):
            temp.append(gameweek_points[player_index][i] + bench_points[player_index][i])
        pointsList.append(temp)
    
    return pointsList

def transposeData(gwpoints_allplayers):
    gw_points = []
    gw_points.append(PLAYER_NAMES)
    for gw in range(0, CURRENT_GAMEWEEK):
        temp_list = []
        for player in range(0, 4):
            if (player == 0):
                temp_list.append(gw + 1)
            else:
                temp_list.append(gwpoints_allplayers[player - 1][gw])
        gw_points.append(temp_list)
    return gw_points

# Main Script
data_object = []

print("Scraping data")

for player_id in PLAYER_IDS:
    temp = []
    for i in range(0, CURRENT_GAMEWEEK):
        temp.append(getDataForGameweek(player_id, i+1))
        pob_cumulative = 0
    data_object.append(temp)
    print("Finished: " + str(player_id))

print("Scraped all data")

with open("data/gameweek_points.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(transposeData(getGameweekPoints(data_object)))

with open("data/gameweek_cumulative_points.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(transposeData(getCumulativeGameweekPoints(data_object)))

with open("data/gameweek_bench_points.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(transposeData(getBenchGameweekPoints(data_object)))

with open("data/gameweek_combined_points.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(transposeData(getCombinedGameweekAndBenchPoints(data_object)))

print("Printed to file")
