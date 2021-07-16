#!/usr/bin/python3.8
import twisted.web.http
from twisted.internet import reactor
from twisted.web import proxy, http
import warnings
import mysql.connector
import requests
from requests import get
import dns.resolver
import os, signal, sys
from os import system
import csv
import socket
from colorama import init
from termcolor import colored
from psutil import process_iter
from signal import SIGTERM
import time
import logging
import re

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
localIP = s.getsockname()[0]
s.close()

# create logger1
formatter = logging.Formatter("%(asctime)s,%(message)s", datefmt='%d-%b-%y_%H:%M:%S')
formatter2 = logging.Formatter(f"%(asctime)s,{localIP},%(message)s", datefmt='%d-%b-%y_%H:%M:%S')

logger1 = logging.getLogger('logger1')
logger1.setLevel(logging.INFO)
ch = logging.FileHandler("logs.log", mode='a')
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger1.addHandler(ch)

#create logger2
logger2 = logging.getLogger('logger2')
logger2.setLevel(logging.INFO)
ch2 = logging.FileHandler("logData.log", mode='a')
ch2.setLevel(logging.INFO)
ch2.setFormatter(formatter2)
logger2.addHandler(ch2)

init()
clear = lambda: system('clear')

def signalHandler(signal, frame):
    print("\nCTRL+C PRESSED")
    open("logs.log", 'w').close()
    open("logData.log", 'w').close()
    for proc in process_iter():
        for conns in proc.connections(kind='inet'):
            if conns.laddr.port == 8080:
                proc.send_signal(SIGTERM)


signal.signal(signal.SIGINT, signalHandler)


myDB = mysql.connector.connect(
    host="192.168.100.50",
    user="root",
    passwd="root",
    database="licenta"
)
myDBcursor = myDB.cursor()

dnsResolver = dns.resolver.Resolver()
dnsResolver.nameservers = ['8.8.8.8']
# dnsResolver.lifetime = 1
# dnsResolver.timeout = 0.5

warnings.filterwarnings("ignore", category=DeprecationWarning)
BLACK_LIST = []

domainHistory=["@**@"] * 2


class LoggingProxyRequest(proxy.ProxyRequest):
    def process(self):
        if str(self.getAllHeaders()[b"host"].decode('utf-8')) in BLACK_LIST:
            if str(self.getAllHeaders()[b"host"].decode('utf-8')) not in domainHistory:
                print(colored(str(localIP), 'green')+ " IS_TRYING_TO_ACCESS "
                      + colored(str(self.getAllHeaders()[b"host"].decode('utf-8')), 'green')
                      + colored(" (MALITIOUS_DOMAIN)", 'red'))

                logger1.info("%s", str(localIP) + ",IS_TRYING_TO_ACCESS,"
                             + str(self.getAllHeaders()[b"host"].decode('utf-8'))
                             + ",(MALITIOUS_DOMAIN)")

                duration = 0.4 #sec
                freq = 440  # Hz
                os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
                if len(domainHistory) == 0:
                    domainHistoryLen = 0
                    domainHistory[domainHistoryLen] = str(self.getAllHeaders()[b"host"].decode('utf-8'))
                    domainHistoryLen += 1
                elif len(domainHistory) == 1:
                    domainHistory[domainHistoryLen] = str(self.getAllHeaders()[b"host"].decode('utf-8'))
                    domainHistoryLen += 1
                elif len(domainHistory) == 2:
                    domainHistoryLen = 0
                    domainHistory[domainHistoryLen] = str(self.getAllHeaders()[b"host"].decode('utf-8'))
            self.transport.loseConnection()
        else:
            if str(self.getAllHeaders()[b"host"].decode('utf-8')) not in domainHistory:
                print(colored(str(localIP), 'green') + " IS_ACCESSING "
                      + colored(str(self.getAllHeaders()[b"host"].decode('utf-8')), 'green'))

                logger1.info("%s", str(localIP) + ",IS_ACCESSING,"
                             + str(self.getAllHeaders()[b"host"].decode('utf-8'))
                             + ",(SAFE_DOMAIN)")
                if len(domainHistory) == 0:
                    domainHistoryLen = 0
                    domainHistory[domainHistoryLen] = str(self.getAllHeaders()[b"host"].decode('utf-8'))
                    domainHistoryLen += 1
                elif len(domainHistory) == 1:
                    domainHistory[domainHistoryLen] = str(self.getAllHeaders()[b"host"].decode('utf-8'))
                    domainHistoryLen += 1
                elif len(domainHistory) == 2:
                    domainHistoryLen = 0
                    domainHistory[domainHistoryLen] = str(self.getAllHeaders()[b"host"].decode('utf-8'))
        try:
            proxy.ProxyRequest.process(self)
        except KeyError:
            pass
            #  For HTTPS connections
            self.transport.loseConnection()

