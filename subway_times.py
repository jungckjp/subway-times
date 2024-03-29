#!/usr/bin/python
# -*- coding: utf-8 -*-
# pip install requests
# pip install --upgrade gtfs-realtime-bindings
# pip install datetime
# pip install humanize
# pip install flask
# pip install colorama

import datetime
import os
import time
import calendar
from urllib2 import urlopen, Request

from samplebase import SampleBase
from rgbmatrix import graphics
import config
import humanize
import requests
from colorama import Back, Fore, Style
from google.transit import gtfs_realtime_pb2

class RunText(SampleBase):
    
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")


    def refresh(self):
        print(Fore.RESET + Back.RESET)
        trains = []

        q = self.getQ()
        # sbs = self.getSBS()
        fourfivesix = self.getFourFiveSix()

        for train in fourfivesix[:20]:
            trains.append(train)

        for train in q[:20]:
            trains.append(train)

        # for train in sbs[:20]:
        #     trains.append(train)

        sort_on = 'timetech'
        decorated = [(dict_[sort_on], dict_) for dict_ in trains]
        decorated.sort()
        trains = [dict_ for (key, dict_) in decorated]
        # trains.reverse()

        trains = filter(lambda a: a['timetech'] \
                        < datetime.timedelta(minutes=-8), trains)  # or "SBS" in a['train']
        trainstext = ''
        for train in trains[:20]:
            trainstext += train['train'] + ' arriving ' + train['time'] \
                + '<br>'

        #self.printTrains(trains)

        return trains[0]['train'] + ' arriving ' + trains[0]['time']

    def printTrains(self,trains):
        os.system('clear')
        for train in trains[:20]:
            print(train['train'] + ' arriving ' + train['time'])

    def getFourFiveSix(self):
        API_headers = {"x-api-key": config.SUBWAY_API_KEY}
        fourfivesix = []
        # response2 = requests.get('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs', headers=API_headers)

        feed2 = gtfs_realtime_pb2.FeedMessage()
        req = Request('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs')
        req.add_header('x-api-key', config.SUBWAY_API_KEY)
        responseMsg = urlopen(req)
        #feed2.ParseFromString(response2.content)
        feed2.ParseFromString(responseMsg.read())
        for entity in feed2.entity:
            if entity.HasField('trip_update'):
                for stopUpdate in entity.trip_update.stop_time_update:
                    if stopUpdate.stop_id == '626S':

                        # print entity.trip_update.trip

                        currenttime = datetime.datetime.now()
                        traintime = \
                            datetime.datetime.fromtimestamp(stopUpdate.arrival.time)
                        timeuntiltrain = currenttime - traintime
                        traintimetext = ''
                        if int(traintime.strftime('%H')) > 12:
                            traintimetext = \
                                str(int(traintime.strftime('%H')) - 12) \
                                + traintime.strftime(':%M') + ' PM'
                        else:
                            traintimetext = traintime.strftime('%H:%M') \
                                + ' AM'
                        if entity.trip_update.trip.route_id == '4':
                            fourfivesix.append({'train': '86th Street '
                                    + Back.GREEN + Fore.WHITE + ' 4 '
                                    + Fore.RESET + Back.RESET + ' South'
                                    ,
                                    'time': humanize.naturaltime(timeuntiltrain)
                                    + ' (' + traintimetext + ')',
                                    'timetech': timeuntiltrain, 'minutes': ((traintime - currenttime).seconds / 60)})
                        if entity.trip_update.trip.route_id == '5':
                            fourfivesix.append({'train': '86th Street '
                                    + Back.GREEN + Fore.WHITE + ' 5 '
                                    + Fore.RESET + Back.RESET + ' South'
                                    ,
                                    'time': humanize.naturaltime(timeuntiltrain)
                                    + ' (' + traintimetext + ')',
                                    'timetech': timeuntiltrain, 'minutes': ((traintime - currenttime).seconds / 60)})
                        if entity.trip_update.trip.route_id == '6':
                            fourfivesix.append({'train': '86th Street '
                                    + Back.GREEN + Fore.WHITE + ' 6 '
                                    + Fore.RESET + Back.RESET + ' South'
                                    ,
                                    'time': humanize.naturaltime(timeuntiltrain)
                                    + ' (' + traintimetext + ')',
                                    'timetech': timeuntiltrain, 'minutes': ((traintime - currenttime).seconds / 60)})
        trains = []        
        for train in fourfivesix[:20]:
            trains.append(train)

        sort_on = 'timetech'
        decorated = [(dict_[sort_on], dict_) for dict_ in trains]
        decorated.sort()
        trains = [dict_ for (key, dict_) in decorated]
        trains.reverse()

        for train in trains:
            if int(train['minutes']) > 8:
                return str(train['minutes']) + " min"
        return "0 min" #fourfivesix

    def getQ(self):
        API_headers = {"x-api-key": config.SUBWAY_API_KEY}
        q = []
        req = Request('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw')
        req.add_header('x-api-key', config.SUBWAY_API_KEY)
        responseMsg = urlopen(req)

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(responseMsg.read())

        for entity in feed.entity:
            if entity.HasField('trip_update'):
                for stopUpdate in entity.trip_update.stop_time_update:
                    if stopUpdate.stop_id == 'Q04S':
                        currenttime = datetime.datetime.now()
                        traintime = \
                            datetime.datetime.fromtimestamp(stopUpdate.arrival.time)
                        timeuntiltrain = currenttime - traintime
                        traintimetext = ''
                        if int(traintime.strftime('%H')) > 12:
                            traintimetext = \
                                str(int(traintime.strftime('%H')) - 12) \
                                + traintime.strftime(':%M') + ' PM'
                        else:
                            traintimetext = traintime.strftime('%H:%M') \
                                + ' AM'
                        q.append({'train': '86th Street ' + Back.YELLOW
                                 + Fore.BLACK + ' Q ' + Fore.RESET
                                 + Back.RESET + ' South',
                                 'time': humanize.naturaltime(timeuntiltrain)
                                 + ' (' + traintimetext + ')',
                                 'timetech': timeuntiltrain, 'minutes': ((traintime - currenttime).seconds / 60)})
                        #if (((traintime - currenttime).seconds / 60) > 8):
                            #return str(((traintime - currenttime).seconds / 60)) + " min"
        trains = []        
        for train in q[:20]:
            trains.append(train)

        sort_on = 'timetech'
        decorated = [(dict_[sort_on], dict_) for dict_ in trains]
        decorated.sort()
        trains = [dict_ for (key, dict_) in decorated]
        trains.reverse()

        for train in trains:
            if int(train['minutes']) > 8:
                return str(train['minutes']) + " min"
        return "0 min" #q

    # def getSBS(self):
    #     sbs = []
    #     response = \
    #         requests.get('http://gtfsrt.prod.obanyc.com/tripUpdates?key='
    #                       + config.BUS_API_KEY)

    #     feed = gtfs_realtime_pb2.FeedMessage()
    #     feed.ParseFromString(response.content)

    #     for entity in feed.entity:
    #         if entity.HasField('trip_update'):
    #             for stopUpdate in entity.trip_update.stop_time_update:
    #                 if stopUpdate.stop_id == '401922':
    #                     currenttime = datetime.datetime.now()
    #                     traintime = \
    #                         datetime.datetime.fromtimestamp(stopUpdate.arrival.time)
    #                     timeuntiltrain = currenttime - traintime
    #                     traintimetext = ''
    #                     if int(traintime.strftime('%H')) > 12:
    #                         traintimetext = \
    #                             str(int(traintime.strftime('%H')) - 12) \
    #                             + traintime.strftime(':%M') + ' PM'
    #                     else:
    #                         traintimetext = traintime.strftime('%H:%M') \
    #                             + ' AM'
    #                     sbs.append({'train': '86th Street ' + Back.BLUE
    #                                + Fore.LIGHTRED_EX + 'SBS'
    #                                + Fore.RESET + Back.RESET + ' West',
    #                                'time': humanize.naturaltime(timeuntiltrain)
    #                                + ' (' + traintimetext + ')',
    #                                'timetech': timeuntiltrain})
    #     return sbs

    def drawCircle(self, canvas, offset, color):
        graphics.DrawLine(canvas,7,0 + offset,11,0 + offset,color)
        graphics.DrawLine(canvas,5,1 + offset,13,1 + offset,color)
        graphics.DrawLine(canvas,4,2 + offset,14,2 + offset,color)
        graphics.DrawLine(canvas,4,3 + offset,14,3 + offset,color)
        graphics.DrawLine(canvas,3,4 + offset,15,4 + offset,color)
        graphics.DrawLine(canvas,3,5 + offset,15,5 + offset,color)
        graphics.DrawLine(canvas,3,6 + offset,15,6 + offset,color)
        graphics.DrawLine(canvas,3,7 + offset,15,7 + offset,color)
        graphics.DrawLine(canvas,3,8 + offset,15,8 + offset,color)
        graphics.DrawLine(canvas,4,9 + offset,14,9 + offset,color)
        graphics.DrawLine(canvas,4,10 + offset,14,10 + offset,color)
        graphics.DrawLine(canvas,5,11 + offset,13,11 + offset,color)
        graphics.DrawLine(canvas,7,12 + offset,11,12 + offset,color)

    def draw4(self, canvas):
        green = graphics.Color(0, 120, 60)
        black = graphics.Color(0,0,0)
        white = graphics.Color(255, 255, 255)
        yellow = graphics.Color(252,204,10)
        
        self.drawCircle(canvas,2,green)
        
        self.drawCircle(canvas,17,yellow)
        

        
        graphics.DrawLine(canvas, 10,5,10,5 ,white)
        graphics.DrawLine(canvas,  9,6,10,6,white)
        graphics.DrawLine(canvas,  8,7,8,7,white)
        graphics.DrawLine(canvas,  10,7,10,7,white)
        graphics.DrawLine(canvas,  7,8,7,8,white)
        graphics.DrawLine(canvas,  10,8,10,8,white)
        graphics.DrawLine(canvas,  7,9,11,9,white)
        graphics.DrawLine(canvas,  10,10,10,10,white)
        graphics.DrawLine(canvas,  10,11,10,11,white)
        
        offset = 17
        
        graphics.DrawLine(canvas,8,3 + offset,10,3 + offset,black)
        graphics.DrawLine(canvas,7,4 + offset,7,4 + offset,black)
        graphics.DrawLine(canvas,11,4 + offset,11,4 + offset,black)
        graphics.DrawLine(canvas,6,5 + offset,6,5 + offset,black)
        graphics.DrawLine(canvas,12,5 + offset,12,5 + offset,black)
        graphics.DrawLine(canvas,6,6 + offset,6,6 + offset,black)
        graphics.DrawLine(canvas,12,6 + offset,12,6 + offset,black)
        graphics.DrawLine(canvas,6,7 + offset,6,7 + offset,black)
        graphics.DrawLine(canvas,10,7 + offset,10,7 + offset,black)
        graphics.DrawLine(canvas,12,7 + offset,12,7 + offset,black)
        graphics.DrawLine(canvas,7,8 + offset,7,8 + offset,black)
        graphics.DrawLine(canvas,10,8 + offset,11,8 + offset,black)
        graphics.DrawLine(canvas,8,9 + offset,9,9 + offset,black)
        graphics.DrawLine(canvas,11,9 + offset,11,9 + offset,black)

    def run(self):
        numLoops = 0;
        self.matrix.brightness = 75
        traintime = "86th Q" #self.refresh()
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont('../rpi-rgb-led-matrix/rpi-rgb-led-matrix-58830f7bb5dfb47fc24f1fd26cd7c4e3a20f13f7/fonts/6x9.bdf')
        textColor = graphics.Color(255, 255, 0)
        pos = 18
        my_text = traintime
        yellow = graphics.Color(252,204,10)
        black = graphics.Color(0,0,0)
        white = graphics.Color(220, 220, 220)
        red = graphics.Color(204, 51, 0)
        green = graphics.Color(0, 120, 60)
        orange = graphics.Color(230,138,0)
        sickgreen = graphics.Color(204,204,0)
        left = True
        wait = 10
        
        qTime = "0 min"
        fTime = "0 min"
        qTime = self.getQ()
        fTime = self.getFourFiveSix()

        while True:
            offscreen_canvas.Clear()
            #len = graphics.DrawText(
            #    offscreen_canvas,
             #   font,
              #  pos,
               # 30,
                #textColor,
                #my_text,
                #)

