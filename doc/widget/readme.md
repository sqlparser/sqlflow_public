# SQLFlow widget
The SQLFlow widget is a Javascript library that enables instantaneous data lineage visualisation on your website.

The SQLFlow widet must work together with the Gudu SQLFlow backend
in order to visualize the data lineage and provides an actionable diagram.

- [SQLFlow widget](#sqlflow-widget)
    + [1. Online demo](#1-online-demo)
    + [2. Get started](#2-get-started)
      - [Files](#files)
    + [3. Parameter](#3-parameter)
    + [4. demos](#4-demos)
      - [4.1 visualize sql text](#41-visualize-sql-text)
      - [4.2 visualize a job](#42-visualize-a-job)
      - [4.3  visualize a specific database object in a job](#43--visualize-a-specific-database-object-in-a-job)
      - [4.4  set data lineage options of job](#44--set-data-lineage-options-of-job)
      - [4.5  set data lineage options of SQL query](#45--set-data-lineage-options-of-sql-query)
      - [4.6  visualize a json object embedded in html page](#46--visualize-a-json-object-embedded-in-html-page)
      - [4.7  visualize data lineage in a separate json file](#47--visualize-data-lineage-in-a-separate-json-file)
      - [4.8  How to get error message](#48--how-to-get-error-message)
      - [4.9  Event: add an event listener on field(column) click](#49--event--add-an-event-listener-on-field-column--click)
      - [4.10,11?](#410-11-)
      - [4.12 Access data lineage from url dierctly](#412-access-data-lineage-from-url-dierctly)
      - [4.14 Visualize the lineage data using Vue](#414-visualize-the-lineage-data-using-vue)
      - [4.15  Event: add an event listener on table click](#415--event--add-an-event-listener-on-table-click)
    + [5. SQLFlow widget api reference](#5-sqlflow-widget-api-reference)
      - [5.1 vendor.set(value: Vendor)](#51-vendorset-value--vendor-)
      - [5.2 vendor.get(): Vendor](#52-vendorget----vendor)
      - [5.3 sqltext.set(value: string): void](#53-sqltextset-value--string---void)
      - [5.4 sqltext.get(): string](#54-sqltextget----string)
      - [5.5 visualize(): Promise\<void\>](#55-visualize----promise--void--)
      - [5.6 job.lineage.viewDetailById(jobId?: string): Promise\<void\>](#56-joblineageviewdetailbyid-jobid---string---promise--void--)
      - [5.7 job.lineage.selectGraph(options: { database?: string; schema?: string; table?: string; column?: string;}): Promise\<void\>](#57-joblineageselectgraph-options----database---string--schema---string--table---string--column---string-----promise--void--)
      - [5.8 addEventListener(event: Event, callback: Callback): void](#58-addeventlistener-event--event--callback--callback---void)
        * [5.8.1 Event：'onFieldClick'](#581-event--onfieldclick-)
      - [5.9 removeEventListener(event: Event, callback: Callback): void](#59-removeeventlistener-event--event--callback--callback---void)
      - [5.10 removeAllEventListener(): void](#510-removealleventlistener----void)


### 1. Online demo

The SQLFlow widget is shipped together with [the SQLFlow On-Premise version](https://www.gudusoft.com/sqlflow-on-premise-version/).
No online demo is available currently.

Once the SQLFlow widget is installed on your server, you can access the SQLFlow widget with the url like:
https://127.0.0.1/widget


### 2. Get started

#### Files

```
├── index.html
├── jquery.min.js
├── sqlflow.widget.2.4.9.css
└── sqlflow.widget.2.4.9.js
└── 1\
└── 2\
└── 3\
└── ...
```

>Please note that the version number in the file will changed constantly.


Add `sqlflow.widget.2.4.9.js` in index.html, during the execution of the JS, a new iframe will be created, and the css from js will be embedded into the iframe,
no additional css is needed.

jquery is optional, and is inlcuded for the demostration only.

```html
<!DOCTYPE html>
<html lang="zh-CN">
    <head>
        <meta charset="UTF-8" />
        <title>widget</title>
        <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js"></script>
        <script src="sqlflow.widget.2.4.9.js"></script>
        <script src="index.js"></script>
    </head>

    <body>
        <div id="sqlflow"></div>
    </body>
</html>
```

Insert the following code in index.js:

```js
$(async () => {
    // get a instance of SQLFlow
    const sqlflow = await SQLFlow.init({
        container: document.getElementById('sqlflow'),
        width: 1000,
        height: 315,
        apiPrefix: 'http://127.0.0.1/api',
    });

    // set dbvendor property
    sqlflow.vendor.set('oracle');

    // set sql text property
    sqlflow.sqltext.set(`CREATE VIEW vsal 
    AS 
      SELECT a.deptno                  "Department", 
             a.num_emp / b.total_count "Employees", 
             a.sal_sum / b.total_sal   "Salary" 
      FROM   (SELECT deptno, 
                     Count()  num_emp, 
                     SUM(sal) sal_sum 
              FROM   scott.emp 
              WHERE  city = 'NYC' 
              GROUP  BY deptno) a, 
             (SELECT Count()  total_count, 
                     SUM(sal) total_sal 
              FROM   scott.emp 
              WHERE  city = 'NYC') b 
    ;`);

    sqlflow.visualize();
});
```


### 3. Parameter

| name      | detail                                                               | type             |   optional  |
| --------- | ------------------------------------------------------------------ | ---------------- | ---- |
| container | the html element where sqlflow is attached                         | HTMLElement      | no |
| apiPrefix | the url of sqlflow backend                                         | string           | no |
| width     | width of container, both percent and fix length can be used like "100%", or 800px | string \| number | no |
| height    | height of container, both percent and fix length can be used like "100%", or 800px | string \| number | no |

### 4. demos

#### 4.1 visualize sql text
Visualize the data lineage after analyzing the input SQL query.

- input: SQL text
- output: data lineage diagram

All necessary files are under this directory.
```
└── 1\
```


#### 4.2 visualize a job

Visualize the data lineage in a [SQLFlow Job](https://docs.gudusoft.com/introduction/getting-started/different-modes-in-gudu-sqlflow).
The SQLFlow job must be already created.

- input: a SQLFlow job id, or leave it empty to view the latest job 
- output: data lineage diagram


All necessary files are under this directory.
```
└── 2\
```

```js
$(async () => {
    const sqlflow = await SQLFlow.init({
        container: document.getElementById('demo-2'),
        width: 1000,
        height: 800,
        apiPrefix: 'http://101.43.8.206/api',
    });

    // view job detail by job id, or leave it empty to view the latest job
    await sqlflow.job.lineage.viewDetailById('b38273ec356d457bb98c6b3159c53be3');
});
```

#### 4.3  visualize a specific database object in a job
Visualize the data lineage of a specified table or column in a SQLFlow job.

- input: a SQLFlow job id, or leave it empty to view the latest job 
- input: database, schema, table, column. 
    * If the column is omitted, return the data lineage for the specified table.
	* if the table and column are ommited, return the data lineage for the specified schema.
	* if the schema, table and column are ommited, return the data lineage for the specified database.
- output: data lineage diagram


All necessary files are under this directory.
```
└── 3\
```

```js
$(async () => {
    const sqlflow = await SQLFlow.init({
        container: document.getElementById('sqlflow'),
        width: 1000,
        height: 700,
        apiPrefix: 'http://101.43.8.206/api',
    });

    // view job detail by job id, or leave it empty to view the latest job
    await sqlflow.job.lineage.viewDetailById('b38273ec356d457bb98c6b3159c53be3');

    sqlflow.job.lineage.selectGraph({
        database: 'DWDB', //
        schema: 'DBO',
        table: '#TMP',
        column: 'NUMBER_OFOBJECTS',
    });
});
```


#### 4.4  set data lineage options of job
Once the job is created, lineage options can't be changed.
So this demo doesn't work any longer.

All necessary files are under this directory.
```
└── 4\
```

#### 4.5  set data lineage options of SQL query
Using the setting to control the output of data lineage of a SQL query.

![gudu sqoflow settings](gudu-sqlflow-settings.png)

All necessary files are under this directory.
```
└── 5\
```

#### 4.6  visualize a json object embedded in html page
A json object that includes the lineage data is embedded in the html page,
SQLFlow will visualize this json object and show the actionable diagram.

Since all layout data is included in the json file, the SQLFlow widget 
will draw the diagram and needn't to connect to the SQLFlow backend.

So, this SQLFlow widget can work without the installation of the Gudu SQLFlow.

All necessary files are under this directory.
```
└── 6\
```

#### 4.7  visualize data lineage in a separate json file
Read and visualize the data lineage in a json file.
This json file should be accessable in the same server as the SQLFlow widget.

Since all layout data is included in the json file, the SQLFlow widget 
will draw the diagram and needn't to connect to the SQLFlow backend.

So, this SQLFlow widget can work without the installation of the Gudu SQLFlow.

All necessary files are under this directory.
```
└── 7\
```



#### 4.8  How to get error message
Show how to get error message after processing input SQL qurey.

All necessary files are under this directory.
```
└── 8\
```


#### 4.9  Event: add an event listener on field(column) click
Add an event listener on field(column) click, so you can get detailed 
information about the field(column) that been clicked.

All necessary files are under this directory.
```
└── 9\
```

#### 4.10,11?

free style?

All necessary files are under this directory.
```
└── 10\
```

#### 4.12 Access data lineage from url dierctly

User can access the data lineage through a url directly by specify the data lineage type, table and column.

```
http://127.0.0.1/widget/12?type=upstream&table=dbo.emp
http://127.0.0.1/widget/12?type=upstream&table=dbo.emp&column=salary
```

- input 
  * type,  upstream or downstream
  * table,
  * column, if column is omitted, return the lineage for table.


All necessary files are under this directory.
```
└── 12\


#### 4.13 Visualize a csv file that includes lineage data
The format of the csv
```csv
source_db,source_schema,source_table,source_column,target_db,target_schema,target_table,target_column,relation_type,effect_type
D1E9IQ1AE488E4,DBT_TESTS,STG_PAYMENTS,AMOUNT,DEFAULT,DEFAULT,RS-5,COUPON_AMOUNT,fdd,select
D1E9IQ1AE488E4,DBT_TESTS,STG_ORDERS,ORDER_ID,DEFAULT,DEFAULT,RS-5,ORDER_ID,fdd,select
D1E9IQ1AE488E4,DBT_TESTS,STG_ORDERS,STATUS,DEFAULT,DEFAULT,RS-5,STATUS,fdd,select
D1E9IQ1AE488E4,DBT_TESTS,STG_PAYMENTS,AMOUNT,DEFAULT,DEFAULT,RS-5,CREDIT_CARD_AMOUNT,fdd,select
D1E9IQ1AE488E4,DBT_TESTS,STG_PAYMENTS,AMOUNT,DEFAULT,DEFAULT,RS-5,GIFT_CARD_AMOUNT,fdd,select
D1E9IQ1AE488E4,DBT_TESTS,STG_ORDERS,ORDER_DATE,DEFAULT,DEFAULT,RS-5,ORDER_DATE,fdd,select
D1E9IQ1AE488E4,DBT_TESTS,STG_PAYMENTS,AMOUNT,DEFAULT,DEFAULT,RS-5,AMOUNT,fdd,select
D1E9IQ1AE488E4,DBT_TESTS,STG_ORDERS,CUSTOMER_ID,DEFAULT,DEFAULT,RS-5,CUSTOMER_ID,fdd,select
D1E9IQ1AE488E4,DBT_TESTS,STG_PAYMENTS,AMOUNT,DEFAULT,DEFAULT,RS-5,BANK_TRANSFER_AMOUNT,fdd,select
```

All necessary files are under this directory.
```
└── 13\
```

#### 4.14 Visualize the lineage data using Vue
The SQLFlow provides a Vue library to support Vue framework.

```
└── 14\
```


#### 4.15  Event: add an event listener on table click
Add an event listener on table click, so you can get detailed 
information about the table that been clicked.

```
└── 15\
```


### 5. SQLFlow widget api reference

#### 5.1 vendor.set(value: Vendor)

set the type of database vendor, Vendor is an enum type.

```ts
type Vendor =
    | 'athena'
    | 'azuresql'
    | 'bigquery'
    | 'couchbase'
    | 'db2'
    | 'greenplum'
    | 'hana'
    | 'hive'
    | 'impala'
    | 'informix'
    | 'mdx'
    | 'mysql'
    | 'netezza'
    | 'openedge'
    | 'oracle'
    | 'postgresql'
    | 'presto'
    | 'redshift'
    | 'snowflake'
    | 'sparksql'
    | 'mssql'
    | 'sybase'
    | 'teradata'
    | 'vertica';
```

#### 5.2 vendor.get(): Vendor

return the current database vendor.

#### 5.3 sqltext.set(value: string): void

set the input sql query that need to be processed.

#### 5.4 sqltext.get(): string

Return the current SQL query text.

#### 5.5 visualize(): Promise\<void\>

Show the diagram related to current input SQL.

#### 5.6 job.lineage.viewDetailById(jobId?: string): Promise\<void\>

Show the diagram of a specific job. if the job id is omitted, 
show the diagram of the top job, if no top job is found, show the diagram of latest job.

#### 5.7 job.lineage.selectGraph(options: { database?: string; schema?: string; table?: string; column?: string;}): Promise\<void\>

Show the lineage diagram of a specific table/column.  `job.lineage.viewDetailById` must be called first before calling this function,
and this function can be called multiple times to return diagram for different table/columns.


#### 5.8 addEventListener(event: Event, callback: Callback): void

Add an event listner.

Callback：(data) => any

##### 5.8.1 Event：'onFieldClick'

This event fired when the column in the diagram is clicked.

data：

| Attribute     | Type                | Comment |
| -------- | ------------------- | ---- |
| database | string \| undefined | name |
| schema   | string \| undefined | name |
| table    | string \| undefined | name |
| column   | string              | name |

#### 5.9 removeEventListener(event: Event, callback: Callback): void

Remove a event listner.

#### 5.10 removeAllEventListener(): void

Remove all event listners.
