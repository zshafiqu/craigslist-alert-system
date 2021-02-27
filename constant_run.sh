#!/bin/sh
# Shell script to re-run python script if it stops for whatever reason

COMMAND='python3 app_driver.py'
LOGFILE=./misc/shell-script-logs.txt

# If the script fails, move the python script logs to an old folder and denote them by the date the script failed
MOVECOMMAND = 'mv ./misc/python-script-logs.txt ./misc/old_logs/python-script-logs-ending-${}.txt'

writelog() {
  now=`date`
  echo "$now $*" >> $LOGFILE
}

moveoldscript() {
    # If the script fails, move the python script logs to an old folder and denote them by the date the script failed
    curr=`date`
    MOVECOMMAND = 'mv ./misc/python-script-logs.txt ./misc/old_logs/python-script-logs-ending-${curr}.txt'
    $MOVECOMMAND
}

writelog "Shell script Starting"
while true ; do
  $COMMAND
  writelog "Exited python script with status $?"
  writelog "Restarting python script"
  moveoldscript
done