class LoggingProxy(proxy.Proxy):
    requestFactory = LoggingProxyRequest

    def connectionLost(self, reason):
        return None

    def dataReceived(self, data):
        try:
            weird_char1 = '\xfe'
            weird_char2 = '\xBF'
            HTTP_method = data.decode('utf-8').replace('\r\n', ' ').split(' ', 1)[0]
            DATA_send = data.decode('utf-8').replace('\r\n', weird_char1).replace(',', weird_char2)
            DOMAIN = re.findall(r'Host: (.+?)þ',DATA_send)
            logger2.info("%s", HTTP_method + "," + DOMAIN[0] + "," + DATA_send)
        except UnicodeError:
            pass
        return proxy.Proxy.dataReceived(self, data)

class LoggingProxyFactory(http.HTTPFactory):
    def buildProtocol(self, addr):
        return LoggingProxy()


# url1 = "http://www.joewein.net/dl/bl/dom-bl.txt"
# url2 = 'https://feeds.alphasoc.net/ryuk.txt'
url3 = "https://www.botvrij.eu/data/ioclist.hostname.raw"

# response1 = requests.get(url1, stream=True)
# response2 = requests.get(url2, stream=True)
response3 = requests.get(url3, stream=True)

if os.path.exists("/home/ubuntu/Documents/Licenta/FINALE/blackListedDomains.csv"):
    os.remove("/home/ubuntu/Documents/Licenta/FINALE/blackListedDomains.csv")

with open("/home/ubuntu/Documents/Licenta/FINALE/blackListedDomains.csv", "wb") as blackListedDomainsCSV:
    if response3.status_code == 200:
        for chunk in response3.iter_content(chunk_size=1024 * 512):
            blackListedDomainsCSV.write(chunk)
    else:
        print("url3 FAILED")

    # if response2.status_code == 200:
    #     for chunk in response2.iter_content(chunk_size=1024 * 512):
    #         blackListedDomainsCSV.write(chunk)
    # else:
    #     print("url2 FAILED")

    # if response1.status_code == 200:
    #     for chunk in response1.iter_content(chunk_size=1024 * 512):
    #         blackListedDomainsCSV.write(chunk)
    # else:
    #     print("url1 FAILED")

with open("/home/ubuntu/Documents/Licenta/FINALE/blackListedDomains.csv", "r") as blackListedDomainsCSV:
    lines = blackListedDomainsCSV.readlines()
with open("/home/ubuntu/Documents/Licenta/FINALE/blackListedDomains.csv", "w") as blackListedDomainsCSV:
    for line in lines:
        if line[0] != '#':
            blackListedDomainsCSV.write(line)

with open("/home/ubuntu/Documents/Licenta/FINALE/blackListedDomains.csv", "r") as blackListedDomainsCSV:
    blackListedDomainsList = [line.strip() for line in blackListedDomainsCSV]

