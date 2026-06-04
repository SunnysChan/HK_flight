import requests
from collections import Counter
import datetime
import json

def get_departures_by_date():
    """
    date_str format: YYYY-MM-DD
    """
    # Convert to required format (YYYYMMDD)
    formatted_date = (datetime.datetime.now(datetime.UTC)+ datetime.timedelta(hours=4)).strftime("%Y-%m-%d")

    # API endpoint used by HK Airport site
    url = "https://www.hongkongairport.com/flightinfo-rest/rest/flights"

    params = {
        'span': '1',
        "date": formatted_date,
        "lang": "en",
        "cargo": "false",
        "arrival": "false"  # departure flights only
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    return data


def extract_destinations(flight_data):
    destinations = []

    for record in flight_data:
        # each record contains list of flights
        for flight in record.get("list", []):
            dest = flight.get("destination", [{}])[0]
            destinations.append(dest)

    return destinations

target={'BKK': ['VTBS','Bangkok'],'PEK': ['ZBAA','Beijing'],'TFU': ['ZUUU','Chengdu'],'DAD': ['VVDN','Da Nang'],'DEL': ['VIDP','Delhi'],
        'FUK': ['RJFF','Fukuoka'],'HAK': ['ZJHK','Haikou'],'HND': ['RJTT','Haneda'],'HGH': ['ZSHC','Hangzhou'],'SGN': ['VVTS','Ho Chi Minh'],
        'ICN': ['RKSI','Incheon'],'CGK': ['WIII','Jakarta'],'KIX': ['RJBB','Kansai'],'KHH': ['RCKH','Kaohsiung'],'KUL': ['WMKK','Kuala Lumpur'],
        'MNL': ['RPLL','Manila'],'OKA': ['ROAH','Naha'],'NRT': ['RJAA','Narita'],'SHA': ['ZSSS','Shanghai Hongqiao'],'PVG': ['ZSPD','Shanghai Pudong'],
        'SIN': ['WSSS','Singapore'],'TPE': ['RCTP','Taipei'],'PKX':['ZBAD','Beijing DaXing'],'HAN':['VVNB','Ha Noi'],'NKG':['ZSNJ','Nanjing'],
       'PQC':['VVPQ','Phu']}

try:
    data = get_departures_by_date()
    destinations = extract_destinations(data)

    if not destinations:
        print("No flights found for this date.")
    else:
        counter = Counter(destinations)
        finale=[]
        for dest, count in counter.most_common(30):
            if dest in target:
                finale.append([target[dest][1],target[dest][0],dest,count])
            else:
                finale.append(['///','///',dest,count])

        with open("flights.json", "w", encoding="utf-8") as f:
            json.dump(finale, f, indent=4)

except Exception as e:
    print("Error:", e)
