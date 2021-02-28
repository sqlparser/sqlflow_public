# Grabit Using Document

## What is a grabit
Grabit is a supporting tool for SQLFlow, which collects SQL scripts from various data sources for SQLFlow, and then uploading them to SQLFlow for data lineage analysis of these SQL scripts. The analysis results can be viewed in the Web front end of SQLFlow. Meanwhile, the analysis results can also be exported from SQLFlow to local area through Grabit, and the JSON results can be uploaded to Neo4j database.

## How to use Grabit

### Prerequisites
- Java 8 or higher version must be installed and configured correctly.

setup the PATH like this: (Please change the JAVA_HOME according to your own environment)
```
export JAVA_HOME=/usr/lib/jvm/default-java

export PATH=$JAVA_HOME/bin:$PATH
```

### Install

````
unzip grabit-x.x.x.zip

cd grabit-x.x.x
````
- **linux & mac open permissions** 
````
chmod 777 *.sh
````
After the installation is complete, you can execute the command `./start.sh /f conf-temp` or `start.bat /f conf-temp`. If the logs directory appears and the **start grabit command** is printed in the log file, the installation is successful.

### Configuration
Modify the configure file to set all parameters correctly according to your own environment.

#### 1. SQLFlow Server
This is the SQLFlow server that the grabit send the SQL script to.

- **server**

