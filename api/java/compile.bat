@ECHO OFF
SETLOCAL enableDelayedExpansion

SET cur_dir=%CD%
echo %cur_dir%

SET qddemo=%cur_dir%

SET qddemo_src=%qddemo%\src
SET qddemo_bin=%qddemo%\lib
SET qddemo_class=%qddemo%\class

echo %qddemo_class%
echo %qddemo_bin%

IF EXIST %qddemo_class%	RMDIR %qddemo_class%
IF NOT EXIST %qddemo_class%  MKDIR %qddemo_class%

cd %cur_dir%
CD %qddemo_src%
FOR /R %%b IN ( . ) DO (
IF EXIST %%b/*.java  SET JFILES=!JFILES! %%b/*.java
)

MKDIR %qddemo_class%\lib
XCOPY  %qddemo_bin%  %qddemo_class%\lib
XCOPY  %qddemo%\MANIFEST.MF  %qddemo_class%

cd %cur_dir%

    javac -d %qddemo_class% -encoding utf-8 -cp .;%qddemo_bin%\commons-codec-1.10.jar;%qddemo_bin%\commons-logging-1.2.jar;%qddemo_bin%\fastjson-1.2.47.jar;%qddemo_bin%\httpclient-4.5.5.jar;%qddemo_bin%\httpcore-4.4.9.jar;%qddemo_bin%\httpmime-4.5.6.jar; %JFILES%

cd %qddemo_class%
    jar -cvfm %qddemo%\grabit-java.jar %qddemo%\MANIFEST-windwos.MF *

echo "successfully"

pause