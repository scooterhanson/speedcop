# speedcop
Monitoring ISP speeds because they won't.

I got tired of my ISP pretending there was no slowdown when I could tell there was.  Here is a collection of tools I use on cron jobs to record speeds and let me know if something isn't right.  Then I can make sure the ISP is aware right away.

This requires Sqlite3 to record data and Twilio for the notifications.

Run speed.py to record up speed, down speed, ping latency, and jitter.
Run getspeedresults.py to see the latest results.
Run speedcop.py to check the last 4 down-speed results; if the average is lower than the threshold, a Twilio notification will be sent.
Run speedavg.py to get an average over the last day's worth of results and send a Twilio notification.

Written in Python3
