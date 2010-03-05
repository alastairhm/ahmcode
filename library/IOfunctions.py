#-----------------------------------------------------------------------------------------------------------------------------------------------------
# File I/O Functions
#-----------------------------------------------------------------------------------------------------------------------------------------------------
import os
import time
import urllib
import string
import filecmp
import sys, difflib, xml.dom.minidom, pprint, traceback
import ConfigParser
from myLib import myPrint

#-----------------------------------------------------------------------------------------------------------------------------------------------------
def readTests(fileName):
    '''Parse passed file for list of server and xml pairs'''
    xmlEntries = []

    try:
        testFile = open(fileName,"r")

        for line in testFile:
            if line[0] !='#':
                if line[0] == '+':
                    # Add tests from sub file
                    splitList = string.split(line.rstrip(), '\t')
                    xmlEntries = xmlEntries + readTests(splitList[1])
                elif line.find("\t") != -1:
                    splitList = string.split(line.rstrip(), '\t')
                    server = splitList[0]
                    xmlfile = splitList[1]
                    xmlEntries.append((server,xmlfile))
        testFile.close()
        return xmlEntries
    except IOError:
        myPrint("Cannot open test file "+fileName)
        sys.exit(2)
#-----------------------------------------------------------------------------------------------------------------------------------------------------
def logFile(filename,value,timeStamp):
    '''Write (append) to a log file'''
    try:
        if timeStamp:
            myOutput = time.strftime("%Y-%m-%d %H:%M") + " " + value
        else:
            myOutput = value
        myLog = open(filename,"a")
        myLog.write(myOutput+"\n")
        myLog.close()
    except IOError:
        myPrint("Cannot write to logfile "+filename)
#-----------------------------------------------------------------------------------------------------------------------------------------------------
def fileRead(filename):
    '''Read from a file'''
    myText=""
    try:
        myFile = open(filename, "r")
        myText = myFile.read()
        myFile.close()
    except IOError:
        return "None"
    finally:
        return myText
#-----------------------------------------------------------------------------------------------------------------------------------------------------
def fileWrite(filename, value):
    '''Write to a file'''
    try:
        myFile = open(filename, "w")
        myFile.write(value)
    except IOError:
        myPrint("Error writing to file "+filename)
    finally:
        myFile.close()
#-----------------------------------------------------------------------------------------------------------------------------------------------------
def readCFG(configFile):
    '''Read the folder locations from the config file'''
    myDir = []
    try:
        config = ConfigParser.RawConfigParser()
        config.read(configFile)
        myDir.append(config.get('Folders', 'benchmarks'))
        myDir.append(config.get('Folders', 'output'))
        myDir.append(config.get('Options', 'compare'))
        myDir.append(config.get('Options', 'mismatch'))
        myDir.append(config.get('Folders', 'logs'))
        myDir.append(config.get('Options', 'editor'))
        myDir.append(config.get('Options', 'build'))
        myDir.append(config.get('Twitter', 'twitter'))
        myDir.append(config.get('Twitter', 'username'))
        myDir.append(config.get('Twitter', 'password'))
        myDir.append(config.get('Options', 'delay'))        
        myDir.append(config.get('Misc', 'codestream'))
    except:
        myPrint("Problems reading the configuration file")
        myPrint('-'*60)
        traceback.print_exc(file=sys.stdout)
        myPrint('-'*60)
    return myDir 
#-----------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------        