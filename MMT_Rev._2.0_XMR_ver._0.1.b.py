# -*- coding: utf-8 -*-

# Modules
# URL
import urllib.request
# JSON
import json
# Scheduler
import schedule
# Date time
import datetime
import time
# Config
import configparser

# Global variable
global Host, Tr_CH
global tmp_file_miner, file_path, file_path_collector

# Name of test files
tmp_file_miner = '1-temp-miner.log'
file_path = '2-info.log'
file_path_collector = '3-collector-info.log'

# Import configuration from file
conf = configparser.RawConfigParser()
conf.read("config")

if conf.has_option("sys","Host"):
    Host = conf.get("sys","Host")

if conf.has_option("sys","Tr_CH"):
    Tr_CH = conf.getint("sys","Tr_CH")

# Function for interaction with XMR-Stak
def get_xmr_stak():
    rig_name_ip_port = list(map(str, Host.split(';')))
    for x,i in enumerate(rig_name_ip_port):
        host_name_ip = i.split('@')
        host_name = host_name_ip[0]
        host_ip = str(host_name_ip[1])
        now = datetime.datetime.now()
        print(now,'-','Request for this host -',host_ip)

        try:
            link = 'http://' + host_ip + '/api.json'
            r = urllib.request.urlopen(link).read()
            string = r.decode('utf8').strip('b')
            data = json.loads(string)
            print(str(datetime.datetime.now()),'-','Result request -',data)
        except:
            data = '{"State":"RIG is OFF"}'
            print(str(datetime.datetime.now()), '-', 'Result request -', data)

        # Write to file
        with open(tmp_file_miner, 'w', encoding='utf-8') as file:
            data_to_file = str(datetime.datetime.now()) + ' - ' + str(data) + '\n'
            file.write(data_to_file)

        # Write to file
        with open(file_path, 'a', encoding='utf-8') as file:
            data_to_file = str(datetime.datetime.now()) + ' - Host name - ' + host_name + ' - Host address - ' + host_ip + ' - ' + str(data )+ '\n'
            file.write(data_to_file)

        # Write to file
        with open(file_path_collector, 'a', encoding='utf-8') as file:
            data_to_file = str(data) + '\n'
            file.write(data_to_file)

# Call function
get_xmr_stak()

# Scheduler for function
schedule.every(Tr_CH).minutes.do(get_xmr_stak)

# Program loop
while True:
    schedule.run_pending()
    time.sleep(1)

