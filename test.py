#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
from time import gmtime,strftime
import re
import subprocess 
import threading

WIFI_URL = "http://192.168.0.1"
    
phantomPath="/home/deepanshu/Downloads/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
driver = webdriver.PhantomJS(executable_path=phantomPath,service_log_path=os.path.devnull)

def startListening():
    driver.get(WIFI_URL)
    threading.Timer(60, startListening).start()
    try:
        #clickin Login Button
        driver.find_element_by_id('loginBtn').click()
        #time.sleep(1)
        
        #Switiching to Main Frame
        driver.switch_to.frame("main")
        
        time.sleep(1)
        #clicking Active Client Table Byutton
        driver.find_element_by_link_text("Active Client Table").click()
        #time.sleep(1)
        
        wirelessClientsTable = driver.find_elements_by_class_name('formlisting')[1]
        wirelessClients = re.findall('<td.*><b>(.*)</b></td>',wirelessClientsTable.get_attribute('innerHTML'))
        totalCount = int(len(wirelessClients)/3)
        
        if os.path.exists("/tmp/connectionNotifier.log"):
            newClients = False
            notificationMessage = "New Connections for " + WIFI_URL + "\r\n"
            message=""
            previousClientsList = []
            with open("/tmp/connectionNotifier.log") as logFile:
                previousClients = logFile.readlines()
                
            for client in previousClients:
                    client = client.split("\t")
                    try:
                        previousClientsList.append(client[1].strip('\n'))
                    except:
                        print("No strip")
            #print(previousClientsList)
            for i in range(totalCount):
                message += wirelessClients[i*3] + "\t" + wirelessClients[i*3 + 2] + "\r\n"
                if wirelessClients[i*3+2] not in previousClientsList:
                    newClients = True    
                    notificationMessage += wirelessClients[i*3] + "\t" + wirelessClients[i*3 + 2] + "\r\n"
            logFile = open("/tmp/connectionNotifier.log","w")
            logFile.write(message)
            logFile.close()
            if newClients:
                subprocess.Popen(['notify-send',notificationMessage])
        else:
            message = "New Connections for " + WIFI_URL + "\r\n"  
            logFile = open("/tmp/connectionNotifier.log","w")
            for i in range(totalCount) :
                message += wirelessClients[i*3] + "\t" + wirelessClients[i*3 + 2] + "\r\n"
                logFile.write(wirelessClients[i*3] + "\t" + wirelessClients[i*3 + 2] +  "\r\n")
            subprocess.Popen(['notify-send',message])
            logFile.close()
    except Exception as e:
        print(e)


subprocess.Popen(['notify-send','Wifi Connections Listener started'])
startListening()



    
    

