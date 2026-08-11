The foreign key in create table statement will create a column-level lineage.

```sql
CREATE TABLE masteTable
(
	masterColumn         varchar(3)  Primary Key,
);


CREATE TABLE foreignTable
(
	foreignColumn1            varchar(3)  NOT NULL ,
	foreignColumn2            varchar(3)  NOT NULL 
	FOREIGN KEY (foreignColumn1) REFERENCES masteTable(masterColumn),
	FOREIGN KEY (foreignColumn2) REFERENCES masteTable(masterColumn)
)
```

The data flow is:

```
masteTable.masterColumn -> fdd -> foreignTable.foreignColumn1
masteTable.masterColumn -> fdd -> foreignTable.foreignColumn2
```

### dataflow in xml

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<dlineage>
    <table id="2" name="masteTable" type="table" coordinate="[1,14,0],[1,24,0]">
        <column id="3" name="masterColumn" coordinate="[3,2,0],[3,14,0]"/>
    </table>
    <table id="5" name="foreignTable" type="table" coordinate="[7,14,0],[7,26,0]">
        <column id="10" name="foreignColumn1" coordinate="[9,2,0],[9,16,0]"/>
        <column id="11" name="foreignColumn2" coordinate="[10,2,0],[10,16,0]"/>
    </table>
    <relation id="1" type="fdd">
        <target id="10" column="foreignColumn1" parent_id="5" parent_name="foreignTable" coordinate="[9,2,0],[9,16,0]"/>
        <source id="3" column="masterColumn" parent_id="2" parent_name="masteTable" coordinate="[3,2,0],[3,14,0]"/>
    </relation>
    <relation id="2" type="fdd">
        <target id="11" column="foreignColumn2" parent_id="5" parent_name="foreignTable" coordinate="[10,2,0],[10,16,0]"/>
        <source id="3" column="masterColumn" parent_id="2" parent_name="masteTable" coordinate="[3,2,0],[3,14,0]"/>
    </relation>
</dlineage>
```

### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> The two legacy `fdd` edges are compatibility encodings, not value movement. SLPC emits
> `ObjectRelationship(PRIMARY_KEY)` for `masteTable.masterColumn` and two
> `ObjectRelationship(FOREIGN_KEY_REFERENCE)` records whose ordered key pairs bind `foreignColumn1` and
> `foreignColumn2` to `masterColumn`. The DDL occurrence is the evidence. A real query join would separately
> produce ROW JOIN facts and `JoinSemantics`; the FK declaration alone never creates a VALUE fact.

### diagram

![image.png](https://images.gitee.com/uploads/images/2021/0705/150530_b497fb6c_8136809.png)
