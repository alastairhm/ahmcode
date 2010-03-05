#-----------------------------------------------------------------------------------------------------------------------------------------------------
# My Library
#-----------------------------------------------------------------------------------------------------------------------------------------------------
import twitter, sys, logging

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
def debug(myString):
    LOG_FILENAME = "logs/debug.log"
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,filemode="w")
    logging.info(myString)    
#-----------------------------------------------------------------------------------------------------------------------------------------------------
def myPrint(myString):
    print myString
#-----------------------------------------------------------------------------------------------------------------------------------------------------
def tweet(tweet,parameters):
    '''Post results to Twitter account'''
    api = twitter.Api(username=parameters[g_user],password=parameters[g_password],input_encoding=None)
    try:
        status = api.PostUpdate(tweet)
    except UnicodeDecodeError:
        myPrint("Your message could not be encoded.  Perhaps it contains non-ASCII characters? ")
        sys.exit(2)    