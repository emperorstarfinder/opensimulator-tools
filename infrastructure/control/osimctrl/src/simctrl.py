#!/usr/bin/python

import os.path
import re
import subprocess
import sys

### CONFIGURE THESE PATHS ###
binaryPath = "/home/opensim/opensim/opensim-current/bin"
pidPath = "/tmp/OpenSim.pid"
componentName = "OpenSim"
screenName = componentName
### END OF CONFIG ###

### UTILITY FUNCTIONS ###
def chdir(dir):
  os.chdir(dir)
  print "Executing chdir to %s" % dir
  
def execCmd(cmd):  
  print "Executing command: %s" % cmd
  output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
  # print "For output got: %s" % output
  return output

def findScreen(screenName):
  screenList = ""
  
  try:
    screenList = getScreenList()
  except subprocess.CalledProcessError as cpe:
    screenList = cpe.output
    
  #print "screenList: %s" % screenList
  return re.search("\s+(\d+\.%s)" % screenName, screenList)
  
def getScreenList():
  return execCmd("screen -list")

### MAIN FUNCTIONS ###
def startComponent():
  if os.path.exists(pidPath):
    print >> sys.stderr, "ERROR: %s PID file %s still present.  Assuming OpenSim has been started already.  If not, please delete this file and retry." % (componentName, pidPath)
    sys.exit(1)
  
  # If PID isn't set then we'll check the screen list.  
  # However, this is a much less perfect mechanism since OpenSimulator may have been started outside screen
  if findScreen(screenName):
    print >> sys.stderr, "ERROR: Screen session named %s for %s already started." % (screenName, componentName)
    sys.exit(1)
    
  chdir(binaryPath)
  
  execCmd("screen -S %s -d -m mono --debug %s.exe" % (screenName, componentName))
  
  screen = findScreen(screenName)
  if screen != None:
    print "%s starting in screen instance %s" % (componentName, screen.group(1))
  else:
    print >> sys.stderr, "ERROR: %s did not start." % componentName
    exit(1)  
  
### SCRIPT ###
if len(sys.argv) < 2 or sys.argv[1] != "start":
  print >> sys.stderr, "Usage: %s start" % sys.argv[0]
  sys.exit(2)
  
startComponent()