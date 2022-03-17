# SQLFlow widget

> The frontend for SQLFlow widget

### 1. Online demo

http://101.43.8.206/widget/

### 2. Get started

#### Files

```
├── index.html
├── index.js
├── sqlflow.widget.2.4.9.css
└── sqlflow.widget.2.4.9.js
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
        apiPrefix: 'http://101.43.8.206/api',
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

You can find the execution result here: [demo：visualize sqltext](http://101.43.8.206/widget/1/#/)

### 3. Parameter

| name      | detail                                                               | type             |   optional  |
| --------- | ------------------------------------------------------------------ | ---------------- | ---- |
| container | the html element where sqlflow is attached                         | HTMLElement      | no |
| apiPrefix | the url of sqlflow backend                                         | string           | no |
| width     | width of container, both percent and fix length can be used like "100%", or 800px | string \| number | no |
| height    | height of container, both percent and fix length can be used like "100%", or 800px | string \| number | no |

### 4. demos

#### 4.1 visualize a job

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

Result: [demo：visualize a job](http://101.43.8.206/widget/2/#/)

#### 4.2  visualize schema of a job

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

result: [demo：visualize schema of a job](http://101.43.8.206/widget/2/#/)

#### 4.3  add an event listener on field(column) click

```js
$(async () => {
    // get a instance of SQLFlow
    const sqlflow = await SQLFlow.init({
        container: document.getElementById('sqlflow'),
        width: 1000,
        height: 400,
        apiPrefix: 'http://101.43.8.206/api',
        token: '', // input your token
    });

    // add an event listener on field(column) click
    sqlflow.addEventListener('onFieldClick', field => {
        $message.val(JSON.stringify(field));

        // remove all event listeners
        // sqlflow.removeAllEventListener()
    });

    // set sql text property
    sqlflow.sqltext.set('select d from a.b.c');

    visualize();
});
```

result: [demo：add an event listener on field(column) click](http://101.43.8.206/widget/9/#/)

### 5. sqlflow instance api

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
