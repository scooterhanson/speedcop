from __future__ import division
import datetime
import getopt
import json
import sqlite3
import subprocess
import sys
import time


def main(argv):
    db_location = ''
    result_limit = 10
    try:
        opts, args = getopt.getopt(argv,"hd:n:",["db_location=","result_limit="])
    except getopt.GetoptError:
        print 'getspeedresults.py -d <db location>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'getspeedresults.py -d <db location>'
            sys.exit()
        elif opt in ("-n", "--num_results"):
            result_limit = arg
        elif opt in ("-d", "--dblocation"):
            db_location = arg

        if db_location != '':
            select = "SELECT down_speed, up_speed, datetime(timestamp,'localtime') FROM speedtestresults ORDER BY id DESC LIMIT " + str(result_limit)
            conn = sqlite3.connect(db_location)
            cursor = conn.execute(select)
            for row in cursor:
                print  (row[0], "Mbps Down  |  ",row[1], "Mbps Up  |  ", row[2])
            conn.close()


if __name__ == "__main__":
    main(sys.argv[1:])

