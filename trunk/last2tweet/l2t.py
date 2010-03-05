#! /usr/bin/env python
# l2t.py
# Alastair Montgomery
#
# Post latest artists listened to from Last.FM to FriendFeed or Twitter
#

import ConfigParser
import feedparser
import friendfeed
import os
import time
import traceback
import twitter
import urllib

#Globals for accessing CFG array
target = 0
ffUser = 1
ffPass = 2
twitUser = 3
twitPass = 4
lastURL = 5
prefix = 6

def readCFG(configFile):
    '''Read the folder locations from the config file'''
    myCFG = []
    try:
        config = ConfigParser.RawConfigParser()
        config.read(configFile)
        myCFG.append(config.get('Options', 'target'))
        myCFG.append(config.get('FriendFeed', 'username'))
        myCFG.append(config.get('FriendFeed', 'password'))
        myCFG.append(config.get('Twitter', 'username'))
        myCFG.append(config.get('Twitter', 'password'))
        myCFG.append(config.get('LastFM', 'url'))
        myCFG.append(config.get('Options','prefix'))
    except:
        print "Problems reading the configuration file"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60            
    return myCFG  

def CompressURL(url):
    '''Compress the URL using to.ly'''
    apiurl = "http://to.ly/api.php?longurl="
    quoted = urllib.quote_plus(url)
    shorturl = urllib.urlopen(apiurl + quoted).read()
    return shorturl

def logFile(filename,value):
    '''Write to a logfile'''
    try:
        myOutput = time.strftime("%Y-%m-%d %H:%M") + " " + value + "\n"
        myLog = open(filename,"a")
        myLog.write(myOutput)
        myLog.close()
    except IOError:
        print "Cannot write to logfile ",filename

def fileRead(filename):
    '''Read from a file'''
    try:
        myFile = open(filename, "r")
        myText = myFile.read()
        myFile.close()
        return myText
    except IOError:
        return "None"

def fileWrite(filename, value):
    '''Write to a file'''
    try:
        myFile = open(filename, "w")
        myFile.write(value)
        myFile.close()
    except IOError:
        print "Error writing to file ",filename

def feedRead(cfgFile):
    '''Reads my Last.FM recent feeds and posts a summary to my FriendFeed/Twitter account'''
    myCFG = readCFG(cfgFile)
    myTracks = myCFG[prefix] + " "
    myArtist = []
    tmpTime = fileRead("time.txt")
    oldTime  = time.strptime("16 Aug 1970","%d %b %Y")
    if tmpTime == "None":
        myTime = time.strptime("16 Aug 1970","%d %b %Y")
    else:
        myTime = time.strptime(tmpTime)
    #print myTime        

    print "Requesting Track Feed"
    myFeed = feedparser.parse(myCFG[lastURL])

    print "Parsing Track Feed"
    for x in range (0,len(myFeed['entries'])):
        #print myFeed['entries'][x]
        rawTime = myFeed['entries'][x].updated_parsed
        if myTime < rawTime:
            if oldTime < rawTime:
                oldTime = rawTime
            title = myFeed['entries'][x].title.replace(u'\u2013','-')
            title = title[:title.find('-')]
            if title.rstrip() not in myArtist:
                myArtist.append(title.rstrip())
    fileWrite("time.txt",time.asctime(oldTime)) 
    print "    Latest Track at ",time.asctime(myTime)
    print "    Number of tracks ",len(myArtist)  
    if len(myArtist) != 0:
        myArtist.sort()
        myTracks += ", ".join(["%s" % (k) for k in myArtist])
        if len(myTracks) > 140:
            myTracks140 = myTracks[:137] + "..."
        else:
            myTracks140 = myTracks
        
        oldTracks = fileRead("tracks.txt")
        
        print "Posting Track Feed"
        if oldTracks != myTracks.encode('ascii', 'replace'):
            if myCFG[target] == "FriendFeed":
                try:
                    session = friendfeed.FriendFeed(auth_nickname=myCFG[ffUser], auth_key=myCFG[ffPass])
                    entry = session.publish_message(myTracks.encode('ascii', 'replace'))    
                    print "Posted new message at ",CompressURL("http://friendfeed.com/e/%s" % entry["id"])
                    fileWrite("tracks.txt",myTracks.encode('ascii', 'replace'))
                    logFile("feedread.log",myTracks.encode('ascii', 'replace'))                            
                except:
                    print "Something went pear shaped"
                    print '-'*60
                    traceback.print_exc(file=sys.stdout)
                    print '-'*60                 
                    sys.exit(2)
            elif myCFG[target] == "Twitter":
                api = twitter.Api(username=myCFG[twitUser],password=myCFG[twitPass],input_encoding=None)
                try:
                    status = api.PostUpdate(myTracks140)
                    print "%s just posted: %s" % (status.user.name, status.text.encode('ascii', 'replace'))
                    fileWrite("tracks.txt",myTracks.encode('ascii', 'replace'))
                    logFile("feedread.log",myTracks.encode('ascii', 'replace'))                
                except UnicodeDecodeError:
                    print "Your message could not be encoded.  Perhaps it contains non-ASCII characters? "
                    sys.exit(2)
            else:
                print "Length     : ",len(myTracks)
                print "Twitter    : ",myTracks140
                print "FriendFeed : ",myTracks
    else:
        print "No new tracks to post"
        logFile("feedread.log","No new tracks to post")
    return myTracks[:140]

if __name__ == "__main__":
    import sys
    if sys.argv[1:]:
        feedRead(sys.argv[1])
    else:
        feedRead("last2twit.cfg")

