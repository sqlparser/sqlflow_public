# Grabit Using Document

## What is a grabit
Grabit is a supporting tool for SQLFlow, which collects SQL scripts from various data sources for SQLFlow, 
and then uploading them to SQLFlow for data lineage analysis of these SQL scripts. 
The analysis results can be viewed in the browser. Meanwhile, the data lineage results will be fetched to 
the directory where Grabit is installed, and the JSON results can be uploaded to the Neo4j database if necessary.

## How to use Grabit

### Prerequisites
- Java 8 or higher version must be installed and configured correctly.

setup the PATH like this: (Please change the JAVA_HOME according to your environment)
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
After the installation is complete, you can execute the command `./start.sh /f conf-template/generic-config-template` or `start.bat /f conf-template/generic-config-template`. 
You may check logs under the logs directory for more information.

### Running the grabit tool

The grabit tool can be running in both GUI mode and the command line mode.

#### GUI mode (only support Oracle JDK)

- **mac & linux**
```
./start.sh
```

- **windows**
```
start.bat
```

#### Command line mode
Grabit is started command-line.

- **mac & linux**
```
./start.sh /f <path_to_config_file>  

note: 
    path_to_config_file: the full path to the config file

eg: 
    ./start.sh /f config.txt
```

- **windows**
```
./start.bat /f <path_to_config_file>  

note: 
    path_to_config_file: the full path to the config file

eg: 
    start.bat /f config.txt
```

After execution, view the `logs/graibt.log` file for the detailed information. 

If the log prints a **submit the job to sqlflow successful**. 
Then it is proved that the upload to SQLFlow has been successful. 

Log in to the SQLFlow website to view the newly analyzed results. 
In the `Job List`, you can view the analysis results of the currently submitted tasks.


#### Run the grabit at a scheduled time
 
This guide shows you how to set up a cron job in Linux, with examples.

- **use mac & linux crontab**
```
cron ./start_job.sh /f <path_to_config_file> <lib_path>

note: 
    path_to_config_file: config file path 
    lib_path: lib directory absolute path

e.g.: 
    1. sudo vi /etc/crontab 
    2. add the following statement to the last line
        0 */1   * * * ubuntu /home/ubuntu/grabit-2.4.6/start_job.sh /f /home/ubuntu/grabit-2.4.6/conf-template/oracle-config-template /home/ubuntu/grabit-2.4.6/lib
        
        note: 
            0 */1   * * *: cron expression
            ubuntu: The name of the system user performing the task
            /home/ubuntu/grabit-2.4.6/start_job.sh: The path of the task script
            /f /home/ubuntu/grabit-2.4.6/conf-template/oracle-config-template: config file path
            /home/ubuntu/grabit-2.4.6/lib: lib directory absolute path
    3.sudo service cron restart    
```

