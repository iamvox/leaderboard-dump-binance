import json
import requests
import pandas as pd
from datetime import datetime

now = datetime.now()

df = pd.DataFrame()
dfNames = pd.DataFrame()
nicknamesLong = []

id_headers = {
    'authority': 'www.binance.com',
    'x-trace-id': '', #xtrace
    'csrftoken': '', #csrf token
    'x-ui-request-trace': '', #x-ui-request-trace
    'user-agent': '', #UA
    'content-type': 'application/json',
    'lang': 'en',
    'fvideo-id': '', #fvideo id
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'device-info': '', #device-info
    'bnc-uuid': '', #bnc-uuid
    'clienttype': 'web',
    'sec-ch-ua-platform': '"macOS"',
    'accept': '*/*',
    'origin': 'https://www.binance.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.binance.com/en/futures-activity/leaderboard?type=filterResults&isShared=true&limit=200&periodType=MONTHLY&pnlGainType=LEVEL4&roiGainType=&sortType=ROI&symbol=&tradeType=PERPETUAL',
    'accept-language': 'en,en-US;q=0.9,ru-RU;q=0.8,ru;q=0.7',
    'cookie': '', #cookie
}

pos_headers = {
    'authority': 'www.binance.com',
    'x-trace-id': '', #xtrace
    'csrftoken': '', #csrf token
    'x-ui-request-trace': #x-ui-request-trace
    'user-agent': '', #UA
    'content-type': 'application/json',
    'lang': 'en',
    'fvideo-id': '', #fvideo id
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'device-info': '', #device info
    'bnc-uuid': '', #bnc-uuid
    'clienttype': 'web',
    'sec-ch-ua-platform': '"macOS"',
    'accept': '*/*',
    'origin': 'https://www.binance.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.binance.com/en/futures-activity/leaderboard?type=filterResults&isShared=true&limit=200&periodType=MONTHLY&pnlGainType=LEVEL4&roiGainType=&sortType=ROI&symbol=&tradeType=PERPETUAL',
    'accept-language': 'en',
    'cookie': '', #cookie
}

id_url = 'https://www.binance.com/bapi/futures/v2/public/future/leaderboard/getLeaderboardRank'
pos_url = 'https://www.binance.com/bapi/futures/v1/public/future/leaderboard/getOtherPosition'

ids = []
positions = []
nicknames = []

interval = ["DAILY", "WEEKLY", "MONTHLY", "ALL"]

# get user id's across all time intervals
for n in interval:
    try:
        response = requests.post(
            id_url, headers=id_headers, json={"isShared": True,
                                              "periodType": n, "statisticsType": "PNL", "tradeType": "PERPETUAL"})
    except requests.exceptions.Timeout:
        print("Timeout occurred, line 78")
    pos_response = json.loads(response.content)
    for element in pos_response["data"]:
        nicknames.append(element['nickName'])
        ids.append(element['encryptedUid'])

# get open positions of each id and assign a nickname to each position
k = 0
for n in ids:
    k = k + 1
    try:
        pos_response = requests.post(pos_url, headers=pos_headers,
                                     json={"encryptedUid": n, "tradeType": "PERPETUAL"}, timeout=2)
    except requests.exceptions.Timeout:
        print("Timeout occurred, line 92")

    try:
        data = json.loads(pos_response.text)
        df = df.append(data['data']['otherPositionRetList'], ignore_index=True)
        nameRange = 0
        if(data['data']['otherPositionRetList'] is None):
            nameRange = 0
        else:
            nameRange = len(data['data']['otherPositionRetList'])
        for i in range(nameRange):
            nicknamesLong.append(nicknames[k-1])
    except ValueError:
        print("Oops! Some unimportant error occured, line 105, so you can totally ignore it and move on with your day :)")

df['nickNames'] = nicknamesLong
df.drop_duplicates(subset='entryPrice', keep='first', inplace=True)

df.to_csv('tables/' + str(now.strftime("%d-%m-%Y %H:%M")) + '.csv')
