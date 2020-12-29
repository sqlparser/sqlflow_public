#!/bin/bash

#  less than or equal to 8G recommended
heapsize="2g";

# greater than 8G  recommended
# heapsize="3g"; 

if [ "$1" ];then 
	if (( $1 == 1 )); then 
		gudusoft=1 
		cros="--cros.allowedOrigins=https://gudusoft.com,https://www.gudusoft.com,https://api.gudusoft.com,https://sqlflow.gudusoft.com,http://gudusoft.com,http://api.gudusoft.com,http://sqlflow.gudusoft.com,http://www.gudusoft.com,http://66.228.46.41"
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
