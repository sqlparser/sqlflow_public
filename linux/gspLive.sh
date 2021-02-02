#!/bin/bash

if [ "$1" ];then 
	if (( $1 == 1 )); then 
		gudusoft=1 
		cros="--cros.allowedOrigins=https://gudusoft.com,https://www.gudusoft.com,https://sqlflow.gudusoft.com,http://sqlflow.gudusoft.com,https://api.gudusoft.com,http://gudusoft.com,http://api.gudusoft.com,http://www.gudusoft.com,http://157.230.132.40"
	else 
		gudusoft=0
	        cros=""	
	fi ; 
else 
	gudusoft=0
       	
fi

if [ "$2" ];then
   cros="--cros.allowedOrigins="$2
fi

memory=$(cat /proc/meminfo |awk '($1 == "MemTotal:"){print $2}')  

if (( $memory < 8*1024*1024 )); 
  then 
    heapsize="2g" 
elif (( $memory < 16*1024*1024 ));
  then 
    heapsize="3g"
elif (( $memory < 32*1024*1024 ));
  then 
    heapsize="4g"
elif (( $memory < 64*1024*1024 ));
  then 
    heapsize="8g"
else 
  heapsize="8g"
fi


bindir=$(cd `dirname $0`; pwd)

pidtotal=$(ps -ef|grep gspLive.jar|grep -v grep|wc -l) 
if [ -e $bindir -a $pidtotal -eq 1 ]; then 
   pid=$(ps -ef|grep -v grep|grep gspLive.jar|awk '{print $2}') 
   kill -9 $pid 
fi 

sleep 1 

cd $bindir

if [ ! -e $bindir/../log ]; then   
	mkdir $bindir/../log
fi 

if [ -f ../lib/gspLive.jar ]; then   
  nohup java -server -Xms$heapsize -Xmx$heapsize -jar ../lib/gspLive.jar $cros >/dev/null 2>&1 &
else
  echo $bindir/../lib/gspLive.jar is not exist!
fi   

exit
