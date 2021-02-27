#!/bin/sh
# Shell script to re-run python script if it stops for whatever reason
mkdir -p ./misc
COMMAND="python3 app_driver.py"
LOGFILE=./misc/shell-script-logs.txt

writelog() {
  now=`date`
  echo "$now $*" >> $LOGFILE
}

moveoldscript() {
    # If the script fails, move the python script logs to an old folder and denote them by the date the script failed
    curr=`date +%Y-%m-%d.%H:%M:%S`
    MOVECOMMAND="mv ./misc/python-script-logs.txt ./misc/old_python_logs/faildate-$curr.txt"
    # -p flag denotes make dir if doesn't exist otherwise continue ...
    MAKELOGDIR="mkdir -p ./misc/old_python_logs"
    $MAKELOGDIR
    $MOVECOMMAND
}

writelog "Shell script Starting"
while true ; do
  $COMMAND
  writelog "Exited python script with status $?"
  writelog "Restarting python script"
  moveoldscript
done