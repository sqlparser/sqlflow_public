#!/bin/bash 

bindir=$(cd `dirname $0`; pwd)

pidtotal=$(ps -ef|grep monitor.sh|grep -v grep|wc -l) 
if [ -e $bindir -a $pidtotal -eq 1 ]; then 
   pid=$(ps -ef|grep -v grep|grep monitor.sh|awk '{print $2}') 
   kill -9 $pid 
   echo stop sqlflow service monitor
fi 

pidtotal=$(ps -ef|grep gspLive.jar|grep -v grep|wc -l) 
if [ -e $bindir -a $pidtotal -eq 1 ]; then 
   pid=$(ps -ef|grep -v grep|grep gspLive.jar|awk '{print $2}') 
   kill -9 $pid 
   echo stop gspLive
fi 

pidtotal=$(ps -ef|grep eureka.jar|grep -v grep|wc -l) 
if [ -e $bindir -a $pidtotal -eq 1 ]; then 
   pid=$(ps -ef|grep -v grep|grep eureka.jar|awk '{print $2}') 
   kill -9 $pid 
   echo stop eureka
fi 

pidtotal=$(ps -ef|grep sqlservice.jar|grep -v grep|wc -l) 
if [ -e $bindir -a $pidtotal -eq 1 ]; then 
   pid=$(ps -ef|grep -v grep|grep sqlservice.jar|awk '{print $2}') 
   kill -9 $pid 
   echo stop sqlservice
fi 

exit
