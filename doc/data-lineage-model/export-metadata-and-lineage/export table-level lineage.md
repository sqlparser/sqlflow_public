### table-level lineage

The exported table-level linege should be in format like this:

```
source_db;source_schema;source_table;target_db;target_schema;target_table;procedure_names;query_hash_id
```

#### sample sql

```sql
CREATE VIEW dbo.hiredate_view  
AS   
SELECT p.FirstName, p.LastName, e.BusinessEntityID, e.HireDate  
FROM HumanResources.Employee e   
JOIN Person.Person AS p ON e.BusinessEntityID = p.BusinessEntityID ; 
```

#### lineage in XML

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<dlineage>
    <process id="19" name="Query Create View" type="Create View" coordinate="[1,1,0],[5,69,0]"/>
    <table id="2" schema="HumanResources" name="HumanResources.Employee" alias="e" type="table" coordinate="[4,6,0],[4,31,0]"/>
    <table id="7" schema="Person" name="Person.Person" alias="p" type="table" coordinate="[5,6,0],[5,24,0]"/>
    <view id="18" schema="dbo" name="dbo.hiredate_view" type="view" processIds="19" coordinate="[1,13,0],[1,30,0]"/>
    <relation id="1007" type="fdd">
        <target id="1008" target_id="19" target_name="Query Create View"/>
        <source id="1002" source_id="7" source_name="Person.Person"/>
    </relation>
    <relation id="1009" type="fdd">
        <target id="1001" target_id="18" target_name="dbo.hiredate_view"/>
        <source id="1010" source_id="19" source_name="Query Create View"/>
    </relation>
    <relation id="1011" type="fdd">
        <target id="1012" target_id="19" target_name="Query Create View"/>
        <source id="1005" source_id="2" source_name="HumanResources.Employee"/>
    </relation>
    <relation id="1013" type="fdd">
        <target id="1004" target_id="18" target_name="dbo.hiredate_view"/>
        <source id="1014" source_id="19" source_name="Query Create View"/>
    </relation>
</dlineage>
```

#### diagram

![image.png](https://images.gitee.com/uploads/images/2021/0709/145303_36edb228_8136809.png)

#### exported lineage

```xml
source_db;source_schema;source_table;target_db;target_schema;target_table;procedure_names;query_hash_id
default;person;person;default;dbo;hiredate_view;batchQueries;xxxxx
default;HumanResources;Employee;default;dbo;hiredate_view;batchQueries;xxxxx

```

The table name in the exported lineage **shoudn't be qualified** , it must be like this `Employee`.  But when it is written to the data catalog such as Atlas, it must be qualified like this:  `default.HumanResources.Employee`
