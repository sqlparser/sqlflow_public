#!/bin/bash 

#  less than or equal to 8G recommended
heapsize="4g";

# greater than 8G  recommended
# heapsize="10g"; 

bindir=$(cd `dirname $0`; pwd)

pidtotal=$(ps -ef|grep sqlservice.jar|grep -v grep|wc -l) 
if [ -e $bindir -a $pidtotal -eq 1 ]; then 
   pid=$(ps -ef|grep -v grep|grep sqlservice.jar|awk '{print $2}') 
   kill -9 $pid 
fi 

sleep 1 

cd $bindir
if [ ! -e $bindir/../log ]; then   
	mkdir $bindir/../log
fi 

if [ -f ../lib/sqlservice.jar ]; then 
  nohup java -server -XX:MetaspaceSize=256M -XX:MaxMetaspaceSize=256M -Xms$heapsize -Xmx$heapsize -Xss256k -XX:SurvivorRatio=8 -XX:CMSInitiatingOccupancyFraction=92 -XX:+UseCMSInitiatingOccupancyOnly -XX:+UseConcMarkSweepGC -Djavax.accessibility.assistive_technologies=" " -jar ../lib/sqlservice.jar >/dev/null 2>&1 & 
else
  echo $bindir/../lib/sqlservice.jar is not exist!
fi 

exit
