### Prerequisites
- install JDK1.8 or higher  
   SET JAVA_HOME variable, and then add %JAVA_HOME%\bin to the path variable

- install nginx for windows
  Download the nginx windows version here: http://nginx.org/en/docs/windows.html

### unzip SQLFlow file
- create a dirctory: c:\wings\sqlflow
- unzip SQLFlow install package to c:\wings\sqlflow, you will get 2 directories like: 
	1. c:\wings\sqlflow\backend 
	2. c:\wings\sqlflow\frontend


### start SQLFlow backend
- Open a dos command windows
- cd c:\wings\sqlflow\backend\bin
- run monitor.bat
- please wait 3-5 minutes to allow the SQLFlow service start completedly.

### config nginx
- enter conf directory where nginx is installed such as : nginx-1.19.4\conf
- modify the nginx.conf, replace server section in nginx.conf with the following code:
```
	server {

		listen 80 default_server;

		listen [::]:80 default_server;

		root C:\wings\sqlflow\frontend;

		index index.html;

		location ~* ^/index.html {

			​ add_header X-Frame-Options deny;

			​ add_header Cache-Control no-store;

			}

		location / {

		​ 	try_files uriuri/ =404;

			}
	
		}
	
```

Please make sure `C:\wings\sqlflow\frontend` is where the SQLFlow frontend is installed.

### start nginx
- Open a dos command windows
- cd the directory where nginx is installed
- run just nginx.exe

### SQLFlow is ready
Just Open the browse and enter the localhost or IP where the SQLFlow is installed.

### stop the SQLFlow
- close the window where the monitor.sh is running.
- cd c:\wings\sqlflow\backend\bin
- run stop.bat