Please check [this document](https://phoenixnap.com/kb/set-up-cron-job-linux) for more information about cron.

### Configuration
Modify the configure file to set all parameters correctly according to your environment.

#### 1. SQLFlow Server
This is the SQLFlow server that the grabit sends the SQL script.

- **server**

Usually, it is the IP address of [the SQLFlow on-premise version](https://www.gudusoft.com/sqlflow-on-premise-version/) 
installed on your owner servers such as `127.0.0.1` or `http://127.0.0.1`

You may set the value to `https://api.gudusoft.com` if you like to send your SQL script to [the SQLFlow Cloud Server](https://sqlflow.gudusoft.com) to get the data lineage result.

- **serverPort**

The default value is `8081` if you connect to your SQLFlow on-premise server.

However, if you setup the nginx reverse proxy in the nginx configuration file like this:
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
Then, keep the value of `serverPort` empty and set `server` to the value like this: `http://127.0.0.1/api`.

>Please keep this value empty if you connect to the SQLFlow Cloud Server by specifying the `https://api.gudusoft.com` 
in the `server`

- **userId, userSecret**

This is the user id that is used to connect to the SQLFlow server.
Always set this value to `gudu|0123456789` and keep `userSecret` empty if you use the SQLFlow on-premise version.

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
You may collect SQL scripts from various sources such as database, Github repo, file system.
This parameter tells grabit where the SQL scripts come from.

Available values for this parameter:
- 1: database 
- 2: github 
- 3: bitbucket 
- 4: single file 
- 5: Multiple SQL Files Under A Directory

This configuration means the SQL script is collected from a database.
```JSON
"optionType":1
```	

#### 2.1. enableGetMetadataInJSONFromDatabase

If the source of the SQL scripts is not the database, we may specify a database by
setting `databaseServer` parameter to fetch metadata from the database instance 
to help SQLFlow get a more accurate result during the analysis.

If `enableGetMetadataInJSONFromDatabase=1`, You must set all necessary information in `databaseServer`.

Of course, you can `enableGetMetadataInJSONFromDatabase=0`. This means all SQL scripts will be analyzed offline without a connection to the database. SQLFlow still works quite well to 
get the data lineage result by taking advantage of its powerful SQL analysis capability.

Sample configuration of enable fetching metadata in json from the database:
```json
"enableGetMetadataInJSONFromDatabase":1
```

#### 3. resultType
When you submit SQL script to the SQLFlow server, A job is created on the SQLFlow server
and you can always see the graphic data lineage result in the frontend of the SQLFlow by using the browser, 


Even better, grabit will fetch the data lineage back to the directory where the grabit is running.
Those data lineage results are stored in the `data/datalineage/` directory. 

This parameter specifies which kind of format is used to save the data lineage result.

Available values for this parameter:
- 1: JSON, data lineage result in JSON.
- 2: CSV, data lineage result in CSV format.
- 3: diagram, in graphml format that can be viewed by yEd.

This sample configuration means the output format is json.
```json
"resultType":1
```

#### 4. databaseType
This parameter specifies the database dialect of the SQL scripts that the SQLFlow has analyzed.

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

This parameter must be specified if you set `optionType=1`, which means the SQL script source
comes from a database. Otherwise, it can be left empty.

- **hostname**

The IP of the database server that the grabit connects.

- **port**

The port number of the database server that the grabit connect.

- **username**

The database user used to login to the database.

- **password**

The password of the database user.

- **sid**

Name of the Oracle instance. 

For other databases, it represents the database name and is optional.
If it's specified, only metadata under this database will be extracted.


- **extractedSchemas**
This option is used for Oracle and Teradata only. 

Comma separated list of schemas to extract, or blank to extract all schemas.
`Schema1,Schema2,Schema3`

- **excludedSchemas**
This option is used for Oracle and Teradata only. 

This parameters works under the resultset filtered by `extractedSchemas`. Comma separated list of schemas to exclude from processing.
If left blank, no schemas will be excluded.
`Schema1,Schema2`

- **extractedDbsSchemas**

List of databases and schemas to extract, separated by
commas, which are to be provided in the format database/schema;
Or blank to extract all databases.
`database1/schema1,database2/schema2,database3`


- **excludedDbsSchemas**

This parameters works under the resultset filtered by `extractedDbsSchemas`.
List of databases and schemas to exclude from extraction, separated by commas
`database1/schema1,database2`


- **extractedStoredProcedures**

A list of stored procedures under the specified database and schema to extract, separated by
commas, which are to be provided in the format database.schema.procedureName or schema.procedureName;
Or blank to extract all databases, support expression, for example 'scott.vEmp*'.
`database1.schema1.procedureName1,database2.schema2.procedureName2,schema3.procedureName3`

- **extractedViews**

A list of stored views under the specified database and schema to extract, separated by
commas, which are to be provided in the format database.schema.viewName or schema.viewName.
Or blank to extract all databases, support expression, for example 'scott.test*'.
`database1.schema1.viewName1,database2.schema2.viewName2,schema3.viewName3`

- **enableQueryHistory**

Fetch SQL queries from the query history if set to `true` default is false.

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
"extractSchema":"",
"excludedSchema":"",
"extractedDbsSchemas":"AdventureWorksDW2019/dbo",
"excludedDbsSchemas":"",
"extractedStoredProcedures":"AdventureWorksDW2019.dbo.f_qry*",
"extractedViews":"",
"enableQueryHistory":false,
"queryHistoryBlockOfTimeInMinutes":30
```

#### 6. githubRepo & bitbucketRepo
When `optionType`=2, grabit will fetch SQL files from a specified github repo, 
When `optionType`=3, grabit will fetch SQL files from a specified bitbucket repository, 
the SQL script files are stored in `data/github/` or `data/bitbucket/` directory temporary
before submitting to the SQLFlow server.

Both sshkey and account password authentication methods are supported.

- **url**

Pull the repository address of the SQL script from GitHub or BitBucket.

- **username**

Pull the user name to which the SQL script is connected from GitHub or BitBucket.

- **password**

Pull the password to which the SQL script is connected from GitHub or BitBucket.

- **sshKeyPath**

The full path to the SSH private key file.


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

When `optionType=4`, this is a single SQL file needs to be analyzed.

- **filePath**

The name of the SQL file with full path.

#### 8. SQLInDirectory

When `optionType=5`, SQL files under this directory including sub-directory will be analyzed. 

- **directoryPath**

The directory includes the SQL files.

#### 9. isUploadNeo4j

Upload the data lineage result to a Neo4j database for further processing. 
Available values for this parameter is 1 or 0, enable this function if the value is 1, disable it if the value is 0, 
the default value is 0.

Sample configuration of a Whether to upload neo4j:
```json
"isUploadNeo4j":1
```

#### 10. neo4jConnection

If `IsuploadNeo4j` is set to '1', this parameter specifies the details of the neo4j server.

- **url**

The IP of the neo4j server that connects to.

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
        "extractedStoredProcedures":"",
        "extractedViews":"",
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
    "enableGetMetadataInJSONFromDatabase":0
}
````
