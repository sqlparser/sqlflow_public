@echo off

echo Try to shutdown and restart sqlflow services...
echo= 

setlocal enabledelayedexpansion

for /f  %%a in ('jps -l ^| findstr eureka.jar') do ( 
    echo shutdown eureka...
    taskkill /f /pid %%a
)

for /f  %%a in ('jps -l ^| findstr sqlservice.jar') do ( 
    echo shutdown sqlservice...
    taskkill /f /pid %%a
)

for /f  %%a in ('jps -l ^| findstr gspLive.jar') do ( 
    echo shutdown gspLive... 
    taskkill /f /pid %%a
)

set bindir=%~dp0

cd /d %bindir%

if exist ..\tmp (
   rd  /s /q ..\tmp
)

echo= 

%bindir%\monitor.bat %1 %2