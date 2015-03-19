#Citrix Webinar Helper

Never miss a Webinar. A scheduler to open Citrix Webinars (or other URLs) at a specified date and time.

The main program is open_urls_at_datetime.py.  It was created to automatically open a Citrix Webinar URL a set number of minutes before a Webinar starts but could be used to automatically open any URL at a given date and time. There is no external database to track the Webinar information but it is currently hardcoded into the script which is easily changed as you add Webinars to your schedule.

When you sign up for a Citrix Webinar you get an email containing the Webinar date, time, title and URL. The second program clipboard_to_webinar_format.py is designed so that if you copy the text of the email message to the clipboard and run this program, it will parse the email text for the information and put on the clipboard a call to the add_webinar function. Paste these calls (one for each Webinar) into open_urls_at_datetime.py and then run that script. It will continue to run until either you stop it or it loads each of the URLs at the proper date and time.

There are a number of things that would be nice to add to this starting with an external database.
