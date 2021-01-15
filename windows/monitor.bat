@echo off

setlocal enabledelayedexpansion

echo start sqlflow service monitor, please don't close this window

:loop 

set bindir=%~dp0

cd /d %bindir%

set eurekaPid=
for /f  %%a in ('jps -l ^| findstr eureka.jar') do (set eurekaPid=%%a)
if "%eurekaPid%" equ "" (
    echo start eureka...
    start %bindir%\eureka.vbs
)

set sqlservicePid=
for /f  %%a in ('jps -l ^| findstr sqlservice.jar') do (set sqlservicePid=%%a)
if "%sqlservicePid%" equ "" (
    echo start sqlservice...
    start %bindir%\sqlservice.vbs
)

set gspLivePid=
for /f  %%a in ('jps -l ^| findstr gspLive.jar') do (set gspLivePid=%%a)
if "%gspLivePid%" equ "" (
    echo start gspLive...
    start %bindir%\gspLive.vbs %1 %2 
)

ping -n 15 127.0.0.1>nul

goto loop