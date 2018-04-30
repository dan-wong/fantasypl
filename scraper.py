import requests
import json
import csv

FPL_URL = "https://fantasy.premierleague.com/drf/"
POINTS_FILENAME = "gameweek_points.csv"
CURRENT_GAMEWEEK = 36

# Daniel, Jayden, James
PLAYER_NAMES = ["Gameweek", "Daniel", "Jayden", "James"]
PLAYER_IDS = [226252, 815677, 2229616]

def getPointsForGameweek(player_id, gameweek):
    r = requests.get(FPL_URL + "/entry/" + str(player_id) + "/event/" + str(gameweek) + "/picks")
    jsonResponse = r.json()
    return jsonResponse["entry_history"]["points"]

def getPointsForSeason(player_id):
    pointsList = []
    for i in range(1, CURRENT_GAMEWEEK + 1):
        pointsList.append(getPointsForGameweek(player_id, i))
    
    return pointsList

def calculateCumulativePoints(gwpoints_allplayers):
    cumulative_points = []
    for player in range(1, 4):
        temp_list = []
        runningSum = 0
        for gw in range(0, CURRENT_GAMEWEEK):
            runningSum += gwpoints_allplayers[player - 1][gw]
            temp_list.append(runningSum)
        cumulative_points.append(temp_list)
    return cumulative_points

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
gameweek_points_allplayers = []
filename = "data/" + POINTS_FILENAME

for player_id in PLAYER_IDS:
    gameweek_points_allplayers.append(getPointsForSeason(player_id))

print("Scraped all data")

with open(filename, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(transposeData(calculateCumulativePoints(gameweek_points_allplayers)))

print("Printed to file")
