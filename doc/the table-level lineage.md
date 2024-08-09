How to get table-level model from the complete lineage model

The table-level lineage model is built on the data of the complete data lineage model.

1. The table id and process id in the table-level model is the same as the one in complete lineage model.
2. The new table-level model uses table and process element from the complete lineage model and generate the new relation between the table and process.
3. Iterate target and source table in the complete lineage model, ignore all intermediate dataset such as resutlset, variable, and build relation between tables.
4. Iterate table-level realtion built in step 3 and according to the processId property in the table element, create the new relation by inserting the process between 2 tables.

```sql
create view v1 as select f1 from t2;
alter table t2 rename to t3;
```

### The complete data lineage

![image.png](https://images.gitee.com/uploads/images/2021/0707/122910_64fb520d_8136809.png)

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<dlineage>
    <process id="9" name="Query Create View" type="Create View" coordinate="[1,1,0],[1,37,0]"/>
    <process id="13" name="Query Alter Table" type="Alter Table" coordinate="[2,1,0],[2,29,0]"/>
    <table id="2" name="t2" type="table" coordinate="[1,34,0],[1,36,0]">
        <column id="3" name="f1" coordinate="[1,26,0],[1,28,0]"/>
        <column id="1" name="PseudoRows" coordinate="[1,34,0],[1,36,0]" source="system"/>
    </table>
    <table id="12" name="t3" type="table" processIds="13" coordinate="[2,26,0],[2,28,0]">
        <column id="11" name="PseudoRows" coordinate="[2,26,0],[2,28,0]" source="system"/>
    </table>
    <view id="8" name="v1" type="view" processIds="9" coordinate="[1,13,0],[1,15,0]">
        <column id="10" name="f1" coordinate="[1,26,0],[1,28,0]"/>
    </view>
    <resultset id="5" name="RS-1" type="select_list" coordinate="[1,26,0],[1,28,0]">
        <column id="6" name="f1" coordinate="[1,26,0],[1,28,0]"/>
    </resultset>
    <relation id="1" type="fdd" effectType="select">
        <target id="6" column="f1" parent_id="5" parent_name="RS-1" coordinate="[1,26,0],[1,28,0]"/>
        <source id="3" column="f1" parent_id="2" parent_name="t2" coordinate="[1,26,0],[1,28,0]"/>
    </relation>
    <relation id="2" type="fdd" effectType="create_view">
        <target id="10" column="f1" parent_id="8" parent_name="v1" coordinate="[1,26,0],[1,28,0]"/>
        <source id="6" column="f1" parent_id="5" parent_name="RS-1" coordinate="[1,26,0],[1,28,0]"/>
    </relation>
    <relation id="3" type="fdd" effectType="rename_table">
        <target id="11" column="PseudoRows" parent_id="12" parent_name="t3" coordinate="[2,26,0],[2,28,0]" source="system"/>
        <source id="1" column="PseudoRows" parent_id="2" parent_name="t2" coordinate="[1,34,0],[1,36,0]" source="system"/>
    </relation>
</dlineage>
```

### The table-level lineage

![image.png](https://images.gitee.com/uploads/images/2021/0707/122930_c6d8cb2a_8136809.png)

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

## The export format of the table-level model

## SQLFlow UI

![image.png](https://images.gitee.com/uploads/images/2021/0707/145217_cf9a983c_8136809.png)
