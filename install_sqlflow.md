## Instructions on how to install SQLFlow on your own server.

SQLFow was comprised of two parts: frontend and backend. 
The frontend and backend can be installed on the same server, or they can be installed on two different servers seperately.

### Prerequisites
- A linux server with at least 8GB memory (ubuntu 20.04 is recommended).
- Java 8
- Nginx web server. 
- Port needs to be opened. (80, 8761,8081,8083. Only 80 port need to be opened if you setup the nginx reverse proxy as mentioned in the below)

### Setup Environment (Ubuntu for example)
	sudo apt-get update
	sudo apt-get install nginx -y
	sudo apt-get install default-jre -y	

CentOS
- [How To Install Nginx on CentOS](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-centos-7)
- [How To Install Java on CentOS ](https://www.digitalocean.com/community/tutorials/how-to-install-java-on-centos-and-fedora)

Windows
- [Install SQLFlow on Windows](install_sqlflow_on_windows.md)

### Upload Files

create a directory :

```bash
# it must be created start with root path
sudo mkdir -p /wings/sqlflow
```

upload your backend and frontend file to `sqlflow` folder, like this :

```
/wings/
└── sqlflow
    ├── backend
    │   ├── bin
    │   │   ├── backend.sh
    │   │   ├── stop.sh
    │   │   ├── monitor.sh 
    │   │   ├── sqlservice.sh 
    │   │   ├── gspLive.sh  
    │   │   ├── eureka.sh
    │   │   ├── backend.bat
    │   │   ├── stop.bat
    │   │   ├── monitor.bat
    │   │   ├── sqlservice.bat
    │   │   ├── gspLive.bat
    │   │   ├── eureka.bat
    │   │   ├── sqlservice.vbs
    │   │   ├── gspLive.vbs  
    │   │   ├── eureka.vbs
    │   ├── lib
    │   │   ├── sqlservice.jar  
    │   │   ├── gspLive.jar  
    │   │   ├── eureka.jar
    │   ├── conf
    │   │   ├── gudu_sqlflow_license.txt     
    │   │   ├── gudu_sqlflow.conf     
    │   ├── data
    │   │   ├── job  
    │   │   │   ├── task     
    │   │   │   ├── {userid}   
    │   │   ├── session     
    │   ├── log
    │   │   ├── sqlservice.log 
    │   │   ├── gspLive.log  
    │   │   ├── eureka.log 
    │   │   ├── slow                   (slow query records)
    │   │   ├── sqlflow                (sqlflow access records)
    │   ├── tmp
    │   │   └── cache  
    └── frontend
        ├── 1.app.b95fd285b4e8a1af563a.js
        ├── 1.index.b95fd285b4e8a1af563a.css
        ├── app.b95fd285b4e8a1af563a.js
        ├── config.private.json
        ├── font
        │   ├── Roboto-Regular.ttf
        │   ├── segoeui-light.woff2
        │   └── segoeui-semilight.woff2
        ├── images
        │   ├── check.svg
        │   ├── Join.svg
        │   ├── pic_Not logged in.png
        │   └── visualize.svg
        ├── index.b95fd285b4e8a1af563a.css
        └── index.html
```

set folder permissions :

```bash
sudo chmod -R 755 /wings/sqlflow
```

### Start Backend Services

start service in background: 

```bash
  /wings/sqlflow/backend/bin/backend.sh
```

please allow 1-2 minutes to start the service.

use `ps -ef|grep java` to check those 3 processing are running.

```
ubuntu   11047     1  0 Nov02 ?        00:04:44 java -server -jar eureka.jar
ubuntu   11076     1  0 Nov02 ?        00:04:11 java -server -Xmn512m -Xms2g -Xmx2g -Djavax.accessibility.assistive_technologies=  -jar sqlservice.jar
ubuntu   11114     1  0 Nov02 ?        00:05:17 java -server -jar gspLive.jar
```

#### Java service port

| File           | Port |
| -------------- | ---- |
| eureka.jar     | 8761 |
| gspLive.jar    | 8081 |
| sqlservice.jar | 8083 |

### Nginx Reverse Proxy

If we set the reverse proxy path of gspLive restful service to /api

**1. Config Nginx**

open your nginx configuration file ( at `/etc/nginx/sites-available/default` under ubuntu ), add a server :

```nginx
server {
	listen 80 default_server;
	listen [::]:80 default_server;

	root /wings/sqlflow/frontend/;
	index index.html;

	location ~* ^/index.html {
		add_header X-Frame-Options deny; # remove this line if you want embed sqlflow in iframe
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

**2. modify frontend configuration file config.private.json**

- Open the configration file "/wings/sqlflow/frontend/config.private.json"
- Modify the **ApiPrefix** attribute
```
  "ApiPrefix": "/api"
```

### Start Frontend Services

start your nginx : 

```bash
sudo service nginx start
```

or reload : 

```bash
sudo nginx -s reload
```

open http://yourdomain.com/ to see the SQLFlow.

open http://yourdomain.com/api/gspLive_backend/doc.html?lang=en to see the Restful API documention.

### Sqlflow client api call

See [sqlflow client api call][1]

1. Get userId from gudu_sqlflow.conf
  - Open the configration file "/wings/sqlflow/backend/conf/gudu_sqlflow.conf"
  - The value of anonymous_user_id field is webapi userId
  ```bash
    anonymous_user_id=xxx
  ```
  - **Note:** on-promise mode, webapi call doesn't need the token parameter
  
2. Test webapi by curl
    
    * test sql:
    ```sql
      select name from user
    ```
    
    * curl command:
    ```bash
      curl -X POST "http://yourdomain.com/api/gspLive_backend/sqlflow/generation/sqlflow" -H "accept:application/json;charset=utf-8" -F "userId=YOUR USER ID HERE" -F  "dbvendor=dbvoracle" -F "sqltext=select name from user"
      ```
      
    * response: 
    ```json
      {
        "code": 200,
        "data": {
          "dbvendor": "dbvoracle",
          "dbobjs": [
            ...
          ],
          "relations": [
            ...
          ]
        },
        "sessionId": ...
      }
    ```
    * If the code returns **401**, please check the userId is set or the userId is valid.
  

[1]: https://github.com/sqlparser/sqlflow_public/blob/master/api/sqlflow_api_full.md#webapi
