import requests
import json
import csv

FPL_URL = "https://fantasy.premierleague.com/drf/"
POINTS_FILENAME = "gameweek_points.csv"
CUMULATIVE_POINTS_FILENAME = "gameweek_cumulative_points.csv"
CURRENT_GAMEWEEK = 36

# Daniel, Jayden, James
PLAYER_NAMES = ["Daniel", "Jayden", "James"]
PLAYER_IDS = [226252, 815677, 2229616]

def getPointsForGameweek(player_id, gameweek):
    r = requests.get(FPL_URL + "entry/" + str(player_id) + "/event/" + str(gameweek) + "/picks")
    jsonResponse = r.json()

    return jsonResponse["entry_history"]["points"]

def getCumulativePointsForGameweek(player_id, gameweek):
    r = requests.get(FPL_URL + "entry/" + str(player_id) + "/event/" + str(gameweek) + "/picks")
    jsonResponse = r.json()
    return jsonResponse["entry_history"]["total_points"]

def getPointsForSeason(player_id):
    pointsList = []
    for i in range(1, CURRENT_GAMEWEEK + 1):
        pointsList.append(getPointsForGameweek(player_id, i))
    
    return pointsList

def getCumulativePointsForSeason(gwpoints_allplayers):
    pointsList = []
    for i in range(1, CURRENT_GAMEWEEK + 1):
        pointsList.append(getCumulativePointsForGameweek(player_id, i))
    
    return pointsList

def transposeData(gwpoints_allplayers):
    gw_points = []
    gw_points.append(PLAYER_NAMES)
    for gw in range(0, CURRENT_GAMEWEEK):
        temp_list = []
        for player in range(0, 3):
            temp_list.append(gwpoints_allplayers[player - 1][gw])
        gw_points.append(temp_list)
    return gw_points

def transposeDataWithGameweek(gwpoints_allplayers):
    gw_points = []
    gw_points.append("Gameweek")
    gw_points.append(PLAYER_NAMES)
    for gw in range(0, CURRENT_GAMEWEEK):
        temp_list = []
        for player in range(0, 3):
            if (player == 0):
                temp_list.append(gw + 1)
            temp_list.append(gwpoints_allplayers[player - 1][gw])
        gw_points.append(temp_list)
    return gw_points

# Main Script
gameweek_points_allplayers = []
cumulative_points_allplayers = []

for player_id in PLAYER_IDS:
    gameweek_points_allplayers.append(getPointsForSeason(player_id))
    cumulative_points_allplayers.append(getCumulativePointsForSeason(player_id))

print("Scraped all data")

with open("data/" + CUMULATIVE_POINTS_FILENAME, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(transposeDataWithGameweek(cumulative_points_allplayers))

with open("data/" + POINTS_FILENAME, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(transposeData(gameweek_points_allplayers))

print("Printed to file")
