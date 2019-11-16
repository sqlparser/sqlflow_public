# Get Start
### Dowload source code and program
```
git clone https://github.com/sqlparser/sqlflow_public.git
```
### Choose the executable program depends on your operating system.

For windows:
```
cd sqlflow_public/api/client/csharp/SQLFlowClient/dist/win
```

For mac:
```
cd sqlflow_public/api/client/csharp/SQLFlowClient/dist/osx
```
```
chmod +x SQLFlowClient
```

For linux:
```
cd sqlflow_public/api/client/csharp/SQLFlowClient/dist/linux
```
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

SQLFlowClient filepath -parameters

### parameters

| parameter          | short | value type                                                   | default |                                   |
| ------------------ | ----- | ------------------------------------------------------------ | ------- | --------------------------------- |
| --graph            | -g    | boolean                                                      | false   | Get the graph from sql.           |
| --dbvendor         | -v    | one of the following list :<br /> bigquery, couchbase, db2, greenplum, hana ,<br /> hive, impala , informix, mdx, mysql, netezza,<br /> openedge, oracle, postgresql, redshift, snowflake,<br /> mssql, sybase, teradata, vertica | oracle  | Set the database of the sqlfile.  |
| --showRelationType | -r    | one or more from the following list :<br /> fdd, fdr, frd, fddi, join | fdd     | Set the relation type.            |
| --simpleOutput     | -s    | boolean                                                      | false   | Set whether to get simple output. |
| --help             |       |                                                              |         | Display this help screen.         |
| --version          |       |                                                              |         | Display version information.      |

### examples
1. SQLFlowClient test.sql
2. SQLFlowClient test.sql -g
3. SQLFlowClient test.sql -g -v db2
4. SQLFlowClient test.sql -g -v db2 -r fdr
5. SQLFlowClient test.sql -g -v db2 -r fdr,join
6. SQLFlowClient test.sql -g -v db2 -r fdr,join -s