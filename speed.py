from __future__ import division
import getopt
import json
import sqlite3
import subprocess
import sys


def main(argv):
    db_location = ''
    speedtest_server_id = ''
    try:
        opts, args = getopt.getopt(argv,"hLs:d:",["speedtest_server_id=","db_location="])
    except getopt.GetoptError:
        print 'speed.py -s <server id> -d <db location>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'speed.py -s <server id> -d <db location>'
            sys.exit()
        elif opt == '-L':
            serverlist_cmd = "/usr/local/bin/speedtest -L"
            output = subprocess.check_output(serverlist_cmd, shell=True)
            print output
        elif opt in ("-s", "--server"):
            speedtest_server_id = arg
        elif opt in ("-d", "--dblocation"):
            db_location = arg

    if (db_location != '') and (speedtest_server_id != ''):
        speedtest_cmd = "/usr/local/bin/speedtest --format=json --server-id=" + speedtest_server_id

        output = subprocess.check_output(speedtest_cmd, shell=True)
        obj = json.loads(output.decode('utf-8'))

        up_bytes = obj["upload"]["bytes"]
        up_bits = up_bytes * 8
        up_elapsed = obj["upload"]["elapsed"] / 1000
        up_bps = up_bits / up_elapsed
        up_Mbps = str(round(up_bps / 1000000, 2))

        down_bytes = obj["download"]["bytes"]
        down_bits = down_bytes * 8
        down_elapsed = obj["download"]["elapsed"] / 1000
        down_bps = down_bits / down_elapsed
        down_Mbps = str(round(down_bps / 1000000, 2))
 
        ping_jitter = str(round(obj["ping"]["jitter"], 2))
        ping_latency= str(round(obj["ping"]["latency"],2))

        print ("DOWN - " + down_Mbps + "Mbps")
        print ("UP - " + up_Mbps + "Mbps")
        print ("LATENCY - " + ping_latency + "ms")
        print ("JITTER - " + ping_jitter + "ms")
  
        conn = sqlite3.connect(db_location)
        conn.execute("INSERT INTO speedtestresults (up_speed, down_speed, ping_latency, ping_jitter) \
                VALUES (" + up_Mbps + ", " + down_Mbps + ", " + ping_latency + ", " + ping_jitter + " )");
        conn.commit()
        conn.close()

if __name__ == "__main__":
    main(sys.argv[1:])


