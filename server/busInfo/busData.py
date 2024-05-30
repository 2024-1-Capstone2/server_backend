import requests
import pprint
import json

def getBusInfo():
    url = 'http://apis.data.go.kr/B551177/BusInformation/getBusInfo'
    params ={'serviceKey' : 'L0N+7lJk031KQZI30ENd+bmj6SJ+bHrcs1Abwred2W9LR9HviOYOmk0iZDSzyRG0IWmHA4uGz1ZsCuQ7pBP81w==',
             'numOfRows' : '10', 'pageNo' : '2', 'area' : '7', 'type' : 'json' }

    response = requests.get(url, params=params)

    response.encoding = 'utf-8'

    data = response.json()

    print(data)
    return data