##https://www.youtube.com/watch?v=sPq8a1MUgr0

import speedtest
import mysql.connector
import datetime
import urllib
import os


with open('/home/db/speedtest/log.txt','a') as log:
	log.write(str(datetime.datetime.now()) + 'Test started\r\n')
	log.close

db = mysql.connector.connect(
	host='127.0.0.1',
	user='ted',
	passwd='',#
	db='JohnLeeWebHooker')
cursor = db.cursor(buffered=True)

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
print(best['host'])
print(best['country'])
print(download_resultMb)
print(upload_resultMb)
print(ping_result)

sql = "INSERT INTO SpeedTest (Download,Upload,ping,ISP,host,country,date,time) VALUES("+str(download_resultMb)+","+str(upload_resultMb)+","+ str(ping_result)+",'"+isp+"','"+best['host']+"','"+best['country'] +"',cast(now() as date), cast(now() as time))"

print(sql)
cursor.execute(sql)
db.commit()
with open('/home/db/speedtest/log.txt','a') as log:
	log.write(str(datetime.datetime.now()) + 'Test ended\r\n')
	log.close