Usually, it is the IP address of [the SQLFlow on-premise version](https://www.gudusoft.com/sqlflow-on-premise-version/) 
installed on your owner server such as `127.0.0.1` or `http://127.0.0.1`

You may set the value to `https://api.gudusoft.com` if you like to send your SQL script to [the SQLFlow Cloud Server](https://sqlflow.gudusoft.com) to get the data lineage result.

- **serverPort**

Default value is `8081` if you connect to your SQLFlow on-premise server.

However, if you use setup the nginx reverse proxy in the nginx configuration file like this:
```
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
```
Then, just keep the value of `serverPort` empty and set `server` to the value like this: `http://127.0.0.1/api`.

>Please just keep this value empty if you connect to the SQLFlow Cloud Server by specifing the `https://api.gudusoft.com` 
in the `server`.

- **userId, userSecret**

This is the user id that used to connect to the SQLFlow server.
Always set this value to `gudu|0123456789` and keep `userSecret` empty if you are using the SQLFlow on-premise version.

If you want to connect to [the SQLFlow Cloud Server](https://sqlflow.gudusoft.com), you may [request a 30 days premium account](https://www.gudusoft.com/request-a-premium-account/) to 
[get the necessary userId and secret code](/sqlflow-userid-secret.md).


Example configuration for on-premise version:
```json
	"SQLFlowServer":{
		"server":"127.0.0.1",
		"serverPort":"8081",
		"userId":"gudu|0123456789",
		"userSecret":"" 
	}
```	

Example configuration for Cloud version:
```json
	"SQLFlowServer":{
		"server":"https://api.gudusoft.com",
		"serverPort":"",
		"userId":"your own user id here",
		"userSecret":"your own secret key here" 
	}
```		

#### 2. optionType
You may collect SQL script from various source such as database, github repo, file system.
This parameter tells grabit where the SQL scripts comes from.

Avaiable values for this parameter:
- 1: database 
- 2: github 
- 3: bitbucket 
- 4: single file 
- 5: Multiple SQL Files Under A Directory

This configuration means the SQL script is collected from a database.
```json
"optionType":1
```	

#### 2.1. enableGetMetadataInJSONFromDatabase

If the SQL scripts is not fetched from the database directly, we can also fetch metadata 
from a database instance to help SQLFlow get a more accurate result during the analysis.

When `enableGetMetadataInJSONFromDatabase=1`, You must set all necessary information in `databaseServer` as well.

Of course, you can `enableGetMetadataInJSONFromDatabase=0`. This means all SQL scripts will 
be analyzed offline without any connection to a database. SQLFlow still works quite well to 
get the data lineage result by taking advantage of it's powerful SQL analysis capability.

Sample configuration of enable fetching metadata in json from the database:
```json
"enableGetMetadataInJSONFromDatabase":1
```

#### 3. resultType
When you submit SQL script to the SQLFlow server, A job is created on the SQLFlow server
and you can always see the graphic data lineage result in the frontend of the SQLFlow by using the browser, 


Even better, grabit will fetch the data lineage back to the directory where the grabit is running.
those data lineage result are stored in the `data/datalineage/` directory. 

This parameter specify which kind of format is used to store the data lineage result.

Avaiable values for this parameter:
- 1: json, data lineage result in json.
- 2: csv, data lineage result in CSV format.
- 3: diagram, in graphml format that can be viewed by yEd.

This sample configuration means the output format is json.
```json
"resultType":1
```

#### 4. databaseType
This parameter specify the database dialect of the SQL scripts that been analyzed by the SQLFlow.

```txt
	access,bigquery,couchbase,dax,db2,greenplum,hana,hive,impala,informix,mdx,mssql,
	sqlserver,mysql,netezza,odbc,openedge,oracle,postgresql,postgres,redshift,snowflake,
	sybase,teradata,soql,vertica
```

This sample configuration means the SQL dialect is SQL Server database.
```json
"databaseType":"sqlserver"
```

#### 5. databaseServer
Specify a database instance that grabit will connect to fetch the metadata that helps SQLFlow 
make a more precise analysis and get a more accurate result of data lineage, the data lineage results are stored in the `data/json/` directory in a JSON file named with the current timestamp.

This parameter must be specified if you set `optionType=1` which means the source of SQL script
comes from a database. Otherwise, it can be leave empty.

- **hostname**

The IP of the datbase server that connect to.

- **port**

The port number of the datbase server that connect to.

- **username**

The database user used to login to the database.

- **password**

The password of the database user.

- **sid**

Name of the Oracle instance. Used for Oracle only.

- **extractedSchemas**
This option is used for Oracle only. 

Comma separated list of schemas to extract, or blank to extract all schemas.
`Schema1,Schema2,Schema3`

- **excludedSchemas**
This option is used for Oracle only. 

Comma separated list of schemas to exclude from processing.
If left blank, no schemas will be excluded.
`Schema1,Schema2`

- **extractedDbsSchemas**

List of databases and schemas to extract, separated by
commas, which are to be provided in the format database/schema;
, or blank to extract all databases.
`database1/schema1,database2/schema2,database3`


- **excludedDbsSchemas**

List of databases and schemas to exclude from extraction,
separated by commas
`database1/schema1,database2`

- **enableQueryHistory**

Fetch SQL queries from the query history if set to `true`, default is false.

- **queryHistoryBlockOfTimeInMinutes**

Time interval to extract SQL query from query history if `enableQueryHistory=true`, 
default is `30` minutes.


Sample configuration of a SQL Server database:
```json
"hostname":"127.0.0.1",
"port":"1433",
"username":"sa",
"password":"PASSWORD",
"sid":"",
"extractSchema":"AdventureWorksDW2019/dbo",
"excludedSchema":"",
"extractedDbsSchemas":"",
"excludedDbsSchemas":"",
"enableQueryHistory":false,
"queryHistoryBlockOfTimeInMinutes":30
```

#### 6. githubRepo & bitbucketRepo
When `optionType`=2, grabit will fetch SQL files from a specified github repo, When `optionType`=3, grabit will fetch SQL files from a specified bitbucket repository, the SQL script files are stored in `data/github/` or `data/bitbucket/` directory.

Both sshkey and account password authentication methods are supported.

- **url**

Pull the repository address of the SQL script from GitHub or BitBucket.

- **username**

Pull the user name to which the SQL script is connected from GitHub or BitBucket.

- **password**

Pull the password to which the SQL script is connected from GitHub or BitBucket.

- **sshKeyPath**

Extract the path to the SSH private key file for the SQL script connection from GitHub or BitBucket, sshkey and account password two authentication methods can be filled in either.

Sample configuration of the GitHub or BitBucket public repository servers :
```json
"url":"your public repository address here",
"username":"",
"password":"",
"sshKeyPath":""
```

Sample configuration of the GitHub or BitBucket private repository servers:
```json
"url":"your private library address here",
"username":"your private repository  username here",
"password":"your private repository  password here",
"sshKeyPath":""
```
or
```json
"url":"your private repository address here",
"username":"",
"password":"",
"sshKeyPath":"your private repository ssh key address here"
```

#### 7. SQLInSingleFile

When `optionType=4`, this is a single SQL file need to be analyzed.

- **filePath**

The name of the SQL file with full path.

#### 8. SQLInDirectory

When `optionType=5`, SQL files under this directory including sub-directory will be analyzed. 

- **directoryPath**

The directory which includes the SQL files.

#### 9. isUploadNeo4j

Whether to upload the JSON analysis results obtained from SQLFlow to the Neo4j database, avaiable values for this parameter is 1 or 0, enable this function if the value is 1, disable it if the value is 0, the default is 0.

Sample configuration of a Whether to upload neo4j:
```json
"isUploadNeo4j":1
```

#### 10. neo4jConnection

If `IsuploadNeo4j` is set to '1', this means that uploading JSON analysis results obtained in SQLFlow to Neo4j database is enabled,
then, this parameter then specifies the details of the neo4j server.

- **url**

The IP of the neo4j server that connect to.

- **username**

The user name of the neo4j server that connect to.

- **password**

The password of the neo4j server that connect to.

Sample configuration of a local directory path:
```json
"url":"127.0.0.1:7687",
"username":"your server username here",
"password":"your server password here"
```



**eg configuration file:**
````json
{
    "databaseServer":{
        "hostname":"127.0.0.1",
        "port":"1433",
        "username":"sa",
        "password":"PASSWORD",
        "sid":"",
        "extractSchema":"AdventureWorksDW2019/dbo",
        "excludedSchema":"",	
        "extractedDbsSchemas":"",
        "excludedDbsSchemas":"",
        "enableQueryHistory":false,
        "queryHistoryBlockOfTimeInMinutes":30
    },
    "githubRepo":{
        "url":"https://github.com/sqlparser/snowflake-data-lineage",
        "username":"",
        "password":"",
        "sshkeyPath":""
    },
    "bitbucketRepo":{
        "url":"",
        "username":"",
        "password":"",
        "sshkeyPath":""
    },
    "SQLInSingleFile":{
        "filePath":""
    },
    "SQLInDirectory":{
        "filePath":""
    },
    "SQLFlowServer":{
        "server":"http:127.0.0.1",
        "serverPort":"8081",
        "userId":"gudu|0123456789",
        "userSecret":""
    },
    "neo4jConnection":{
        "url":"",
        "username":"",
        "password":""
    },
    "optionType":2,
    "resultType":1,
    "databaseType":"snowflake",
    "isUploadNeo4j":0,
    "enableGetMetadataInJSONFromDatabase":1
}
````

### Launch 
#### grabit ui launch
Graphic interface mode to start Grabit.

- **mac & linux**
`
./start.sh
`
- **windows**
`
start.bat
`
#### grabit cmd launch
Grabit is started command-line.

- **mac & linux**
````
./start.sh /f <path_to_config_file>  

note: 
    path_to_config_file: config file path  

eg: 
    ./start.sh /f config.txt
````
- **windows**
````
./start.bat /f <path_to_config_file>  

note: 
    path_to_config_file: config file path  

eg: 
    start.bat /f config.txt
````

After execution, view the `logs/log.log` file. If the log prints a **submit job to sqlflow successful**. Then it is proved that the upload to SQLFlow has been successful. Log in the SQLFlow website to view the newly analyzed results. In the `Task List`, you can view the analysis results of the currently submitted tasks.If the download analysis result is set, **export json result successful** will appear in the log.

#### grabit job 
Timed tasks start grabit.

- **use mac & linux crontab**
````
cron ./start_job.sh /f <path_to_config_file> <lib_path>

note: 
    path_to_config_file: config file path 
    lib_path: lib directory absolute path

eg: 
    1. sudo vi /etc/crontab 
    2. add the following statement to the last line
        0 */1   * * * ubuntu /home/ubuntu/grabit-2.4.6/start_job.sh /f /home/ubuntu/grabit-2.4.6/conf-oracle /home/ubuntu/grabit-2.4.6/lib
        
        note: 
            0 */1   * * *: cron expression
            ubuntu: The name of the system user performing the task
            /home/ubuntu/grabit-2.4.6/start_job.sh: The path of the task script
            /f /home/ubuntu/grabit-2.4.6/conf-oracle: config file path
            /home/ubuntu/grabit-2.4.6/lib: lib directory absolute path
    3.sudo service cron restart    
````
