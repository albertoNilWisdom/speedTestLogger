import speedtest
import json
from datetime import datetime
import urllib
import os
from kafka import KafkaProducer

topicName = 'speedTest'
kafkaServer = 'localhost:9092'

producer = KafkaProducer(bootstrap_servers=kafkaServer)

test = speedtest.Speedtest()

test.get_servers()#get list of servers
best = test.get_best_server()#get best server
download_result = test.download()
upload_result = test.upload()
ping_result = test.results.ping
host = best['host']
country = best['country']
config = test.get_config()

download_resultMb = int(download_result / 1024 / 1024)
upload_resultMb = int(upload_result / 1024 / 1024)
isp = config['client']['isp']

resultsDictionary = {
        "host":str(host),
        "country":str(country),
        "isp":str(isp),
        "ping":str(ping_result),
        "download":str(download_resultMb),
        "upload":str(upload_resultMb),
        "datetime":str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
}
resultsJson = json.dumps(resultsDictionary)

producer.send(topicName,  resultsJson.encode('utf-8'))
producer.flush()
