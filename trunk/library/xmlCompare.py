#-----------------------------------------------------------------------------------------------------------------------------------------------------
# Quick and dirty XML compare
#-----------------------------------------------------------------------------------------------------------------------------------------------------
import os, time, urllib, string, filecmp
import sys, difflib, xml.dom.minidom, pprint, traceback

from myLib import *
from IOfunctions import *
from xml.etree.ElementTree import ElementTree

#Globals for CFG array
g_bench = 0
g_output = 1
g_compare = 2
g_mismatch = 3
g_logs = 4
g_editor = 5
g_build = 6
g_twitter = 7
g_user = 8
g_password = 9
g_delay = 10
g_codestream = 11

#-----------------------------------------------------------------------------------------------------------------------------------------------------
def treeCompare(file1,file2):
    flag = False
    
    tree = ElementTree()
    tree.parse(file1)
    #Try to find PublishRespose
    p = tree.find("PublishResponse")
    if p != None:
        r = p.getiterator("ResolvedContent")
        
        btree = ElementTree()
        btree.parse(file2)
        pb = btree.find("PublishResponse")
        rb = pb.getiterator("ResolvedContent")
        
        for loop in range(0,len(r)):
            debug("Loop %d" % (loop))
            if r[0].text == rb[0].text:
                debug("Publish True")
                flag = True
            else:
                debug("Publish False "+file1)
                flag = False
    else:
        p = tree.find("SearchResponse")
        if p != None:
            r = p.getiterator("SearchResults")
            
            btree = ElementTree()
            btree.parse(file2)
            pb = btree.find("SearchResponse")
            rb = pb.getiterator("SearchResults")

            for loop in range(0,len(r)):
                debug("Loop %d" % (loop))
                if r[0].text == rb[0].text:
                    debug("Search True")
                    flag = True
                else:
                    debug("Search False "+file1)
                    flag = False
        else:
                debug("Unable understand response file "+file1)
    return flag
#-----------------------------------------------------------------------------------------------------------------------------------------------------
def junkemptylines(temp):
    '''Remove blank or whitespace lines'''
    textA = []
    for text in temp:
        text = text.rstrip()
        if len(text):
            textA.append(text)
    return textA
#-----------------------------------------------------------------------------------------------------------------------------------------------------
def dirtyXMLCompare(file1,file2):
    '''Quick and dirty XML file compare'''
    try:
        domA = xml.dom.minidom.parse(file1)
        temp = domA.toprettyxml().splitlines(1)
        textA = junkemptylines(temp)

        domB = xml.dom.minidom.parse(file2)
        temp = domB.toprettyxml().splitlines(1)
        textB = junkemptylines(temp)

        d = difflib.Differ()

        mydiff = list(d.compare(textA, textB))

        thesame = True
        ws_skip = 0

        for line in mydiff:
            if line.find('ErrorResponse id="4024" type="malformedRequest"') > 0:
                #Setup counter to skip the blasted Websphere error message
                ws_skip = 4
            if line.find('version="') > 0:
                #Skip Agility Version Number
                ws_skip = 4
            if ws_skip > 0:
                ws_skip -= 1
                continue
            if line[0] != " ":
                #Ignore differences in query time, etc
                if ignoreDiff(line):
                    thesame = False
        
        if not thesame:
            for line in mydiff:
                #if line[0] != " ":
                line_coded = unicode(line).encode("utf8", "replace")
                logFile(file1[:file1.find(".xml")]+"_diff.txt",line_coded,False)
    except:
        thesame = False
        myPrint("Problems comparing XML files")
        myPrint('-'*60)
        traceback.print_exc(file=sys.stdout)
        myPrint('-'*60)         
    return thesame
#-----------------------------------------------------------------------------------------------------------------------------------------------------
def ignoreDiff(line):
    '''Ignore Differences in Query time, timestamps etc'''
    result = True
    if line.find("executionTime") != -1 or line[0] == "?":
        result = False
    return result
#-----------------------------------------------------------------------------------------------------------------------------------------------------    
def checkDirectories(parameters):
    '''Create the benchmark and output folders if they do not exist'''
    try:
        if not os.path.exists(parameters[g_bench]):
            os.mkdir(parameters[g_bench])
        if not os.path.exists(parameters[g_output]):
            os.mkdir(parameters[g_output])
    except:
        myPrint("Problems with input/ Output folders")
        myPrint('-'*60)
        traceback.print_exc(file=sys.stdout)
        myPrint('-'*60)        
#-----------------------------------------------------------------------------------------------------------------------------------------------------        
def compareResults(resultsFile,compareName,parameters,results,timer,version,multiFlag):
    '''Compare the result file against the benchmark file'''
    resultFilename = os.path.join(parameters[g_output],resultsFile)
    if os.path.exists(resultFilename):
        if version != "Unknown":
            #Check for version specific version of the results
            if multiFlag != 1:
                #Check if need to trim multi run count off filename
                #Multi Run trim the count
                tmpTxt = resultsFile[:resultsFile.find("_res")+4]+".xml"
            else:
                #Single Run
                tmpTxt = resultsFile
            benchmarkFile = os.path.join(parameters[g_bench],tmpTxt[:tmpTxt.find('/')+1]+version+"_"+tmpTxt[tmpTxt.find('/')+1:])
            if os.path.exists(benchmarkFile) == False:
                benchmarkFile = os.path.join(parameters[g_bench],tmpTxt)
        else:
            #Check if need to trim multi run count off filename
            if multiFlag == 1:
                #Single Run
                benchmarkFile = os.path.join(parameters[g_bench],resultsFile)
            else:
                #Multi Run trim the count
                tmpTxt = resultsFile[:resultsFile.find("_res")+4]+".xml"
                benchmarkFile = os.path.join(parameters[g_bench],tmpTxt)
                
        if os.path.exists(benchmarkFile):
            if filecmp.cmp(resultFilename,benchmarkFile,shallow=False) == True:
                logFile(compareName,resultsFile + " same as benchmark response. (%f secs)" %timer,True)
                results[1] = results[1]+1
            else:
                if treeCompare(resultFilename,benchmarkFile):
                    logFile(compareName,resultsFile + " same as benchmark response. (%f secs)" %timer,True)
                    results[1] = results[1]+1                
                else:
                    if dirtyXMLCompare(resultFilename,benchmarkFile):
                        logFile(compareName,resultsFile + " same as benchmark response. (%f secs)" %timer,True)
                        results[1] = results[1]+1
                    else:
                        logFile(compareName,resultsFile + " MISMATCH. (%f secs)" %timer,True)
                        results[2] = results[2]+1
        else:
            logFile(compareName,benchmarkFile + " MISSING. (%f secs)" %timer,True)
            results[2] = results[2]+1
    else:
        logFile(compareName,resultsFile + " MISSSING. (%f secs)" %timer,True)
        results[2] = results[2]+1
#-----------------------------------------------------------------------------------------------------------------------------------------------------