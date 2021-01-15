#!/bin/bash 

bindir=$(cd `dirname $0`; pwd)
cd $bindir

while true;do
	pidtotal=$(ps -ef|grep eureka.jar|grep -v grep|wc -l)
	if [ $pidtotal -eq 0 ]; then 
	   ./eureka.sh  
	fi

	pidtotal=$(ps -ef|grep sqlservice.jar|grep -v grep|wc -l)
	if [ $pidtotal -eq 0 ]; then 
	   ./sqlservice.sh  
	fi

	pidtotal=$(ps -ef|grep gspLive.jar|grep -v grep|wc -l)
	if [ $pidtotal -eq 0 ]; then 
	   ./gspLive.sh $1 $2 
	fi

	
sleep 5
done
