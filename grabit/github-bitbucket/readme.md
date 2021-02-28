## Automated data lineage from github/bitbucket

Grabit able to fetch SQL scripts from the github/bitbucket repo,
and automated data lineage from those SQL scripts by sending it
to the SQLFlow server.


### Step 1: Install git
- **ubuntu:** 
```
sudo apt-get install git
```
- **centos:** 
```
sudo yum install git
```
- **mac:** 
```
brew install git
```
- **windows:** 
```
1.Go to the Git official website to download, website address: https://git-scm.com/downloads
2.Run the Git installation file and click Next to finish the installation
```
After the installation is completed, run **git --version** to check it is installed successfully.

- **Generate the ssh public and private key**：
```
ssh-keygen -o
```
### Step 2: Install grabit
```
unzip grabit-x.x.x.zip

cd grabit-x.x.x
```

- **linux & mac open permissions** 
```
chmod 777 *.sh
```

After the installation is completed, you can execute the command  `./start.sh /f conf-temp` or `start.bat /f conf-temp`. 
If the logs directory appears and the **start grabit command** is printed in the log file, the installation is successful.

### Step 3: Set up grabit configuration file

#### 1. set up optionType to grab SQL from github/bitbucket

You may collect SQL script from various source such as database, github repo, file system. 
This parameter tells grabit where the SQL scripts comes from.

Avaiable values for this parameter:

- github：2

- bitbucket：3

#### 2. set up databaseType

the database type of all connections, the types currently supported：
```text
access,bigquery,couchbase,dax,db2,greenplum,hana,hive,impala,informix,mdx,mssql,sqlserver,mysql,netezza,
odbc,openedge,oracle,postgresql,postgres,redshift,snowflake,sybase,teradata,soql,vertica
```

#### 3. Other options
For all other options, please check [the grabit documentation](https://github.com/sqlparser/sqlflow_public/blob/master/grabit/readme.md)
