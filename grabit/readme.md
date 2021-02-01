# Grabit Using Document

## grabit ui launch
#### mac & linux
`
./start.sh
`
#### windows
`
./start.bat
`
## grabit cmd launch
### step 1. set config file

Configuration file template details explain:
````
{
    // bitbucket option config info
    "bitbucketRepoHistoryInfo":{
	"url" : "",
	"username" : "",
	"password" : "",
	"sshkeyPath" : "ssh key file path"
    },
	
    // dataBase type
    "dataBase":"dataBase type.  eg: mysql/sqlserver/orcale...",
	
    // database option config info
    "dataBaseHistoryInfo":{
	"excludedSchema":"",
	"extractSchema":"",
	"hostname":"",
	"password":"",
	"port":"",
	"sid":"",
	"username":""
    },

    // single file option file path
    "fileHistoryInfo":{
	"filePath" : ""
    },

    // directory option file path
    "dirHistoryInfoT":{
	"filePath" : ""
    },

    // github option config info
    "githubRepoHistoryInfo":{
	"url" : "",
	"username" : "",
	"password" : "", 
	"sshkeyPath" : " ssh key file path"
    },
    
    // sqlflow connetion config info
   "sqlFlowHistoryInfo":{
	"ip":"https://api.gudusoft.com",
	"port":"",
	"secret":"",
	"userid":""
    },

    // neo4j connetion config info
    "neo4jConnection":{
        "url":"localhost:7687",
        "userName":"neo4j",
        "password":""
    },

    optionType: 1,
    resultType: 1,
    isUploadNeo4j: 1,
    // Whether to enable a history query
    isQueryHistory: false,
    // history query minutes time
    min: 30
}


optionType: data source type.  
    1: database 
    2: github 
    3: bitbucket 
    4: single file 
    5: Multiple SQL Files Under A Directory

resultType: output result type
    1: json
    2: csv
    3: diagram

isUploadNeo4j:
    1: yes
    0: no (default)

isQueryHistory: Whether open  history SQL query
    true
    false (default)

min: history query minutes time
````

### step 2. Usage
#### mac & linux
````
./start.sh /f <path_to_config_file>  

note: 
    path_to_config_file: config file path  

eg: 
    ./start.sh /f config.txt
````
#### winodws
````
./start.bat /f <path_to_config_file>  

note: 
    path_to_config_file: config file path  

eg: 
    start.bat /f config.txt
````
## grabit job 
### use mac & linux crontab
````
cron ./start.sh /f <path_to_config_file>  

note: 
    path_to_config_file: config file path  

eg: 
    10 0 * * * ./start.sh /f config.txt
````
