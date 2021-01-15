@echo off

setlocal enabledelayedexpansion

for /f  %%a in ('jps -l ^| findstr gspLive.jar') do taskkill /f /pid %%a

ping 1.1.1.1 -n 1 -w 2000 > nul

for /F "skip=1" %%I in ('%SystemRoot%\System32\wbem\wmic.exe OS Get TotalVisibleMemorySize') do (
   set "memory=%%I"
   goto BelowLoop
)

:BelowLoop

if %memory% LSS 9000000 (set heapsize=2g) else if %memory% LSS 17000000  (set heapsize=3g) else if %memory% LSS 33000000 (set heapsize=4g) else if %memory% LSS 65000000 (set heapsize=8g) else (set heapsize=8g)

if "%1" equ "" (
	set gudusoft=0
	set cros=
) else (
	if "%1"=="1" (
		set gudusoft=1 
		set cros=--cros.allowedOrigins=https://gudusoft.com,https://www.gudusoft.com,https://sqlflow.gudusoft.com,http://sqlflow.gudusoft.com,https://api.gudusoft.com,http://gudusoft.com,http://api.gudusoft.com,http://www.gudusoft.com,http://157.230.132.40
	) else (
		set gudusoft=0
	    set cros=	
	)
)

if "%2" neq "" (
	set cros=--cros.allowedOrigins=%2
)

set bindir=%~dp0

cd /d %bindir%

if exist ..\lib\gspLive.jar (
   echo Start gspLive, please don't close this window.
   java -server -Xms%heapsize% -Xmx%heapsize% -jar ..\lib\gspLive.jar %cros%
) else (
   echo %bindir%\..\lib\gspLive.jar is not exist!
   pause
)