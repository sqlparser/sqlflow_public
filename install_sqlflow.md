## Instructions on how to install SQLFlow on your own server.

SQLFow was comprised of two parts: frontend and backend. 
The frontend and backend can be installed on the same server, or they can be installed seperated on two different servers.

### Prerequisites
- A linux server with 4GB memory.
- Java 8
- Nginx web server.

### frontend
The SQLFlow frontend is written in Typescript and the distribution files include some obfuscated javascript files along with some css and html files.

#### Files
sqlflow/*.js
sqlflow/index.html
sqlflow/index.css
sqlflow/config.private.json
sqlflow/font
sqlflow/images

Just copy those files into the directory under web root(such as `/var/www/html`) and modify the config file to set environment accordingly.

#### Modify the config file

- "ApiPrefix": "http://106.54.134.160:8081"

	set your own IP address and keep port 8081 if it's unchanged during the installation of backend.

- "base64token": ""  

	This token value must be the same as the token in backend(user/username.json) 

### backend
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
  

Create a directory for backend files:

`sudo mkdir -p wings/sqlflow/backend`

copy all backend files into this directory:
  
```
chmod  744  monitor.sh
chmod  744  backend.sh
chmod  744  eureka.sh
chmod  744  sqlservice.sh
chmod  744  gspLive.sh
```

### Modify the shell script
The default install path for the SQLFlow backend is: /wings/sqlflow/backend
Please modify the path accordingly in the shell script if you change this default install directory.

### Change the service port
You may change the service port by adding the following parameter in shell script when starting the service.
```
--server.port=<port>
```

#### start the service

`./backend.sh`

Please allow 1-2 minutes to start the service.

