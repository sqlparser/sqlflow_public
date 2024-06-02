# Install SQLFlow on your own Mac

SQLFow was comprised of two parts: frontend and backend. The frontend and backend can be installed on the same server, or they can be installed on two different servers seperately.

## Prerequisites
- [SQLFlow on-premise version](https://www.gudusoft.com/sqlflow-on-premise-version/)
- Java 8
- Nginx web server.
- Port needs to be opened. (80, 8761,8081,8083. Only 80 port need to be opened if you setup the nginx reverse proxy as mentioned in the below)
- At least 8GB memory

## Setup Environment

* [Java setup environment link](https://mkyong.com/java/how-to-set-java_home-environment-variable-on-mac-os-x/) 

```
# setup java environment
echo export "JAVA_HOME=\$(/usr/libexec/java_home)" >> ~/.bash_profile
source ~/.bash_profile
```

## Install Nginx

- [How To Install Nginx on Mac](https://medium.com/@ThomasTan/installing-nginx-in-mac-os-x-maverick-with-homebrew-d8867b7e8a5a)

## Upload Files

create a directory :

```
# example you can use other path
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
        │   ├── Roboto-Regular.ttf
        │   ├── segoeui-light.woff2
        │   └── segoeui-semilight.woff2
        ├── images
        │   ├── check.svg
        │   ├── Join.svg
        │   ├── pic_Not logged in.png
        │   └── visualize.svg
        ├── index.b95fd285b4e8a1af563a.css
        └── index.html
```

## set scripts permissions :

```
chmod +x /wings/sqlflow/backend/bin
```

## Start Backend Services

If your computer has more than 8G of memory, you can change the boot parameters to recommended

Please use the gspLive.sh, eureka.sh and sqlservice.sh under [mac](mac) directory instead of the original one.

* /wings/sqlflow/backend/bin/gspLive.sh

```
#  defult and less than or equal to 8G recommended
heapsize="2g";
# greater than 8G  recommended
# heapsize="3g"; 

```

* /wings/sqlflow/backend/bin/eureka.sh

```
#  defult and less than or equal to 8G recommended
heapsize="256m";
# greater than 8G  recommended
# heapsize="512m"; 
```

* /wings/sqlflow/backend/bin/sqlservice.sh

```
#  defult and less than or equal to 8G recommended
heapsize="4g";
# greater than 8G  recommended
# heapsize="10g"; 
```

start service in background:

```
sh /wings/sqlflow/backend/bin/backend.sh
```

please allow 1-2 minutes to start the service.

use `jps` to check those 3 processing are running.

```
58497 sqlservice.jar
58516 gspLive.jar
58477 eureka.jar
```

**Java service port**

| File           | Port |
| -------------- | ---- |
| eureka.jar     | 8761 |
| gspLive.jar    | 8081 |
| sqlservice.jar | 8083 |

## Nginx Reverse Proxy

If we set the reverse proxy path of gspLive restful service to /api

**1. Config Nginx**

open your nginx configuration file ( at `/usr/local/etc/ngin/nginx.conf` ), add a server :

```
server {
	listen 80 default_server;
	listen [::]:80 default_server;
	
	
	root /wings/sqlflow/frontend/;
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

**2. modify frontend configuration file config.private.json**

- Open the configration file "/wings/sqlflow/frontend/config.private.json"
- Modify the **ApiPrefix** attribute

```
  "ApiPrefix": "/api"
```

### Start Frontend Services

start your nginx :

```
sudo nginx
```

or reload :

```
sudo nginx -s reload
```

open http://yourdomain.com/ to see the SQLFlow.

open http://yourdomain.com/api/gspLive_backend/doc.html?lang=en to see the Restful API documention.

## Sqlflow client api call

See [sqlflow client api call](https://github.com/sqlparser/sqlflow_public/blob/master/api/sqlflow_api_full.md#webapi)

1. Get userId from gudu_sqlflow.conf

- Open the configration file "/wings/sqlflow/backend/conf/gudu_sqlflow.conf"
- The value of anonymous_user_id field is webapi userId

```
  anonymous_user_id=xxx
```

- **Note:** on-promise mode, webapi call doesn't need the token parameter

1. Test webapi by curl

   - test sql:

   ```
     select name from user
   ```

   - curl command:

   ```
   curl -X POST "http://yourdomain.com/api/gspLive_backend/sqlflow/generation/sqlflow" -H "accept:application/json;charset=utf-8" -F "userId=YOUR USER ID HERE" -F  "dbvendor=dbvoracle" -F "sqltext=select name from user"
   ```

   - response:

   ```
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

   - If the code returns **401**, please check the userId is set or the userId is valid.

## How to use  grabit submit to local SQLFlow

1. Get userId from gudu_sqlflow.conf

* Open the configration file "/wings/sqlflow/backend/conf/gudu_sqlflow.conf"

* The value of anonymous_user_id field is webapi userId

    ```
    anonymous_user_id=xxx
    ```

2. Please Input SqlFlow Connect Information tab

   ```
   Server: http://yourdomain.com/api  eg: http://localhost/api
   ServerPort: doesn't need
   UserId: please see No.1 
   User Secret: Just fill in any one 
   ```

   

