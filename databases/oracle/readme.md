## Automated data lineage from SQL Server (GUI Mode)
This article introduces how to discover the data lineage from SQL Server scripts or the SQL Server database and automatically update it. 
So the business users and developers can see the SQL Server data lineage graph instantly.

### Software used in this solution
- [SQLFlow Cloud](https://sqlflow.gudusoft.com) Or [SQLFlow on-premise version](https://www.gudusoft.com/sqlflow-on-premise-version/)
- [Grabit tool](https://www.gudusoft.com/grabit/) for SQLFlow. It's free.


### Install grabit tool
After [download grabit tool](https://www.gudusoft.com/grabit/), please [check this article](https://github.com/sqlparser/sqlflow_public/tree/master/grabit) 
to see how to setup the grabit tool.

### Discover data lineage in a SQL Server database
- After [start up the grabit tool](https://github.com/sqlparser/sqlflow_public/tree/master/grabit#running-the-grabit-tool), this is the first UI.
Click the `database` button.

![Grabit SQL Server UI 1](grabit-oracle-1.png)

-  Select `sql server` in the list

![Grabit SQL Server UI 2 database](grabit-sql-server-2-database.png)

- Set the database parameters. In this example, we only discover the data lineage in AdventureWorksDW2019/dbo schema.

![Grabit SQL Server UI 3 database parameters](grabit-sql-server-3-database-parameters.png)

- After grabbing the metadata from the SQL Server database, connect to the SQLFlow server. 
It would help if you had [a premium account](https://github.com/sqlparser/sqlflow_public/blob/master/sqlflow-userid-secret.md) to access the SQLFlow Cloud.

![Grabit SQL Server SQLFlow](grabit-sql-server-4-sqlflow.png)

- Submit the database metadata to the SQLFlow server and get the data lineage 
![Grabit SQL Server SQLFlow result](grabit-sql-server-5-sqlflow-result.png)

- Check out the diagram via this url: [https://sqlflow.gudusoft.com/#/job/latest](https://sqlflow.gudusoft.com/#/job/latest)

![Grabit SQL Server data lineage result](grabit-sql-server-6-data-lineage-result.png)

- You may save the data lineage in JSON/CSV/GRAPHML format

The file will be saved under `data\datalineage` directory.

### Further information
This tutorial illustrates how to discover the data lineage of a SQL Server database in the grabit UI mode,
If you like to automated the data lineage discovery, you may use the Grabit command line mode.

- [Discover SQL Server data lineage in command line mode](grabit-sql-server-command-line.md)


This tutorial illustrates how to discover the data lineage of a SQL Server database by submitting the database
metadata to the SQLFlow Cloud version, You may set up the [SQLFlow on-premise version](https://www.gudusoft.com/sqlflow-on-premise-version/)
on your server to secure your information.

For more options of the grabit tool, please check this page.
- [Grabit tool readme](https://github.com/sqlparser/sqlflow_public/tree/master/grabit)

The completed guide of SQLFlow UI
- [How to use SQLFlow](https://github.com/sqlparser/sqlflow_public/blob/master/sqlflow_guide.md)



### Know-How
![sqlflow-automated-data-lineage](/images/sqlflow-overview-grabit.png "SQLFlow automated data lineage")
