#! /usr/bin/env bash

logfile='/var/tmp/crawler/crawl.log'
echo 'Start gatherring process'
echo 'Start gatherring process' >> $logfile
echo $(date) 
echo $(date) >> $logfile
~/praxisProjekt/src/FancyName.py >> ~/praxisProjekt/crawlerOutputGathererRun.log &
sleep 6
foldersize=$(du -gc /var/tmp/crawler/ | tail -n 1 | awk '{print $1}')

while [ $foldersize -lt 400 ]
do
sleep 2
foldersize=$(du -gc /var/tmp/crawler/ | tail -n 1 | awk '{print $1}')
done
echo 'reached max foldersize'
echo 'reached max foldersize' >> $logfile
ps -ef | grep FancyName | grep -v grep | awk '{print $2}' | xargs kill
echo 'Process killed'
echo 'Process killed' >> $logfile
echo $(date) 
echo $(date) >> $logfile
