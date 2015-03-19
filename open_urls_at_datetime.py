#!/usr/bin/env python

"""
Never miss a webinar. A scheduler to open Citrix Webinars (or other URLs) 
at a specified date and time

By Stephen Genusa
March 2015

http://development.genusa.com
"""

import datetime
import os
from subprocess import Popen
import time
import webbrowser

# How many minutes before Webinar begins would you like to have the URL opened?
minutes_before_webinar_to_open = 8

# Set the path to Firefox if using Windows
path_to_browser_win = 'C:\\Program Files\\Mozilla Firefox 30\\firefox.exe'
webinars = []


def add_webinar(year, month, day, hour, minute, url, name):
    """Add a webinar to the webinar list
    """
    # Calc the date/time for the webinar to start minus the minutes before 
    # the webinar to open the browser
    start_time = time.mktime((datetime.datetime(year, month, day, hour, minute, 0) - \
                              datetime.timedelta(minutes=minutes_before_webinar_to_open)).timetuple())
    # Only add it if the date/time is in the future
    if time.mktime(datetime.datetime.now().timetuple()) < start_time+datetime.timedelta(minutes=minutes_before_webinar_to_open).total_seconds():
        webinars.append({"StartTime" : start_time, "URL":url, "EventHandled":False, "EventName":name})

def show_future_webinars():
    """Clear the screen and dump the list of webinars which are still unhandled
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print "The following webinars are being waited on:"
    for webinar in webinars:
        if webinar["EventHandled"] == False:
            print "  ", webinar["EventName"], "at", time.ctime(webinar["StartTime"]+datetime.timedelta(minutes=minutes_before_webinar_to_open).total_seconds())
    print "URLs will open", minutes_before_webinar_to_open, "minutes ahead of time"



###################################################################################
# Call add_webinar(Year, Month, Day, Hour(24), Minute, URL, Title) for each Webinar
###################################################################################

# add_webinar(2015, 3, 25, 10, 0, "https://global.gotowebinar.com/join/###########/#######", "How to Solve Every Global and Personal Problem, Sponsored by Some Sales Pitch")
# add_webinar(2015, 3, 26, 12, 0, "https://global.gotowebinar.com/join/###########/#######", "How to Solve Every Global and Personal Problem, Sponsored by Some Other Sales Pitch")


show_future_webinars()

# Wait for clock to come round to 0 seconds so that URL startups occur
# at the beginning of the start minute rather than possibly waiting till
# the end of a minute
while datetime.datetime.now().timetuple()[5] != 0:
    time.sleep(1)
    
while True:
    # Get the current time
    cur_time = time.mktime(datetime.datetime.now().timetuple())
    # Set a flag which will be tested after looping through all webinars
    all_webinars_launched = True
    for webinar in webinars:
        # If the current time is >= than the time set to open the URL and the 
        # URL has not already been opened
        if cur_time >= webinar["StartTime"] and webinar["EventHandled"] == False:
            webinar["EventHandled"] = True
            print "launching browser", webinar["EventName"]
            # Launch the browser
            if os.name == 'nt':
                cmd = [path_to_browser_win, webinar["URL"]]            
                p = Popen(cmd,shell=False,stdin=None,stdout=None,stderr=None,close_fds=True,creationflags=0x00000008)
            else:
				# May require customization depending on O/S configuration
                webbrowser.open_new_tab(webinar["URL"])
            
            show_future_webinars()
        # Set flag to keep loop running if there are unhandled Webinars left
        if webinar["EventHandled"] == False:
            all_webinars_launched = False
    if all_webinars_launched:
        break
    time.sleep(60)
print "All Webinars launched. Job finished."