#if pos + len < 16:
#               pos = 64
#           else:
#               pos -= 1
            if wait > 0:
                wait -= 1
                len = graphics.DrawText(offscreen_canvas,font,64,12,white,fTime)
                graphics.DrawText(offscreen_canvas,font,63 - len,12,white,fTime)
                twolen = graphics.DrawText(offscreen_canvas,font,64,27,white,qTime)
                graphics.DrawText(offscreen_canvas,font,63 - twolen,27,white,qTime)
                for y in range(0, 31):
                    graphics.DrawLine(offscreen_canvas,0,y,16,y,black)
                self.draw4(offscreen_canvas)
            else:
                clockFont = graphics.Font()
                clockFont.LoadFont('../rpi-rgb-led-matrix/rpi-rgb-led-matrix-58830f7bb5dfb47fc24f1fd26cd7c4e3a20f13f7/fonts/5x7.bdf')
                dayText = datetime.datetime.today().strftime("%A")
                dayLen = graphics.DrawText(offscreen_canvas,clockFont,64,6,red,dayText)
                dateText = datetime.datetime.today().strftime("%B %d")
                dateLen = graphics.DrawText(offscreen_canvas,clockFont,64,6,red,dateText)
                graphics.DrawText(offscreen_canvas,clockFont,((64-dateLen)/2)+1,19,red,dateText)
                graphics.DrawText(offscreen_canvas,clockFont,((64-dayLen)/2)+1,10,red,dayText)

                clockTime = datetime.datetime.now().strftime("%I:%M%p")
                if clockTime[0] == "0":
                    clockTime = clockTime[1:]
                timeLen = graphics.DrawText(offscreen_canvas,clockFont,64,6,red,clockTime)
                graphics.DrawText(offscreen_canvas,clockFont,((64-timeLen)/2)+1,28,green,clockTime)
                #qTime = self.getQ()
                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                
                
                if numLoops == 3:
                    numLoops = 0
                    try:
                        newFTime = self.getFourFiveSix()
                        newQTime = self.getQ()
                        if newFTime != "0 min":
                            fTime = newFTime
                        if newQTime != "0 min":
                            qTime = newQTime
                    except:
                        #do nothing
                        print("Failed to fetch.")
                else:
                    numLoops = numLoops + 1;
                wait = 10
                time.sleep(10)
            #else:
            #    if left:
            #        if pos + len > 63:
            #            pos -= 1
            #        else:
            #            left = False
            #            wait = 6
            #    else:
            #        if pos < 18:
            #            pos += 1
            #        else:
            #            left = True
            #            wait = 6

            time.sleep(1)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


if __name__ == '__main__':
    while True:
        run_text = RunText()
        if (not run_text.process()):
            run_text.print_help()

        time.sleep(5)

    # refresh()
    # time.sleep(30)


			
