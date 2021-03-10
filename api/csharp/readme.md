# Get Started
### [Download](https://api.gudusoft.com/download/api/client/csharp/SQLFlowClient/dist/) the executable program according to your operating system.

- [windows](https://sqlflow.gudusoft.com/download/win/SQLFlowClient.exe)
- [mac](https://sqlflow.gudusoft.com/download/osx/SQLFlowClient)
- [linux](https://sqlflow.gudusoft.com/download/linux/SQLFlowClient)


### Configuration 

#### SQLFlow Cloud server

Create a file named `config.json` in directory where the executable(.exe) exists, and then input your `SecretKey` and `UserId`, always set `host` to `https://api.gudusoft.com` ,for example:

```json
{
  "Host": "https://api.gudusoft.com",
  "SecretKey": "XXX",
  "UserId": "XXX"
}
```
If you want to connect to [the SQLFlow Cloud Server](https://sqlflow.gudusoft.com), you may [request a 30 days premium account](https://www.gudusoft.com/request-a-premium-account/) to 
[get the necessary userId and secret code](/sqlflow-userid-secret.md).

#### SQLFlow on-premise version

Create a file named `config.json` in directory where the executable(.exe) exists, and always set `userId` to `gudu|0123456789`, keep `userSecret` empty, and set `host`to your server ip, for example:

```json
{
  "Host": "http://your server ip:8081",
  "SecretKey": "",
  "UserId": "gudu|0123456789"
}
```
Please [check here](https://github.com/sqlparser/sqlflow_public/blob/master/install_sqlflow.md) to see how to install SQLFlow on-premise version on you own server.

### Set permissions


For mac:
```
chmod +x SQLFlowClient
```

For linux:
```
chmod +x SQLFlowClient
```

### Create a simple sql file for testing
For example, test.sql:
```sql
insert into t2 select * from t1;
```

Run the program from command line:
```
./SQLFlowClient test.sql
```
```
./SQLFlowClient test.sql -g
```

# Usage

SQLFlowClient filepath -parameter value

### parameters

| parameter          | short | value type                                                   | default |                                   |
| ------------------ | ----- | ------------------------------------------------------------ | ------- | --------------------------------- |
| --graph            | -g    | boolean                                                      | false   | Get the graph from sql.           |
| --dbvendor         | -v    | one of the following list :<br />bigquery, couchbase, db2, greenplum, <br />hana , hive, impala , informix, <br />mdx, mysql, netezza, openedge, <br />oracle, postgresql, redshift, snowflake, <br />mssql, sybase, teradata, vertica | oracle  | Set the database of the sqlfile.  |
| --showRelationType | -r    | one or more from the following list :<br /> fdd, fdr, frd, fddi, join | fdd     | Set the relation type.            |
| --simpleOutput     | -s    | boolean                                                      | false   | Set whether to get simple output. |
| --ignoreRecordSet  |       | boolean                                                      | false   | Set whether to ignore record set. |
| --ignoreFunction   |       | boolean                                                      | false   | Set whether to ignore function.   |
| --output           | -o    | string                                                       | ""      | Save output as a file.            |
| --help             |       |                                                              |         | Display this help screen.         |
| --version          |       |                                                              |         | Display version information.      |

### examples
1. SQLFlowClient test.sql
2. SQLFlowClient test.sql -g
3. SQLFlowClient test.sql -g -v oracle
4. SQLFlowClient test.sql -g -v oracle -r fdr
5. SQLFlowClient test.sql -g -v oracle -r fdr,join
6. SQLFlowClient test.sql -g -v oracle -r fdr,join -s
7. SQLFlowClient test.sql -g -v oracle -r fdr,join -s --ignoreRecordSet
8. SQLFlowClient test.sql -g -v oracle -r fdr,join -s --ignoreFunction -o result.txt

# Compile and build on windows

### Download and install the .NET Core SDK

```
https://dotnet.microsoft.com/download
```

### Download source code
```
git clone https://github.com/sqlparser/sqlflow_public.git
```

### Build from command line

```
dotnet publish -c Release /p:PublishProfile=Properties\PublishProfiles\linux.pubxml
dotnet publish -c Release /p:PublishProfile=Properties\PublishProfiles\osx.pubxml
dotnet publish -c Release /p:PublishProfile=Properties\PublishProfiles\win.pubxml
```

### [Download executable programs](https://sqlflow.gudusoft.com/download//)

