@echo off

setlocal enabledelayedexpansion

for /f  %%a in ('jps -l ^| findstr eureka.jar') do taskkill /f /pid %%a

ping 1.1.1.1 -n 1 -w 2000 > nul

for /F "skip=1" %%I in ('%SystemRoot%\System32\wbem\wmic.exe OS Get TotalVisibleMemorySize') do (
   set "memory=%%I"
   goto BelowLoop
)

:BelowLoop

if %memory% gtr 8388608 (set heapsize=512m) else (set heapsize=256m)

set bindir=%~dp0

cd /d %bindir%

if exist ..\lib\eureka.jar (
   echo Start eureka, please don't close this window.
   java -server -Xms%heapsize% -Xmx%heapsize% -jar ..\lib\eureka.jar %cros%
) else (
   echo %bindir%\..\lib\eureka.jar is not exist!
   pause
)