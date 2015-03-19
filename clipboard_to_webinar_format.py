#!/usr/bin/env python

"""
This is a helper script to take the work out of adding entries to the
list of Webinars. 

When you register for a Citrix Webinar you'll get an email thanking you for 
registering and telling you the date and time and the URL to join the Webinar. 

Copy the text of that message to the clipboard and run this script. It will 
parse the message and then stuff back onto the clipboard an add_webinar() call
that can be plugged into the open_urls_at_datetime.py file. 

Ideally, this data would be stored in a database/XML dump but it isn't worth
the extra effort right now to code.

By Stephen Genusa
March 2015

http://development.genusa.com
"""

import subprocess
import re
import datetime
import sys


def getClipboardData():
    """ Win32/Linux/OS X Clipboard Get
    """
    clipboard_data = ""
    if sys.platform == "win32":
        # Not pip installable.
        # http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/
        import win32clipboard
        win32clipboard.OpenClipboard()
        clipboard_data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()        
        
    if sys.platform.find ('linux') > -1:
        import Tkinter
        root = Tkinter.Tk()
        root.withdraw()
        clipboard_data = root.clipboard_get()      
        
    if sys.platform == "darwin":
        """ Get clipboard data on OS X
            From http://www.devx.com/opensource/Article/37233
        """
        p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
        retcode = p.wait()
        clipboard_data = p.stdout.read()
        
    return clipboard_data


def setClipboardData(clipboard_data):
    """ Win32/Linux/OS X Clipboard Set
    """
    if sys.platform == "win32":
        # Not pip installable.
        # http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/
        import win32clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(clipboard_data)
        win32clipboard.CloseClipboard()      
    
    if sys.platform.find ('linux') > -1:
        import Tkinter
        root = Tkinter.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(clipboard_data)
            
    if sys.platform == "darwin":
        """ Set clipboard data on OS X
            From http://www.devx.com/opensource/Article/37233
        """
        p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        p.stdin.write(clipboard_data)
        p.stdin.close()
        retcode = p.wait()
    

# Get the clipboard
clipboard_data = getClipboardData()
# Get the date of the webinar
match = re.search("\n\w{3}, (.{1,30}?201\d \d{1,2}:\d\d [APM]{2})", clipboard_data, re.DOTALL | re.MULTILINE)
if match:
    parsed_datetime = match.groups(0)[0]
    try:
        valid_date = datetime.datetime.strptime(parsed_datetime, "%b %d, %Y %I:%M %p")
    except ValueError as e:
        print(e)
    # Get the URL for the Webinar    
    match = re.search("(http://|https://.{10,100}?)\n", clipboard_data, re.DOTALL | re.MULTILINE)
    if match:
        webinar_url = match.groups(0)[0]
    # Get the Title of the Webinar    
    match = re.search("registering for \"(.{10,100}?)\"", clipboard_data, re.DOTALL | re.MULTILINE)
    if match:
        webinar_name = match.groups(0)[0]
    # Create the function call with the parsed data
    webinar_entry = 'add_webinar({0}, {1}, {2}, {3}, {4}, "{5}", "{6}")'.format(valid_date.year, valid_date.month, valid_date.day, valid_date.hour, valid_date.minute, webinar_url.strip(), webinar_name.strip())
    setClipboardData(webinar_entry)
    print "Webinar entry on clipboard"
    #print webinar_entry
