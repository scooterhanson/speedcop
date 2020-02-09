from __future__ import division
from Notifier import Notifier
import datetime
import getopt
import json
import sqlite3
import subprocess
import sys
import time


def main(argv):
    db_location = ''
    account = ''
    token = ''
    from_num = ''
    to_num = ''
    min_down_speed = 100
    try:
        opts, args = getopt.getopt(argv,"ha:t:F:T:d:m:",["account=","token=","from=","to=","db_location=","min_down_speed="])
    except getopt.GetoptError:
        print 'speedavg.py -a <account> -t <token> -F <from> -T <to> -d <db location> -m <min down speed>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'speedavg.py -a <account> -t <token> -F <from> -T <to> -d <db location> -m <min down speed>'
            sys.exit()
        elif opt in ("-d", "--dblocation"):
            db_location = arg
        elif opt in ("-a", "--account"):
            account = arg
        elif opt in ("-t", "--token"):
            token = arg
        elif opt in ("-F", "--from"):
            from_num = arg
        elif opt in ("-T", "--to"):
            to_num = arg
        elif opt in ("-m", "--min_down_speed"):
            min_down_speed = arg

        if db_location != '' and account != '' and token != '' and from_num != '' and to_num != '':
            num_consecutive_slow = 4
            cnt_below_threshold = 0
            sum_speed = 0
            avg_speed = 0
            select = "SELECT down_speed FROM speedtestresults ORDER BY id DESC LIMIT " + str(num_consecutive_slow)
            conn = sqlite3.connect(db_location)
            cursor = conn.execute(select)
            for row in cursor:
                print ("DOWN SPEED = ", row[0])
                if row[0] < min_down_speed:
                    cnt_below_threshold += 1
                sum_speed += row[0]
            conn.close()
            avg_speed = sum_speed / num_consecutive_slow

            if cnt_below_threshold == num_consecutive_slow:
                print ("SENDING NOTIFICATION")
                notifier = Notifier()
                dateNow = datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S")
                msg = str(num_consecutive_slow) + " CONSECUTIVE SLOW SPEED RESULTS AT " + str(dateNow) + ".  AVG SPEED " + str(round(avg_speed,2)) + "Mbps"
                notifier.send_sms_alert(msg)
            else:
                print ("SPEEDS WITHIN ACCEPTABLE RANGE")

if __name__ == "__main__":
    main(sys.argv[1:])
