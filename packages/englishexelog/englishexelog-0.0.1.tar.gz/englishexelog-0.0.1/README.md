# englishexelog

This is a simple python module to log simple messages into Log.log,

Install:
pip install englishexelog

Import:
import englishexelog as log

Usage:
log.log(" OK ", "Loaded!")

log.logfile(" OK ", "Loaded!", "Log.log")

log.logadd("User1", " OK ", "Loaded!")

log.logaddfile("User1", " OK ", "Loaded!", "Log.log")

log.wipe("Log.log")
