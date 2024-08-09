## table

Table type represents the table object in a relational database.

It also represents the derived table such as function table.

struct definition

```json
{
    "elementName" : "table",
    "attributeDefs": [
        {
            "name": "id",
            "typeName": "int",
            "isOptional": false,
            "isUnique": true
        },
        {
            "name": "name",
            "typeName": "string",
            "isOptional": false
        },
        {
            "name": "alias",
            "typeName": "string",
            "isOptional": true
        },
        {
            "name": "type",
            "typeName": "string",
            "isOptional": false
        },
        {
            "name": "subType",
            "typeName": "string",
            "isOptional": false
        },  
        {
            "name": "database",
            "typeName": "string",
            "isOptional": true
        },  
        {
            "name": "schema",
            "typeName": "string",
            "isOptional": true
        },  
        {
            "name": "coordinate",
            "typeName": "string",
            "isOptional": true
        },  
        {
            "name": "processIds",
            "typeName": "int",
            "isOptional": true
        },  
        {
            "name": "columns",
            "typeName": "array<column>",
            "isOptional": true
        } 
    ]
}
```

### id

unique id in the output.

### name

table name in the original SQL query.

### alias

alias of the table in the original SQL query.

### type

type of the table, available value: `table`,`pseudoTable`

- table

This means a base table found in the SQL query.

```sql
create view v123 as select a,b 
from employee a, name b 
where employee.id = name.id
```

```xml
<table id="2" name="employee" alias="a" type="table">
```

- constantTable

  ```sql
  update t1 set f1 =3
  ```

  In order to link constant 3 to f1, we create a constant table with the name SQL_CONSTANTS includes a single column to save the constant.

  ```xml
  <table id="11" name="SQL_CONSTANTS" type="constantTable">
  	<column id="12" name="3" />
  </table>
  ```
- pseudoTable

Due to the lack of metadata information, some columns can't be linked to a table correctly.
Those columns will be assigned to a pseudo table with name: `pseudo_table_include_orphan_column`.
The type of this table is `pseudoTable`.

In the following sample sql, columm `a`, `b` can't be linked to a specific table without enough information,
so a pseudo table with name `pseudo_table_include_orphan_column` is created to contain those orphan columns.

```sql
create view v123 as 
select a,b from employee a, name b where employee.id = name.id
```

```xml
<table id="11" name="pseudo_table_include_orphan_column" type="pseudoTable" coordinate="[1,1,f904f8312239df09d5e008bb9d69b466],[1,35,f904f8312239df09d5e008bb9d69b466]">
	<column id="12" name="a" coordinate="[1,28,f904f8312239df09d5e008bb9d69b466],[1,29,f904f8312239df09d5e008bb9d69b466]"/>
	<column id="14" name="b" coordinate="[1,30,f904f8312239df09d5e008bb9d69b466],[1,31,f904f8312239df09d5e008bb9d69b466]"/>
</table>
```

### subType

In the most case of SQL query, the table used is a base table.
However, derived tables are also used in the from clause or other places.

The `subType` property in the `table` element tells you what kind of the derived table this table is.

Take the following sql for example, `WarehouseReporting.dbo.fnListToTable` is a function that
used as a derived table. So, the value of `subType` is `function`.

Currently(GSP 2.2.0.6), `function` is the only value of `subType`. More value of `tableType` will be added in the later version
such as `JSON_TABLE` for JSON_TABLE.

```sql
select entry as Account FROM WarehouseReporting.dbo.fnListToTable(@AccountList)
```

```xml
<table id="2" database="WarehouseReporting" schema="dbo" name="WarehouseReporting.dbo.fnListToTable" type="table" tableType="function" coordinate="[1,30,15c3ec5e6df0919bb570c4d8cdd66651],[1,87,15c3ec5e6df0919bb570c4d8cdd66651]">
	<column id="3" name="entry" coordinate="[1,8,15c3ec5e6df0919bb570c4d8cdd66651],[1,13,15c3ec5e6df0919bb570c4d8cdd66651]"/>
</table>
```

### database

The database this table belongs to.

### schema

The schema this table belongs to.

### coordinate

Indicates the positions the table occurs in the SQL script.

`coordinate="[1,37,0],[1,47,0]"`

the first number is line， the second number is column, the third number is SQL script index of task. SqlInfoHelper uses the third number to position SQL script.

### processIds

The Id of the process which is doing the transformation related to this table. This `processIds` is used when generate table-level lineage model.

### columns

Array of `column` beblogs to this table.
