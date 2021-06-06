import os
import requests
import json
import sys
import io
import numpy as np
import csv

def currentViewers(channel):
    sys.stdout.flush()
    data = requests.get('http://tmi.twitch.tv/group/user/'+ channel.lower() +'/chatters').json()
    if(data != ""):
        # Getting all the viewers we are interested in
        currentViewers = data['chatters']['vips'] + data['chatters']['viewers'] 
        return currentViewers
    else:
        return None # if something goes wrong

def main():

    channels = np.array(np.loadtxt("A:/ORF 387 Test/channels.csv", dtype = 'str', comments = "#", delimiter = ",", unpack = False))

    os.chdir('A:/ORF 387')
    
    for channel in channels:
        viewers = currentViewers(channel)
        if viewers != None:

            # new plan

            # check to see if directory exists, create it if not
            if os.path.isdir("A:/ORF 387/" + channel) == False:
                os.mkdir(channel)

            # it's loop time baby
            for viewer in viewers:
                
                # get first character of chatter
                first = viewer[0]
                # check to see if corresponding first level directory already exists
                if os.path.isdir("A:/ORF 387/" + channel + "/" + first) == False:
                    # if not, create it
                    os.mkdir("A:/ORF 387/" + channel + "/" + first)


                # for viewers with one letter usernames. These are not technically possible, but my paranoia compels me to include this just in case
                if len(viewer) < 2:

                    sys.stdout.flush()
                    # check to see if the viewer has already been recorded
                    already_recorded = False
                    if os.path.isfile("A:/ORF 387/" + channel + "/" + first + '/' + "none.csv") != False:
                        past_viewers = np.array(np.loadtxt("A:/ORF 387/" + channel + "/" + first + '/' + "none.csv", dtype = 'str', comments = "#", delimiter = ",", unpack = False))
                        if past_viewers.shape != ():
                            for past_viewer in past_viewers:
                                if past_viewer == viewer:
                                    already_recorded = True
                                    break
                        else:
                            if past_viewers == viewer:
                                already_recorded = True
                        
                    # if the viewer hasn't been recorded, record them
                    if already_recorded == False:
                        with open("A:/ORF 387/" + channel + "/" + first + '/' + "none.csv", 'a', newline = '') as test:
                            w = csv.writer(test)
                            w.writerow([viewer])

                else:

                    sys.stdout.flush()
                    # second letter of the viewer
                    second = viewer[1]

                    # creating the third level directory
                    if os.path.isdir("A:/ORF 387/" + channel + '/' + first + '/' + second) == False:
                        os.mkdir("A:/ORF 387/" + channel + '/' + first + '/' + second)

                    # for two letter viewers. These are not technically possible, but my paranoia compels me to include this just in case
                    if len(viewer) < 3:

                        # check to see if the viewer has already been recorded
                        already_recorded = False
                        if os.path.isfile("A:/ORF 387/" + channel + "/" + first + '/' + second + '/' +  "none.csv") != False:
                            past_viewers = np.array(np.loadtxt("A:/ORF 387/" + channel + "/" + first + '/' + second + '/' +  "none.csv", dtype = 'str', comments = "#", delimiter = ",", unpack = False))
                            if past_viewers.shape != ():
                                for past_viewer in past_viewers:
                                    if past_viewer == viewer:
                                        already_recorded = True
                                        break
                            else:
                                if past_viewers == viewer:
                                    already_recorded = True

                        # if the viewer hasn't been recorded, record them
                        if already_recorded == False:
                            with open("A:/ORF 387/" + channel + "/" + first + '/' + second + '/' +  "none.csv", 'a', newline = '') as test:
                                w = csv.writer(test)
                                w.writerow([viewer])
                                    
                    # for all other viewers
                    else:

                        sys.stdout.flush()
                        # third letter of the viewer's name
                        third = viewer[2]

                        # check to see if the viewer has already been recorded. This could be improved using sets and intersection, but I am done running this and am not going to rewrite it
                        already_recorded = False
                        if os.path.isfile("A:/ORF 387/" + channel + "/" + first + '/' + second + '/' +  third + ".csv") != False:
                            past_viewers = np.array(np.loadtxt("A:/ORF 387/" + channel + "/" + first + '/' + second + '/' +  third + ".csv", dtype = 'str', comments = "#", delimiter = ",", unpack = False))
                            if past_viewers.shape != ():
                                for past_viewer in past_viewers:
                                    if past_viewer == viewer:
                                        already_recorded = True
                                        break

                            else:
                                if past_viewers == viewer:
                                    already_recorded = True

                        # if the viewer hasn't been recorded, record them
                        if already_recorded == False:
                            with open("A:/ORF 387/" + channel + "/" + first + '/' + second + '/' +  third + ".csv", 'a', newline = '') as test:
                                w = csv.writer(test)
                                w.writerow([viewer])


#Program Execution
if __name__ == '__main__':
    main()
