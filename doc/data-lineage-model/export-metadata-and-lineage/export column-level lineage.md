### column-level lineage

The exported column-level linege should be in format like this:

```
source_db;source_schema;source_table;source_column;target_db;target_schema;target_table;target_column;procedure_names;query_hash_id
```

the exported column-level lineage **shouldn't include any intermediate recordset**, it only inclues the source and target table column, the hasd id of the query which does this transformation.

#### sample sql

```sql
CREATE VIEW dbo.hiredate_view(FirstName,LastName)  
AS   
SELECT p.FirstName, p.LastName
from Person.Person AS p 
GO 

update dbo.hiredate_view h
set  h.FirstName =  p.FirstName
from h join Person.Person p 
on h.id = p.id;

insert into  dbo.hiredate_view (FirstName,LastName)   
SELECT p.FirstName, p.LastName
from Person.Person AS p ;
```

#### column-level lineage in xml

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<dlineage>
    <process id="11" name="Query Create View" type="Create View" coordinate="[1,1,0],[4,27,0]"/>
    <process id="14" name="Query Update" type="Update" coordinate="[7,1,0],[10,16,0]"/>
    <process id="21" name="Query Insert" type="Insert" coordinate="[12,1,0],[14,26,0]"/>
    <table id="2" schema="Person" name="Person.Person" alias="p" type="table" coordinate="[4,6,0],[4,24,0]">
        <column id="28" name="FirstName" coordinate="[3,8,0],[3,19,0]"/>
        <column id="29" name="LastName" coordinate="[3,21,0],[3,31,0]"/>
        <column id="20" name="id" coordinate="[10,11,0],[10,15,0]"/>
    </table>
    <view id="10" schema="dbo" name="dbo.hiredate_view" type="view" processIds="11 14 21" coordinate="[1,13,0],[1,30,0]">
        <column id="12" name="FirstName" coordinate="[1,31,0],[1,40,0]"/>
        <column id="13" name="LastName" coordinate="[1,41,0],[1,49,0]"/>
        <column id="19" name="id" coordinate="[10,4,0],[10,8,0]"/>
    </view>
    <resultset id="6" name="RS-1" type="select_list" coordinate="[3,8,0],[3,31,0]">
        <column id="7" name="FirstName" coordinate="[3,8,0],[3,19,0]"/>
        <column id="8" name="LastName" coordinate="[3,21,0],[3,31,0]"/>
    </resultset>
    <resultset id="25" name="INSERT-SELECT-1" type="insert-select" coordinate="[13,8,0],[13,31,0]">
        <column id="26" name="FirstName" coordinate="[13,8,0],[13,19,0]"/>
        <column id="27" name="LastName" coordinate="[13,21,0],[13,31,0]"/>
    </resultset>
    <resultset id="16" name="UPDATE-SET-1" type="update-set" coordinate="[7,1,0],[10,16,0]">
        <column id="17" name="FirstName" coordinate="[8,6,0],[8,17,0]"/>
        <column id="15" name="PseudoRows" coordinate="[7,1,0],[10,16,0]" source="system"/>
    </resultset>
    <relation id="1" type="fdd" effectType="select">
        <target id="7" column="FirstName" parent_id="6" parent_name="RS-1" coordinate="[3,8,0],[3,19,0]"/>
        <source id="28" column="FirstName" parent_id="2" parent_name="Person.Person" coordinate="[3,8,0],[3,19,0]"/>
    </relation>
    <relation id="2" type="fdd" effectType="select">
        <target id="8" column="LastName" parent_id="6" parent_name="RS-1" coordinate="[3,21,0],[3,31,0]"/>
        <source id="29" column="LastName" parent_id="2" parent_name="Person.Person" coordinate="[3,21,0],[3,31,0]"/>
    </relation>
    <relation id="3" type="fdd" effectType="create_view">
        <target id="12" column="FirstName" parent_id="10" parent_name="dbo.hiredate_view" coordinate="[1,31,0],[1,40,0]"/>
        <source id="7" column="FirstName" parent_id="6" parent_name="RS-1" coordinate="[3,8,0],[3,19,0]"/>
    </relation>
    <relation id="4" type="fdd" effectType="create_view">
        <target id="13" column="LastName" parent_id="10" parent_name="dbo.hiredate_view" coordinate="[1,41,0],[1,49,0]"/>
        <source id="8" column="LastName" parent_id="6" parent_name="RS-1" coordinate="[3,21,0],[3,31,0]"/>
    </relation>
    <relation id="5" type="fdd" effectType="update">
        <target id="17" column="FirstName" parent_id="16" parent_name="UPDATE-SET-1" coordinate="[8,6,0],[8,17,0]"/>
        <source id="28" column="FirstName" parent_id="2" parent_name="Person.Person" coordinate="[3,8,0],[3,19,0]"/>
    </relation>
    <relation id="6" type="fdd" effectType="update">
        <target id="12" column="FirstName" parent_id="10" parent_name="dbo.hiredate_view" coordinate="[1,31,0],[1,40,0]"/>
        <source id="17" column="FirstName" parent_id="16" parent_name="UPDATE-SET-1" coordinate="[8,6,0],[8,17,0]"/>
    </relation>
    <relation id="8" type="fdd" effectType="select">
        <target id="26" column="FirstName" parent_id="25" parent_name="INSERT-SELECT-1" coordinate="[13,8,0],[13,19,0]"/>
        <source id="28" column="FirstName" parent_id="2" parent_name="Person.Person" coordinate="[3,8,0],[3,19,0]"/>
    </relation>
    <relation id="9" type="fdd" effectType="select">
        <target id="27" column="LastName" parent_id="25" parent_name="INSERT-SELECT-1" coordinate="[13,21,0],[13,31,0]"/>
        <source id="29" column="LastName" parent_id="2" parent_name="Person.Person" coordinate="[3,21,0],[3,31,0]"/>
    </relation>
    <relation id="10" type="fdd" effectType="insert">
        <target id="12" column="FirstName" parent_id="10" parent_name="dbo.hiredate_view" coordinate="[1,31,0],[1,40,0]"/>
        <source id="26" column="FirstName" parent_id="25" parent_name="INSERT-SELECT-1" coordinate="[13,8,0],[13,19,0]"/>
    </relation>
    <relation id="11" type="fdd" effectType="insert">
        <target id="13" column="LastName" parent_id="10" parent_name="dbo.hiredate_view" coordinate="[1,41,0],[1,49,0]"/>
        <source id="27" column="LastName" parent_id="25" parent_name="INSERT-SELECT-1" coordinate="[13,21,0],[13,31,0]"/>
    </relation>
    <relation id="7" type="fdr" effectType="update">
        <target id="15" column="PseudoRows" parent_id="16" parent_name="UPDATE-SET-1" coordinate="[7,1,0],[10,16,0]" source="system"/>
        <source id="19" column="id" parent_id="10" parent_name="dbo.hiredate_view" coordinate="[10,4,0],[10,8,0]" clauseType="joinCondition"/>
        <source id="20" column="id" parent_id="2" parent_name="Person.Person" coordinate="[10,11,0],[10,15,0]" clauseType="joinCondition"/>
    </relation>
</dlineage>
```

#### diagram

![image.png](https://images.gitee.com/uploads/images/2021/0709/180222_79498e1d_8136809.png)

#### exported lineage

```xml
source_db;source_schema;source_table;source_column;target_db;target_schema;target_table;target_column;procedure_names;query_hash_id
default;Person;Person;FirstName;default;default;hashId_of_update-set-1;FirstName;batchQueries;hashId_of_query
default;default;hashId_of_update-set-1;FirstName;default;dbo;hiredate_view;FirstName;batchQueries;hashId_of_query

```

The column name in the exported lineage **shoudn't be qualified** , it must be like this `FirstName `.  But when it is written to the data catalog such as Atlas, it must be qualified like this:    `default.dbo.hiredate_view.FirstName.`

The `hashId_of_update-set-1` is the pseduo name of the update-set resultset, it is MD5 value of string `type+column name in resultset`.

The `hashId_of_query` is the MD5 value of the SQL query text from which this lineage is generated.

Both of those hashId are used in order to make sure the resultset name or query from the same SQL statement is the same every time the SQL statement is executed.
