# Get Started
### [Download](https://api.gudusoft.com/download/api/client/csharp/SQLFlowClient/dist/) the executable program depends on your operating system.

- [windows](https://api.gudusoft.com/download/api/client/csharp/SQLFlowClient/dist/win/SQLFlowClient.exe)
- [mac](https://api.gudusoft.com/download/api/client/csharp/SQLFlowClient/dist/osx/SQLFlowClient)
- [linux](https://api.gudusoft.com/download/api/client/csharp/SQLFlowClient/dist/linux/SQLFlowClient)

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

### Use your  own configuration 

If you want to use your own server and token, create the a file named `config.json` in directory where executable exists, and then input your `host` and `token`, for example:

```json
{
	"Host": "https://api.gudusoft.com",
	"Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWVzdFVzZXIiLCJleHAiOjE1ODEyMDY0MDAsImlhdCI6MTU3MzQzMDQwMH0.-lvxaPlXmHbtgSFgW7ycu8KUczRiFZy5A1aNRGY-tKM"
}
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
| --output           | -o    | string                                                       | ""      | Save output as a file.            |
| --help             |       |                                                              |         | Display this help screen.         |
| --version          |       |                                                              |         | Display version information.      |

### examples
1. SQLFlowClient test.sql
2. SQLFlowClient test.sql -g
3. SQLFlowClient test.sql -g -v db2
4. SQLFlowClient test.sql -g -v db2 -r fdr
5. SQLFlowClient test.sql -g -v db2 -r fdr,join
6. SQLFlowClient test.sql -g -v db2 -r fdr,join -s
7. SQLFlowClient test.sql -g -v db2 -r fdr,join -s -o result.txt

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

### [Download executable programs](https://api.gudusoft.com/download/api/client/csharp/SQLFlowClient/dist/)

