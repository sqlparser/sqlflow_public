Embed the SQLFlow UI into your application

# Get started

Firstly, [download](https://github.com/sqlparser/sqlflow_public/tree/master/sqlflowjs) the sqlflow.js, css and font.

Secondly, create a new file, insert sqlflow.js and sqlflow.css in the head.

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <!-- use jquery, this is optional -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/1.11.0/jquery.min.js" integrity="sha256-spTpc4lvj4dOkKjrGokIrHkJgNA0xMS98Pw9N7ir9oI=" crossorigin="anonymous"></script>
    <!-- insert sqlflow.js and sqlflow.css in the head -->
	<script type="text/javascript" src="sqlflow.js"></script>
	<link href="sqlflow.css" rel="stylesheet">
</head>
<body>
</body>
</html>

```

Lastly, create a root element, and create a SQLFlow instance on that element.

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <!-- use jquery, this is optional -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/1.11.0/jquery.min.js" integrity="sha256-spTpc4lvj4dOkKjrGokIrHkJgNA0xMS98Pw9N7ir9oI=" crossorigin="anonymous"></script>
    <!-- insert sqlflow.js and sqlflow.css in the head -->
	<script type="text/javascript" src="sqlflow.js"></script>
	<link href="sqlflow.css" rel="stylesheet">
</head>
<body>
    <!-- create a root element -->
    <div id="app"></div>
</body>

<script>
	$(function () {
        // create an instance
		var sqlflow = new SQLFlow({
			el: document.getElementById("app"),
		});

        // set a dbvendor
		sqlflow.setDbvendor("oracle");

        // set sql text
		sqlflow.setSQLText("CREATE VIEW vsal \n" +
				"AS \n" +
				"  SELECT a.deptno                  \"Department\", \n" +
				"         a.num_emp / b.total_count \"Employees\", \n" +
				"         a.sal_sum / b.total_sal   \"Salary\" \n" +
				"  FROM   (SELECT deptno, \n" +
				"                 Count()  num_emp, \n" +
				"                 SUM(sal) sal_sum \n" +
				"          FROM   scott.emp \n" +
				"          WHERE  city = 'NYC' \n" +
				"          GROUP  BY deptno) a, \n" +
				"         (SELECT Count()  total_count, \n" +
				"                 SUM(sal) total_sal \n" +
				"          FROM   scott.emp \n" +
				"          WHERE  city = 'NYC') b \n" +
				";\n" +
				"\n" +
				"INSERT ALL\n" +
				"\tWHEN ottl < 100000 THEN\n" +
				"\t\tINTO small_orders\n" +
				"\t\t\tVALUES(oid, ottl, sid, cid)\n" +
				"\tWHEN ottl > 100000 and ottl < 200000 THEN\n" +
				"\t\tINTO medium_orders\n" +
				"\t\t\tVALUES(oid, ottl, sid, cid)\n" +
				"\tWHEN ottl > 200000 THEN\n" +
				"\t\tinto large_orders\n" +
				"\t\t\tVALUES(oid, ottl, sid, cid)\n" +
				"\tWHEN ottl > 290000 THEN\n" +
				"\t\tINTO special_orders\n" +
				"SELECT o.order_id oid, o.customer_id cid, o.order_total ottl,\n" +
				"o.sales_rep_id sid, c.credit_limit cl, c.cust_email cem\n" +
				"FROM orders o, customers c\n" +
				"WHERE o.customer_id = c.customer_id;");

         // visualize it
		sqlflow.visualize();
	});
</script>
</html>

```

you can [open this simple demo](http://111.229.12.71/sqlflowjs/sqlflow.js_get_start.html) in browser.

## SQLFlow.js api

you can [open the complete demo](http://111.229.12.71/sqlflowjs/) in browser.

### SQLFlow(options)

create a new instance

options:

```json
{
	el: HTMLElement,
}
```

### SQLFlow.setDbvendor( dbvendor : string )

set dbvendor of sql

dbvendor : "bigquery" | "couchbase" | "db2" | "greenplum" | "hana" | "hive" | "impala" | "informix" | "mysql" | "netezza" | "openedge" | "oracle" | "postgresql" | "redshift" | "snowflake" | "mssql" | "sybase" | "teradata" | "vertica"

default : "oracle"

### SQLFlow.setSQLText( sqltext : string )

set sql

### SQLFlow.visualize()

visualize relations

### SQLFlow.visualizeJoin()

visualize join relations

### SQLFlow.setting

get current setting of sqlflow instance

### SQLFlow.setHideAllColumns( value : boolean)

change sqlflow instance setting

### SQLFlow.setDataflow( value : boolean)

change sqlflow instance setting

### SQLFlow.setImpact( value : boolean)

change sqlflow instance setting

### SQLFlow.setShowIntermediateRecordset( value : boolean)

change sqlflow instance setting

### SQLFlow.setShowFunction( value : boolean)

change sqlflow instance setting