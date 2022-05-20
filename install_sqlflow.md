- [Instructions on how to install SQLFlow on your own server.](#instructions-on-how-to-install-sqlflow-on-your-own-server)
  * [Prerequisites](#prerequisites)
  * [Setup Environment (Ubuntu for example)](#setup-environment--ubuntu-for-example-)
  * [Upload Files](#upload-files)
  * [Nginx Reverse Proxy](#nginx-reverse-proxy)
  * [Customize the port](#customize-the-port)
    + [1. Default port](#1-default-port)
    + [2. Modify the web port](#2-modify-the-web-port)
    + [3. Modify java service port](#3-modify-java-service-port)
  * [Start Backend Services](#start-backend-services)
  * [Start Frontend Services](#start-frontend-services)
  * [Gudu SQLFlow License file](#gudu-sqlflow-license-file)
  * [Backend Services Configuration](#backend-services-configuration)
  * [Sqlflow client api call](#sqlflow-client-api-call)
  * [Trouble Shooting](#trouble-shooting)
    + [1. Failed to get license info.](#1-failed-to-get-license-info)
    + [2. Config nginx on RHEL: Redhat linux](#2-config-nginx-on-rhel-redhat-linux)
    + [3. Get license fail: 502 Bad Gateway](#3-get-license-fail-502-bad-gateway)



# Instructions on how to install SQLFlow on your own server.

SQLFow was comprised of two parts: frontend and backend. 
The frontend and backend can be installed on the same server, or they can be installed on two different servers seperately.

## Prerequisites
- [SQLFlow on-premise version](https://www.gudusoft.com/sqlflow-on-premise-version/)
- A linux server with at least 8GB memory (ubuntu 20.04 is recommended).
- Java 8
- Nginx web server. 
- Port needs to be opened. (80, 8761,8081,8083. Only 80 port need to be opened if you setup the nginx reverse proxy as mentioned in the below)

## Setup Environment (Ubuntu for example)
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

## Upload Files

create a directory :

```bash
# it must be created start with root path
sudo mkdir -p /wings/sqlflow
```

upload your zip file including backend and frontend file to `sqlflow` folder, and unzip like this :
```bash
unzip sqlflow.zip
```

You should get files organized like this:

```
/wings/
└── sqlflow
    ├── backend
    │   ├── bin
    │   │   ├── backend.bat 
    │   │   ├── backend.sh
    │   │   ├── eureka.bat
    │   │   ├── eureka.sh
    │   │   ├── eureka.vbs
    │   │   ├── gspLive.bat
    │   │   ├── gspLive.sh  
    │   │   ├── gspLive.vbs  
    │   │   ├── monitor.bat
    │   │   ├── monitor.sh 
    │   │   ├── sqlservice.bat
    │   │   ├── sqlservice.sh 
    │   │   ├── sqlservice.vbs
    │   │   ├── stop.bat
    │   │   ├── stop.sh
    │   ├── lib
    │   │   ├── eureka.jar
    │   │   ├── gspLive.jar  
    │   │   ├── sqlservice.jar
    │   ├── conf
    │   │   ├── gudu_sqlflow_license.txt     
    │   │   ├── gudu_sqlflow.conf     
    │   ├── data
    │   │   ├── job  
    │   │   │   ├── task     
    │   │   │   ├── {userid}   
    │   │   ├── schema     
    │   │   ├── session     
    │   │   ├── version     
    │   ├── log
    │   ├── tmp
    │   │   └── cache  
    └── frontend
        ├── config.public.json
        ├── images
        │   ├── check.svg
        │   ├── Join.svg
        │   ├── pic_Not logged in.png
        │   └── visualize.svg
        ├── index.********************.css
        ├── index.********************.css
        ├── index.********************.css
        ├── index.********************.css
        └── index.html
        └── lang
        ├── page.*********************.js
        ├── page.*********************.js
        ├── page.*********************.js
        ├── page.*********************.js
        ├── public.*********************.js
        ├── widget
        │   ├── index.js
        │   ├── sqlflow-library.version.css
        │   └── sqlflow-library.version.js
```

set folder permissions :

```bash
sudo chmod -R 755 /wings/sqlflow
```

## Nginx Reverse Proxy

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

`/api` is mapped to `http://127.0.0.1:8081` in the above configration. This is useful if you 
company doesn't allow access `8081` port from the external.

**2. modify frontend configuration file config.private.json**

- Open the configration file "/wings/sqlflow/frontend/config.private.json"
- Modify the **ApiPrefix** attribute
```
  "ApiPrefix": "/api"
```

## Customize the port

If you don't want to change the default service port, just ignore this section,
otherwise, please act as the following instructions.

### 1. Default port
1. Web port is `80`
2. SQLFlow backend service port:

| File           | Port |
| -------------- | ---- |
| eureka.jar     | 8761 |
| gspLive.jar    | 8081 |
| sqlservice.jar | 8083 |

### 2. Modify the web port
Change the default web port from `80` to `9000` (or any port you like).

![sqlflow-install-customize-web-port](/images/sqlflow-install-customize-web-port.png)

### 3. Modify java service port
Change the default gspLive port from `8081` to `9001`(or any port you like).

1. Change the port in nginx config file
![sqlflow-install-customize-gsplive-port-nginx](/images/sqlflow-install-customize-gsplive-port-nginx.png)

2. Change the port in gspLive.sh(gspLive.bat)
![sqlflow-install-customize-port-gsplive](/images/sqlflow-install-customize-port-gsplive.png)


## Start Backend Services

start service in background: 

```bash
  sudo /wings/sqlflow/backend/bin/backend.sh
```

please allow 3-5 minutes to start the service.

use `ps -ef|grep java` to check those 3 processing are running.

```
ubuntu   11047     1  0 Nov02 ?        00:04:44 java -server -jar eureka.jar
ubuntu   11076     1  0 Nov02 ?        00:04:11 java -server -Xmn512m -Xms2g -Xmx2g -Djavax.accessibility.assistive_technologies=  -jar sqlservice.jar
ubuntu   11114     1  0 Nov02 ?        00:05:17 java -server -jar gspLive.jar
```


## Start Frontend Services

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


##  Gudu SQLFlow License file
If this is the first time you setup the Gudu SQLFlow on a new machine,
then, you will see this license UI:
![gudu sqlflow license ui](/images/gudu-sqlflow-license.png)

1. You send us the Gudu SQLFlow Id (6 characters in red).
2. We will generate a license file for you based on this id.
3. You upload the license file by click the "upload license file" link.

## Backend Services Configuration

sqlflow provides several optioins to control the service analysis logic. Open the sqlservice configuration file(conf/gudu_sqlflow.conf)

* **relation_limit**:  default value is 2000. When the count of selected object relations is greater than relation_limit, 
sqlflow will fallback to the simple mode, ignore all the record sets. 
If the relations of simple mode are still greater than relation_limit, sqlflow will only show the summary information.

* **big_sql_size**: default value is 4096. If the sql length is greater than big_sql_size, sqlflow submit the sql in the work queue and execute it. 
If the work queue is full, sqlflow throws an exception and return error message "Sorry, the service is busy. Please try again later."


## Sqlflow client api call

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

## Trouble Shooting
### 1. Failed to get license info.

![sqlflow-install-failed-to-get-license-info](/images/sqlflow-install-failed-to-get-license-info.png)

If you see this error, just wait another 3-5 minutes to wait the backend service startup successfully 
and refresh the web page.

Or, this issue may caused by the browser cache, just use `Incognito mode` to access the Sqlflow page and
clear the cache.


### 2. Config nginx on RHEL: Redhat linux

a) Type: vim /etc/nginx/nginx.conf and change the server section of the conf file with below configurations
```
server {

        listen       80 default_server;

        listen       [::]:80 default_server;

        server_name  _;

        #root         /usr/share/nginx/html;

        root          /wings/sqlflow/frontend/;

        index index.html

        # Load configuration files for the default server block.

        include /etc/nginx/default.d/*.conf;

 

        location / {

                try_files $uri $uri/ =404;

        }

 

        error_page 404 /404.html;

            location = /40x.html {

        }

 

        error_page 500 502 503 504 /50x.html;

            location = /50x.html {

        }

        location ~* ^/index.html {

                 add_header X-Frame-Options deny; # remove this line if you want to embed SQLFlow in iframe

                 add_header Cache-Control no-store;

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

b) Configure selinux to permission by going to: vi /etc/selinux/configure --> SELinux status to = permissive


### 3. Get license fail: 502 Bad Gateway

![gudu sqlflow 502 bad gateway](/images/sqlflow-install-502-bad-gateway.png)

If you find this error, this is because the port that is needed by the SQLFlow is already used by another application,
please configure the SQLFlow to [use another port](#customize-the-port).
