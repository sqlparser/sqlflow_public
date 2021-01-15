#!/bin/bash 

memory=$(cat /proc/meminfo |awk '($1 == "MemTotal:"){print $2}')  

if (( $memory < 8*1024*1024 )); 
  then 
    heapsize="4g" 
elif (( $memory < 16*1024*1024 ));
  then 
    heapsize="10g"
elif (( $memory < 32*1024*1024 ));
  then 
    heapsize="24g"
elif (( $memory < 64*1024*1024 ));
  then 
    heapsize="31g"
else 
  heapsize="118g"
fi

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
