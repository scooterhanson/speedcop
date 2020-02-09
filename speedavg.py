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
    try:
        opts, args = getopt.getopt(argv,"ha:t:F:T:d:",["account=","token=","from=","to=","db_location="])
    except getopt.GetoptError:
        print 'speedavg.py -a <account> -t <token> -F <from> -T <to> -d <db location>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'speedavg.py -a <account> -t <token> -F <from> -T <to> -d <db location>'
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

        if db_location != '' and account != '' and token != '' and from_num != '' and to_num != '':
            num_speeds = 0
            sum_speed = 0
            avg_speed = 0
            select = "SELECT down_speed FROM speedtestresults WHERE date(Timestamp,'localtime') >= date('now','localtime','start of day')"
            conn = sqlite3.connect(db_location)
            cursor = conn.execute(select)
            for row in cursor:
                num_speeds += 1
                sum_speed += row[0]
            conn.close()
            avg_speed = round(sum_speed / num_speeds,2)

            dateNow = datetime.datetime.now().strftime("%m-%d-%y")
            msg = "AVERAGE SPEED FOR " + str(dateNow) + " WAS " + str(avg_speed) + "Mbps"
            notifier = Notifier(account, token, from_num, to_num)
            notifier.send_sms_alert(msg)


if __name__ == "__main__":
    main(sys.argv[1:])
