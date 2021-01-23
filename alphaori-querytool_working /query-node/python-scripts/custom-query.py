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

#query="SELECT company_id FROM company "

#cluster node must be altered daily
cluster = Cluster([sys.argv[2]])
session = cluster.connect()
session.set_keyspace('smartship_shore')
results = session.execute(sys.argv[1])

print("======== Custom Query Results ========")
for result in results:
   print(str(result))

