@echo off

setlocal enabledelayedexpansion

for /f  %%a in ('jps -l ^| findstr eureka.jar') do taskkill /f /pid %%a
for /f  %%a in ('jps -l ^| findstr sqlservice.jar') do taskkill /f /pid %%a
for /f  %%a in ('jps -l ^| findstr gspLive.jar') do taskkill /f /pid %%a
for /f  %%a in ('jps -l ^| findstr license.jar') do taskkill /f /pid %%a

echo Stop all sqlflow services.