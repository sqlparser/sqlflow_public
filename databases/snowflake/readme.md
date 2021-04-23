## Automated data lineage from Snowflake (GUI Mode)
This article introduces how to discover the data lineage from snowflake scripts or the snowflake database and automatically update it. 
So the business users and developers can see the SQL Server data lineage graph instantly.

### Software used in this solution
- [SQLFlow Cloud](https://sqlflow.gudusoft.com) Or [SQLFlow on-premise version](https://www.gudusoft.com/sqlflow-on-premise-version/)
- [Grabit tool](https://www.gudusoft.com/grabit/) for SQLFlow. It's free.


### Install grabit tool
After [download grabit tool](https://www.gudusoft.com/grabit/), please [check this article](https://github.com/sqlparser/sqlflow_public/tree/master/grabit) 
to see how to setup the grabit tool.

### Discover data lineage in a snowflake database
- After [start up the grabit tool](https://github.com/sqlparser/sqlflow_public/tree/master/grabit#running-the-grabit-tool), this is the first UI.
Click the `database` button.

![Grabit snowflake UI 1](grabit-snowflake-1.png)

-  Select `snowflake` in the list

![Grabit snowflake UI 2 database](grabit-snowflake-2-database.png)

- Set the database parameters. In this example, we only discover the data lineage in DEMO_DB/PUBLIC schema.

![Grabit snowfalke UI 3 database parameters](grabit-snowflake-3-database-parameters.png)

- If we only want to get all the schema data in the specified database, we can do this by using the following configuration:
  
    If you only want to retrieve all the data under the currently connected database, the `extractedDbsSchemas` parameter needs to specify all the schemas under the current database.In this example
    ````json
    "database":"db1"
    "extractedDbsSchemas":"shcema1,shcema2,shcema3...",
    "excludedDbsSchemas":""
    ````

    If you just want to get all the data under other databases, the `extractedDbsSchemas` parameter needs to specify the database as well as all the schemas.In this example
    ````json
    "database":"db1"
    "extractedDbsSchemas":"db2/shcema1,db2/shcema2...",
    "excludedDbsSchemas":""
    ````

- After grabbing the metadata from the snowflake database, connect to the SQLFlow server. 
It would help if you had [a premium account](https://github.com/sqlparser/sqlflow_public/blob/master/sqlflow-userid-secret.md) to access the SQLFlow Cloud.

![Grabit snowflake SQLFlow](grabit-snowflake-4-sqlflow.png)

- Submit the database metadata to the SQLFlow server and get the data lineage 
![Grabit snowflake SQLFlow result](grabit-snowfalke-5-sqlflow-result.png)

- Check out the diagram via this url: [https://sqlflow.gudusoft.com/#/job/latest](https://sqlflow.gudusoft.com/#/job/latest)

![Grabit snowflake data lineage result](grabit-snowflake-6-data-lineage-result.png)

- You may save the data lineage in JSON/CSV/GRAPHML format

The file will be saved under `data\datalineage` directory.

### Further information
This tutorial illustrates how to discover the data lineage of a Snowflake database in the grabit UI mode,
If you like to automated the data lineage discovery, you may use the Grabit command line mode.

- [Discover snowflake data lineage in command line mode](grabit-snowflake-command-line.md)


This tutorial illustrates how to discover the data lineage of a snowflake database by submitting the database
metadata to the SQLFlow Cloud version, You may set up the [SQLFlow on-premise version](https://www.gudusoft.com/sqlflow-on-premise-version/)
on your server to secure your information.

For more options of the grabit tool, please check this page.
- [Grabit tool readme](https://github.com/sqlparser/sqlflow_public/tree/master/grabit)

The completed guide of SQLFlow UI
- [How to use SQLFlow](https://github.com/sqlparser/sqlflow_public/blob/master/sqlflow_guide.md)
