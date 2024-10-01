## Intermediate result set

[toc]

### 1. What is intermediate result set?

In the SQLFlow, intermediate result set is the result set of a select statement.

The intermediate result set is used to show the details of the data flow and let you know exactly what is going on. 

The intermediate result set is always built in order to create a complete data flow graph. However, you may choose to hide the intermediate result set in the UI in order to make the data flow graph cleaner in a big data flow scenario.

For example:

```sql
CREATE VIEW v1 AS
SELECT EmployeeID, FirstName, LastName, ManagerID, EmpLevel  -- resultset1
FROM Employees
WHERE ManagerID IS NULL
```

The intermediate result set is:

```
EmployeeID, FirstName, LastName, ManagerID, EmpLevel
```
in the select list and shown in the data flow graph as below:

![intermediate-resultset](../../assets/images/get-started-intermediate-resultset1.png)

### CTE example:

CTE will be treated as a intermediate result set.
<a name="cte-example">
```sql
CREATE VIEW V1 AS
WITH
  cteReports (EmpID, FirstName, LastName, MgrID, EmpLevel)
  AS
  (
    SELECT EmployeeID, FirstName, LastName, ManagerID, EmpLevel  -- resultset1
    FROM Employees
    WHERE ManagerID IS NULL
  )
SELECT
  count(EmpID), sum(EmpLevel)  -- resultset2
FROM cteReports 
```
</a>
So, there are there intermediate result sets:

1. resultset1: EmployeeID, FirstName, LastName, ManagerID, EmpLevel
2. cte: cteReports (EmpID, FirstName, LastName, MgrID, EmpLevel) 
3. resultset2: count(EmpID), sum(EmpLevel)

And the data flow graph is like this:

![intermediate-resultset](../../assets/images/get-started-intermediate-resultset2.png)

### 2. SQL clauses that generate intermediate result set

#### 1. select list
```sql
SELECT EmployeeID, FirstName, LastName, ManagerID, EmpLevel  FROM Employees
```

the intermediate result set generated: (a `resultset` XML tag and type attribute value `select_list`)

```xml
<resultset id="11" name="RS-1" type="select_list">
    <column id="12" name="EmployeeID"/>
    <column id="13" name="FirstName"/>
    <column id="14" name="LastName"/>
    <column id="15" name="ManagerID"/>
    <column id="16" name="EmpLevel"/>
</resultset>
```


#### 2. cte
[CTE example SQL](#cte-example), the intermediate result set generated: (a `resultset` XML tag and type attribute value `with_cte`)
```xml
<resultset id="4" name="CTE-CTEREPORTS-1" type="with_cte">
    <column id="5" name="EmpID"/>
    <column id="6" name="FirstName"/>
    <column id="7" name="LastName"/>
    <column id="8" name="MgrID"/>
    <column id="9" name="EmpLevel"/>
    <column id="3" name="RelationRows" source="system"/>
</resultset>
```

#### 3. set clause in update statement
```sql
UPDATE table1 t1 JOIN table2 t2 ON t1.field1 = t2.field1 
SET t1.field2=t2.field2 --mysql
```

the intermediate result set generated: (a `resultset` XML tag and type attribute value `update-set`)

```xml
<resultset id="11" name="UPDATE-SET-1" type="update-set">
    <column id="12" name="field2"/>
    <column id="10" name="RelationRows" source="system"/>
</resultset>
```

![update-set](../../assets/images/get-started-intermediate-resultset3.png)

#### 4. merge statement

```sql
-- bigquery sample SQL
MERGE dataset.DetailedInventory T USING dataset.Inventory S ON T.product = S.product
WHEN NOT MATCHED AND s.quantity < 20 THEN
  INSERT(product, quantity, supply_constrained, comments)
  VALUES(product, quantity, true, ARRAY<STRUCT<created DATE, comment STRING>>[(DATE('2016-01-01'), 'comment1')])
WHEN NOT MATCHED THEN
  INSERT(product, quantity, supply_constrained)
  VALUES(product, quantity, false)
;
```

the intermediate result set generated: (a `resultset` XML tag with type attribute value `merge-insert`)

```xml
<resultset id="11" name="MERGE-INSERT-1" type="merge-insert">
    <column id="12" name="product"/>
    <column id="15" name="quantity"/>
    <column id="18" name="supply_constrained"/>
    <column id="20" name="comments"/>
</resultset>
<resultset id="23" name="MERGE-INSERT-2" type="merge-insert">
    <column id="24" name="product"/>
    <column id="25" name="quantity"/>
    <column id="26" name="supply_constrained"/>
</resultset>
```

#### 5. other SQL clauses

### 3. resultset ouput but not a relation

#### (1) Function
Due to historical design reasons, some SQL clauses will generate a result set but it is not a relation. The most common example is the SQL function that returns a scalar value.

```sql
SELECT COUNT(*) FROM Employees
```

the intermediate result set generated: (a `resultset` XML tag and type attribute value `scalar`)

```xml
<resultset id="9" name="COUNT" type="function">
    <column id="10" name="COUNT"/>
</resultset>
```

This result is not a true intermediate result set, but rather a scalar value. However, we can distinguish it from other intermediate result sets by examining the `type` attribute. In this case, the `type` attribute has a value of `function`, indicating that it represents the output of a SQL function rather than a traditional result set.

This distinction is important for understanding how different SQL operations are represented in the intermediate result structure. While tables and subqueries typically produce relational result sets, functions often return single values, which are handled differently in the data lineage analysis.

#### (2) Constant

Constants used in the SQL statement will be collected and saved in a pseduo table: `constantTable`.
Each SQL statement will create a `constantTable` table to save the constants used in the SQL statement.

So SQLFlow able to generate the data flow to trace the constant value.
> Constants only will be collected when the /showConstant is set to true in the SQLFlow.
and constants used in the insert statement WILLNOT BE collected in order to avoid too many constants even if the /showConstant is set to true.

>By default, the /showConstant is set to false in the SQLFlow which means constants will not be collected.

```sql
SELECT 'constant' as field1, 2 as field2;
```

a `table` XML tag and type attribute value `constantTable`:

```xml
  <table id="5" name="SQL_CONSTANTS-1" type="constantTable">
      <column id="6" name="'constant'"/>
      <column id="8" name="2"/>
  </table>
```

```sql
UPDATE table1 t1 JOIN table2 t2 ON t1.field1 = t2.field1 
SET t1.field2='constant' and t1.field3=2;
```

a `table` XML tag and type attribute value `constantTable`:

```xml
  <table id="15" name="SQL_CONSTANTS-1" type="constantTable">
      <column id="16" name="'constant'"/>
      <column id="17" name="2"/>
  </table>
```
