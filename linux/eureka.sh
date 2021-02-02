#!/bin/bash

memory=$(cat /proc/meminfo |awk '($1 == "MemTotal:"){print $2}')
if (( $memory < 8*1024*1024 )); then heapsize="256m"; else heapsize="512m"; fi

bindir=$(cd `dirname $0`; pwd)

pidtotal=$(ps -ef|grep eureka.jar|grep -v grep|wc -l) 
if [ -e $bindir -a $pidtotal -eq 1 ]; then 
   pid=$(ps -ef|grep -v grep|grep eureka.jar|awk '{print $2}') 
   kill -9 $pid 
fi 

sleep 1 

cd $bindir

if [ ! -e $bindir/../log ]; then   
	mkdir $bindir/../log
fi 

if [ -f ../lib/eureka.jar ]; then 
  nohup java -Xms$heapsize -Xmx$heapsize -server -jar ../lib/eureka.jar >/dev/null 2>&1 & 
else
  echo $bindir/../lib/eureka.jar is not exist!
fi  

exit
