import logging
#logging.basicConfig(level=logging.INFO)
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)

import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')
import cassandra,io

import json

from datetime import datetime
from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy

try:

    cluster = Cluster([sys.argv[1]])
    session = cluster.connect()
    print('"Successfully connected"')

except:
    print('"Failed to connect"')

"""
try:
    session.set_keyspace('smartship_shore')
    logging.info("Connected with Keyspace done..")
except:
    print("Cannot connect with keyspace...")

try:
    vessels = session.execute("SELECT vessel_no  FROM vessel ")
    logging.info("Querying database done..")

except:
    print("Issues while executing the CQL queries...")

def get_vessels():
    printLine()
    print("======== Vessels Available under this fleet ==========")
    for vessel in vessels:
        print("Vessel_No:"+str(vessel.vessel_no))
"""