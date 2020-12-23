### Prerequisites
- install JDK1.8 or higher  
   SET JAVA_HOME variable, and then add %JAVA_HOME%\bin to the path variable

- install Nginx for windows
	Download the Nginx Windows version here: http://nginx.org/en/docs/windows.html

### unzip SQLFlow file
- create a dirctory: c:\wings\sqlflow
- unzip SQLFlow install package to c:\wings\sqlflow, you will get 2 directories like: 
	1. c:\wings\sqlflow\backend 
	2. c:\wings\sqlflow\frontend


### start SQLFlow backend
- Open a dos command windows
- cd c:\wings\sqlflow\backend\bin
- run monitor.bat
- please wait 3-5 minutes to allow the SQLFlow service to start completely.

### Nginx Reverse Proxy

If we set the reverse proxy path of gspLive restful service to /api

**1. config Nginx**
- enter conf directory where Nginx is installed such as Nginx-1.19.4\conf
- modify the Nginx.conf, replace the server section in nginx.conf with the following code:
```
	server {

		listen 80 default_server;

		listen [::]:80 default_server;

		root C:\wings\sqlflow\frontend;

		index index.html;
		
		location ~* ^/index.html {
			add_header X-Frame-Options deny;
			add_header Cache-Control no-store;
		}

		location / {
			try_files $uri $uri/ =404;
		}
	
		location /api/ {
			proxy_pass http://127.0.0.1:8081/;
			proxy_connect_timeout 600s ;
			proxy_read_timeout 600s;
			proxy_send_timeout 600s;
		
			proxy_set_header Host $host;
			proxy_set_header X-Real-IP $remote_addr;
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			proxy_set_header User-Agent $http_user_agent;  
		}
	}
	
```

Please make sure `C:\wings\sqlflow\frontend` is where the SQLFlow frontend is installed, 
otherwise, please change `C:\wings\sqlflow\frontend` to the path where the SQLFlow frontend is located.

**2. modify frontend configuration file config.private.json**

- Open the configration file "C:\wings\sqlflow\frontend\config.private.json"
- Modify the **ApiPrefix** attribute
```
  "ApiPrefix": "/api"
```

### start Nginx
- Open a dos command window
- cd the directory where Nginx is installed
- run just nginx.exe

### SQLFlow is ready
Just Open the browser and enter the localhost or IP where the SQLFlow is installed.

open http://yourIp/ to see the SQLFlow.

open http://yourIp/api/gspLive_backend/doc.html?lang=en to see the Restful API documention.

### stop the SQLFlow
- close the window where the monitor.sh is running.
- cd c:\wings\sqlflow\backend\bin
- run stop.bat

### troubleshooting
- make sure the window hostname doesn't include the underscore symbol (_), otherwise, the service will not work properly.
	please change it to minus symbol (-)
