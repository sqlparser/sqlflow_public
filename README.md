## [SQLFlow](https://sqlflow.gudusoft.com) - A tool that tracks column-level data lineage

Track Column-Level Data Lineage for [more than 20 major databases](/databases/readme.md) including 
Snowflake, Hive, SparkSQL, Teradata, Oracle, SQL Server, AWS redshift, BigQuery, etc.

Build and visualize lineage from SQL script from query history, ETL script,
Github/Bitbucket, Local filesystem and remote databases.

[Exploring lineage using an interactive diagram](https://sqlflow.gudusoft.com) or programmatically using [Restful APIs](/api) or [SDKs](https://www.gudusoft.com/sqlflow-java-library-2/).

Discover data lineage in this query:
```sql
insert into emp (id,first_name,last_name,city,postal_code,ph)
  select a.id,a.first_name,a.last_name,a.city,a.postal_code,b.ph
  from emp_addr a
  inner join emp_ph b on a.id = b.id;
```

SQLFlow presents a nice clean graph to you that tells
where the data came from, what transformations it underwent along the way, 
and what other data items are derived from this data value.

[![SQLFlow Introduce](images/sqlflow_introduce1.png)](https://sqlflow.gudusoft.com)

### What SQLFlow can do for you
- Scan your database and discover the data lineage instantly.
- Automatically collect SQL script from github/bitbucket or local file system.
- Provide a nice cleam diagram to the end-user to understand the data lineage quickly.
- programmatically using [Restful APIs](/api) or [SDKs](https://www.gudusoft.com/sqlflow-java-library-2/) to get lineage in CSV, JSON, Graphml format.
- Incorporate the lineage metadata decoded from the complex SQL script into your own metadata database for further processing.
- Visualize the metadata already existing in your database to release the power of data.
- Perform impact analysis and root-cause analysis by tracing lineage backwards or forwards with several mouse click.
- Able to process SQL script from more than 20 major database vendors.

### How to use SQLFlow
- Open [the official website](https://gudusoft.com/sqlflow/#/) of the SQLFlow and paste your SQL script or metadata to get a nice clean lineage diagram.
- Call the [Restful API](/api) of the SQLFlow in your own code to get data lineage metadata decoded by the SQLFlow from the SQL script.
- The [on-premise version](https://github.com/sqlparser/sqlflow_public/blob/master/install_sqlflow.md) of SQLflow enables you to use it on your own server to keep the data safer.


### Restful APIs
- [SQLFlow API document](https://github.com/sqlparser/sqlflow_public/blob/master/api/sqlflow_api.md)
- [Client in C#](https://github.com/sqlparser/sqlflow_public/tree/master/api/client/csharp)

### SQLFlow architecture
- [Architecture document](sqlflow_architecture.md)

### User manual and FAQ
- [User guide](sqlflow_guide.md)
- [SQLFlow FAQ](sqlflow_faq.md)


