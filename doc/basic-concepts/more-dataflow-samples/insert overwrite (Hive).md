```sql
INSERT OVERWRITE LOCAL DIRECTORY '/tmp/pv_gender_sum'
SELECT pv_gender_sum.*
FROM pv_gender_sum;
```

### column-level lineage

The data flow is:

```
pv_gender_sum(*) ->  fdd ->  path ( uri='/tmp/pv_gender_sum')
```

#### dataflow in xml

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<dlineage>
    <path id="2" name="'/tmp/pv_gender_sum'" uri="'/tmp/pv_gender_sum'" type="path" processIds="3" coordinate="[1,34,0],[1,54,0]">
        <column id="4" name="uri='/tmp/pv_gender_sum'" coordinate="[-1,-1,0],[-1,-1,0]"/>
    </path>
    <process id="3" name="Query Insert" type="Insert" coordinate="[1,1,0],[3,20,0]"/>
    <table id="6" name="pv_gender_sum" type="table" coordinate="[3,6,0],[3,19,0]">
        <column id="7" name="*" coordinate="[2,8,0],[2,23,0]"/>
    </table>
    <resultset id="9" name="INSERT-SELECT-1" type="insert-select" coordinate="[2,8,0],[2,23,0]">
        <column id="10" name="*" coordinate="[2,8,0],[2,23,0]"/>
    </resultset>
    <relation id="1" type="fdd" effectType="select">
        <target id="10" column="*" parent_id="9" parent_name="INSERT-SELECT-1" coordinate="[2,8,0],[2,23,0]"/>
        <source id="7" column="*" parent_id="6" parent_name="pv_gender_sum" coordinate="[2,8,0],[2,23,0]"/>
    </relation>
    <relation id="2" type="fdd" effectType="insert">
        <target id="4" column="uri='/tmp/pv_gender_sum'" parent_id="2" parent_name="'/tmp/pv_gender_sum'" coordinate="[-1,-1,0],[-1,-1,0]"/>
        <source id="10" column="*" parent_id="9" parent_name="INSERT-SELECT-1" coordinate="[2,8,0],[2,23,0]"/>
    </relation>
</dlineage>
```

#### diagram

![image.png](https://images.gitee.com/uploads/images/2021/0705/150952_71d31fcd_8136809.png)

### table-level lineage

```
pv_gender_sum ->  query process (insert overwrite) ->  path ( uri='/tmp/pv_gender_sum')
```


 ![image.png](https://images.gitee.com/uploads/images/2021/0709/140623_6cb3727f_8136809.png)
