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


Mac
- [Install SQLFlow on Mac](install_sqlflow_on_mac.md)

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

### Backend Services Configuration

sqlflow provides several optioins to control the service analysis logic. Open the sqlservice configuration file(conf/gudu_sqlflow.conf)

* **relation_limit**:  default value is 2000. When the count of selected object relations is greater than relation_limit, sqlflow will fallback to the simple mode, ignore all the record sets. If the relations of simple mode are still greater than relation_limit, sqlflow will only show the summary information.
* **big_sql_size**: default value is 4096. If the sql length is greater than big_sql_size, sqlflow submit the sql in the work queue and execute it. If the work queue is full, sqlflow throws an exception and return error message "Sorry, the service is busy. Please try again later."

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

#### Modify java service port
In the bash files, `sqlservice.sh, gspLive.sh, eureka.sh` (or `sqlservice.bat, gspLive.bat, eureka.bat`), the services are started by the java command like this:
```sh
java -server -Xms%heapsize% -Xmx%heapsize% -jar ..\lib\gspLive.jar %cros% 
```

We can modify the service port via two ways:
* Application main argument (--server.port)
```sh
java -server -Xms%heapsize% -Xmx%heapsize% -jar ..\lib\gspLive.jar --server.port=8081 %cros% 
```
* JVM argument (-Dserver.port)
```sh
java -server -Xms%heapsize% -Xmx%heapsize% -Dserver.port=8081 -jar ..\lib\gspLive.jar %cros% 
```

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
note that `8081` in `proxy_pass http://127.0.0.1:8081/` should be the same as gspLive.jar's port.

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
OR 

open http://yourdomain.com:8081/gspLive_backend/doc.html?lang=en to see the Restful API documention.

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