while True:
    updateCacheInput = input("\nUPDATE cacheDomainsIp ? [y/n]: ")
    if updateCacheInput == 'n':
        if os.path.exists("/home/ubuntu/Documents/Licenta/FINALE/cacheDomainsIp.csv"):
            with open("/home/ubuntu/Documents/Licenta/FINALE/cacheDomainsIp.csv", 'r') as cacheDomainsIp:
                reader = list(csv.reader(cacheDomainsIp, delimiter=','))
                cachedDomainsDict = {}
                for row in reader:
                    cachedDomainsDict.update({row[0]: row[1]})
            break
        else:
            with open("/home/ubuntu/Documents/Licenta/FINALE/cacheDomainsIp.csv", "w") as cacheDomainsIp:
                writer = csv.writer(cacheDomainsIp)
                for r in blackListedDomainsList:
                    try:
                        a_records = dnsResolver.resolve(r, 'A')
                        DST_IP = str(a_records[0].address)
                    except Exception:
                        DST_IP = "DOWN"

                    print(r, DST_IP)
                    writer.writerow([r, DST_IP])
            print("\ncacheDomainsIp NOT FOUND ...")
            print("CREATING & UPDATING cacheDomainsIp ...")
            print("cacheDomainsIp READY, TRY AGAIN ...")
    elif updateCacheInput == 'y':
        with open("/home/ubuntu/Documents/Licenta/FINALE/cacheDomainsIp.csv", "w") as cacheDomainsIp:
            writer = csv.writer(cacheDomainsIp)
            for r in blackListedDomainsList:
                try:
                    a_records = dnsResolver.resolve(r, 'A')
                    DST_IP = str(a_records[0].address)
                except Exception:
                    DST_IP = "DOWN"

                print(r, DST_IP)
                writer.writerow([r, DST_IP])
        print("\ncacheDomainsIp UPDDATED ...")

        if os.path.exists("/home/ubuntu/Documents/Licenta/FINALE/cacheDomainsIp.csv"):
            with open("/home/ubuntu/Documents/Licenta/FINALE/cacheDomainsIp.csv", 'r') as cacheDomainsIp:
                reader = list(csv.reader(cacheDomainsIp, delimiter=','))
                cachedDomainsDict = {}
                for row in reader:
                    cachedDomainsDict.update({row[0]: row[1]})
            break

while True:
    updateDatabaseInput = input("\nUPDATE Database ? [y/n]: ")

    if updateDatabaseInput == 'y':
        try:
            myDBcursor.execute("DROP TABLE domains;")
        except mysql.connector.errors.ProgrammingError:
            pass

        myDBcursor.execute("CREATE TABLE domains"
                           "( id_domain INT AUTO_INCREMENT PRIMARY KEY, domain_name VARCHAR(100), ip VARCHAR(40));")
        for i in cachedDomainsDict.items():
            sql = "INSERT INTO domains (domain_name, IP) VALUES ( %s, %s );"
            myDBcursor.execute(sql, i)

        myDB.commit()
        print("DATABASE READY ...")
        break

    elif updateDatabaseInput == 'n':
        try:
            myDBcursor.execute("SELECT * FROM domains;")
            results = myDBcursor.fetchall()
            if len(results) == 0:
                print("EMPTY TABLE, ADDING DATA ...")
                for i in cachedDomainsDict.items():
                    sql = "INSERT INTO domains (domain_name, IP) VALUES ( %s, %s );"
                    myDBcursor.execute(sql, i)
                myDB.commit()
                print("DATABASE READY ...")

        except mysql.connector.errors.ProgrammingError:
            print("TABLE NOT FOUND ...")
            print("CREATING TABLE, ADDING DATA ...")
            myDBcursor.execute("CREATE TABLE domains"
                               "( id_domain INT AUTO_INCREMENT PRIMARY KEY, domain_name VARCHAR(100), ip VARCHAR(40));")
            for i in cachedDomainsDict.items():
                sql = "INSERT INTO domains (domain_name, IP) VALUES ( %s, %s );"
                myDBcursor.execute(sql, i)
            myDB.commit()
            print("DATABASE READY ...")
        break

for key in cachedDomainsDict.keys():
    BLACK_LIST.append(key)
    BLACK_LIST.append("www." + key)
    BLACK_LIST.append("www." + key + ":443")
    BLACK_LIST.append(key + ":443")

print("\nPROXI ENABLED\n")
time.sleep(1.5)

clear()
myDB.close()
myDBcursor.close()

reactor.listenTCP(8080, LoggingProxyFactory(), interface='localhost')
reactor.run()


