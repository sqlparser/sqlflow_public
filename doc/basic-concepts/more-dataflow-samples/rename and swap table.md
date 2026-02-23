```sql
create view v1 as select f1 from t2;
alter table t2 rename to t3;
```

### column-level lineage mode

In order to put a table involved in both column-level lineage and table-level lineage into one picture,we use `PseudoRows` column in order to represent this relation.

```
t2.PseudoRows -> fdd -> t3.PseudoRows
```

#### diagram

This is the diagram show lineage in column-level mode.

![image.png](https://images.gitee.com/uploads/images/2021/0704/180540_c910755a_8136809.png)

### table-level lineage mode

If we want to show the table in above SQL in a table-level lineage mode, the relation between 2 tables should be represented by another form like this:

```
t2 -> query process (create view) -> v1
t2 -> query process (alter table rename) -> t3
```

#### diagram

This is the diagram show lineage in table-level mode.

![image.png](https://images.gitee.com/uploads/images/2021/0707/145605_6c4f4b22_8136809.png)

#### dataflow in xml

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<dlineage>
    <process id="9" name="Query Create View" type="Create View" coordinate="[1,1,0],[1,37,0]"/>
    <process id="13" name="Query Alter Table" type="Alter Table" coordinate="[2,1,0],[2,29,0]"/>
    <table id="2" name="t2" type="table" coordinate="[1,34,0],[1,36,0]"/>
    <table id="12" name="t3" type="table" processIds="13" coordinate="[2,26,0],[2,28,0]"/>
    <view id="8" name="v1" type="view" processIds="9" coordinate="[1,13,0],[1,15,0]"/>
    <relation id="307" type="fdd">
        <target id="308" target_id="9" target_name="Query Create View"/>
        <source id="302" source_id="2" source_name="t2"/>
    </relation>
    <relation id="309" type="fdd">
        <target id="301" target_id="8" target_name="v1"/>
        <source id="310" source_id="9" source_name="Query Create View"/>
    </relation>
    <relation id="311" type="fdd">
        <target id="312" target_id="13" target_name="Query Alter Table"/>
        <source id="305" source_id="2" source_name="t2"/>
    </relation>
    <relation id="313" type="fdd">
        <target id="304" target_id="12" target_name="t3"/>
        <source id="314" source_id="13" source_name="Query Alter Table"/>
    </relation>
</dlineage>


```
