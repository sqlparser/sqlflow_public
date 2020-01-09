## Instructions on how to install SQLFlow on your own server.

SQLFow was comprised of two parts: frontend and backend. 
The frontend and backend can be installed on the same server, or they can be installed on two different servers seperately.

### Prerequisites
- A linux server with at least 4GB memory.
- Java 8
- Nginx web server.

### setup Environment (Ubuntu for example)
	sudo apt-get update
	sudo apt-get install nginx
		(web root: /var/www/nginx-default)
	sudo apt-get install default-jre	

CentOS
	- [How To Install Nginx on CentOS](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-centos-7)
	- [How To Install Java on CentOS ](https://www.digitalocean.com/community/tutorials/how-to-install-java-on-centos-and-fedora)
	
### Frontend
The SQLFlow frontend is written in Typescript and the distribution files include some obfuscated javascript files along with some css and html files.

#### Files
- sqlflow/*.js
- sqlflow/index.html
- sqlflow/index.css
- sqlflow/config.private.json
- sqlflow/font
- sqlflow/images


Just copy those files into the directory under web root(such as `/var/www/html`) and modify the config file to set environment accordingly.

#### Modify the config file

- "ApiPrefix": "http://127.0.0.1:8081"

	Default is empty and no need to change it if the frontend is installed on the same server as the backend.
	Otherwise, set your own IP and port like above.  The default port is 8081.

- "base64token": ""  

	This token value must be the same as the token in backend(`user/username.json`) 

### Backend
The SQLFlow backend is written in Java. The distribution files include some jar files and scripts that help you start SQLFlow.


#### Files
  - backend.sh, script used to start the SQLFlow.
  - eureka.jar, default port: 8761
  - eureka.sh
  - gspLive.jar, default port: 8081
  - gspLive.sh
  - gudu_sqlflow_license.key
  - gudu_sqlflow_license.txt
  - monitor.sh
  - sqlservice.jar, default port: 8083
  - sqlservice.sh
  - user/username.json, including the authorization token which is used in the RESTFul APIs
  

Create a directory for backend files and then,

`sudo mkdir -p wings/sqlflow/backend`

copy all backend files into this directory:
  
```
chmod  744  monitor.sh
chmod  744  backend.sh
chmod  744  eureka.sh
chmod  744  sqlservice.sh
chmod  744  gspLive.sh
```

#### Modify the shell script
The default installation path for the SQLFlow backend is: `/wings/sqlflow/backend`.
Please modify the path accordingly in the shell script if you change this path of directory.

Add `-Xms -Xmx` option in `sqlserver.sh` and `gspLive.sh` if 8G memory is available on the server.

gspLive.sh

	nohup java -server -Xms2048m -Xmx2048m -jar gspLive.jar >> gspLive.out 2>&1 & 
	
sqlserver.sh
	
	nohup java -server -Xmn512m -Xms4096m -Xmx4096m -Djavax.accessibility.assistive_technologies=" " -jar sqlservice.jar  >> sqlservice.out 2>&1 & 

#### Change the service port
You may change the service port by adding the following parameter in shell script when starting the service.
```
--server.port=<port>
```

#### Starting the backend service

`./backend.sh`

Please allow 1-2 minutes to start the service.

Use `ps -ef|grep java` to check those 3 processing are running.

```
ubuntu   11047     1  0 Nov02 ?        00:04:44 java -server -jar eureka.jar
ubuntu   11076     1  0 Nov02 ?        00:04:11 java -server -Xmn512m -Xms2g -Xmx2g -Djavax.accessibility.assistive_technologies=  -jar sqlservice.jar
ubuntu   11114     1  0 Nov02 ?        00:05:17 java -server -jar gspLive.jar
```

### Use the SQLFlow
Just open a browser and enter `http://ip-of-your-server/sqlflow`

