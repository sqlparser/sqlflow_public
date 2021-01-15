@echo off

setlocal enabledelayedexpansion

for /f  %%a in ('jps -l ^| findstr sqlservice.jar') do taskkill /f /pid %%a

ping 1.1.1.1 -n 1 -w 2000 > nul

for /F "skip=1" %%I in ('%SystemRoot%\System32\wbem\wmic.exe OS Get TotalVisibleMemorySize') do (
   set "memory=%%I"
   goto BelowLoop
)

:BelowLoop

if %memory% gtr 8388608 (set heapsize=10g) else (set heapsize=4g)

set bindir=%~dp0

cd /d %bindir%

if exist ..\lib\sqlservice.jar (
   echo Start sqlservice, please don't close this window.
   java -server -XX:MetaspaceSize=256M -XX:MaxMetaspaceSize=256M -Xms%heapsize% -Xmx%heapsize% -Xss256k -XX:SurvivorRatio=8 -XX:CMSInitiatingOccupancyFraction=92 -XX:+UseCMSInitiatingOccupancyOnly -XX:+UseConcMarkSweepGC -Djavax.accessibility.assistive_technologies=" " -jar ..\lib\sqlservice.jar 
) else (
   echo %bindir%\..\lib\sqlservice.jar is not exist!
   pause
)