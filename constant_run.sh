#!/bin/sh
# Shell script to re-run python script if it stops for whatever reason

COMMAND='python3 app_driver.py'
LOGFILE=./misc/shell-script-logs.txt

writelog() {
  now=`date`
  echo "$now $*" >> $LOGFILE
}

writelog "Starting"
while true ; do
  $COMMAND
  writelog "Exited python script with status $?"
  writelog "Restarting python script"
done