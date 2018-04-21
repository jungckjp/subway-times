# pip install requests
# pip install --upgrade gtfs-realtime-bindings
# pip install datetime
# pip install humanize
# pip install flask
# pip install colorama

import datetime
import os
import time

import config
import humanize
import requests
from colorama import Back, Fore, Style
from google.transit import gtfs_realtime_pb2

def refresh():
    print Fore.RESET + Back.RESET
    trains = []

    q = getQ()
    sbs = getSBS()
    fourfivesix = getFourFiveSix()
        
    for train in fourfivesix[:20]:
            trains.append(train)
    
    for train in q[:20]:
        trains.append(train)

    for train in sbs[:20]:
        trains.append(train)

    sort_on = "timetech"
    decorated = [(dict_[sort_on], dict_) for dict_ in trains]
    decorated.sort()
    trains = [dict_ for (key, dict_) in decorated]
    trains.reverse()

    trains = filter(lambda a: a['timetech'] < datetime.timedelta(minutes=-8), trains) # or "SBS" in a['train']
    trainstext = ""
    for train in trains[:20]:
        trainstext += train['train'] + " arriving " + train['time'] + "<br>"

    printTrains(trains)

    return trainstext

def printTrains(trains):
    os.system('clear')
    for train in trains[:20]:
        print train['train'] + " arriving " + train['time']
    os.system('sudo ~/Documents/Code/rpi-rgb-led-matrix/rpi-rgb-led-matrix-58830f7bb5dfb47fc24f1fd26cd7c4e3a20f13f7/examples-api-use/text-example --led-no-hardware-pulse --led-gpio-mapping=adafruit-hat --led-rows=32 --led-cols=64 --led-slowdown-gpio=2 -f ../fonts/8x13.bdf -C 0,204,175')
    os.system('Testing')

def getFourFiveSix():
    fourfivesix = []
    response2 = requests.get("http://datamine.mta.info/mta_esi.php?key=" + config.SUBWAY_API_KEY +"&feed_id=1")

    feed2 = gtfs_realtime_pb2.FeedMessage()
    feed2.ParseFromString(response2.content)
    for entity in feed2.entity:
        if entity.HasField('trip_update'):
            for stopUpdate in entity.trip_update.stop_time_update:
                if stopUpdate.stop_id == "626S":
                    #print entity.trip_update.trip
                    currenttime = datetime.datetime.now()
                    traintime = datetime.datetime.fromtimestamp(stopUpdate.arrival.time)
                    timeuntiltrain = (currenttime - traintime)
                    traintimetext = ""
                    if int(traintime.strftime("%H")) > 12:
                        traintimetext = str(int(traintime.strftime("%H")) - 12) + traintime.strftime(":%M") + " PM"
                    else:
                        traintimetext = traintime.strftime("%H:%M") + " AM"
                    if (entity.trip_update.trip.route_id == "4"):
                        fourfivesix.append({'train':"86th Street " + Back.GREEN + Fore.WHITE + " 4 " + Fore.RESET + Back.RESET + " South",'time':(humanize.naturaltime(timeuntiltrain) + " (" + traintimetext + ")"), 'timetech':timeuntiltrain})
                    if (entity.trip_update.trip.route_id == "5"):
                        fourfivesix.append({'train':"86th Street " + Back.GREEN + Fore.WHITE + " 5 " + Fore.RESET + Back.RESET + " South",'time':(humanize.naturaltime(timeuntiltrain) + " (" + traintimetext + ")"), 'timetech':timeuntiltrain})
                    if (entity.trip_update.trip.route_id == "6"):
                        fourfivesix.append({'train':"86th Street " + Back.GREEN + Fore.WHITE + " 6 " + Fore.RESET + Back.RESET + " South",'time':(humanize.naturaltime(timeuntiltrain) + " (" + traintimetext + ")"), 'timetech':timeuntiltrain})
    return fourfivesix

def getQ():
    q = []
    response = requests.get("http://datamine.mta.info/mta_esi.php?key=" + config.SUBWAY_API_KEY +"&feed_id=16")

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    for entity in feed.entity:
        if entity.HasField('trip_update'):
            for stopUpdate in entity.trip_update.stop_time_update:
                if stopUpdate.stop_id == "Q04S":
                    currenttime = datetime.datetime.now()
                    traintime = datetime.datetime.fromtimestamp(stopUpdate.arrival.time)
                    timeuntiltrain = (currenttime - traintime)
                    traintimetext = ""
                    if int(traintime.strftime("%H")) > 12:
                        traintimetext = str(int(traintime.strftime("%H")) - 12) + traintime.strftime(":%M") + " PM"
                    else:
                        traintimetext = traintime.strftime("%H:%M") + " AM"
                    q.append({'train':"86th Street " + Back.YELLOW + Fore.BLACK + " Q " + Fore.RESET + Back.RESET + " South",'time':(humanize.naturaltime(timeuntiltrain) + " (" + traintimetext + ")"), 'timetech':timeuntiltrain})
    return q

def getSBS():
    sbs = []
    response = requests.get("http://gtfsrt.prod.obanyc.com/tripUpdates?key=" + config.BUS_API_KEY)

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    for entity in feed.entity:
        if entity.HasField('trip_update'):
            for stopUpdate in entity.trip_update.stop_time_update:
                if stopUpdate.stop_id == "401922":
                    currenttime = datetime.datetime.now()
                    traintime = datetime.datetime.fromtimestamp(stopUpdate.arrival.time)
                    timeuntiltrain = (currenttime - traintime)
                    traintimetext = ""
                    if int(traintime.strftime("%H")) > 12:
                        traintimetext = str(int(traintime.strftime("%H")) - 12) + traintime.strftime(":%M") + " PM"
                    else:
                        traintimetext = traintime.strftime("%H:%M") + " AM"
                    sbs.append({'train':"86th Street " + Back.BLUE + Fore.LIGHTRED_EX + "SBS" + Fore.RESET + Back.RESET + " West",'time':(humanize.naturaltime(timeuntiltrain) + " (" + traintimetext + ")"), 'timetech':timeuntiltrain})
    return sbs

if __name__ == '__main__':
    while True:
        refresh()
        time.sleep(30)
