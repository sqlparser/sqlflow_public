## Indirect dataflow and RelationRows (pseudo column)

This article introduces some SQL elements that generate indirect dataflow. Indirect dataflow usually is generated from columns used in the where clause, group by clause, aggregate function and etc.

In order to create indirect dataflow between columns, we introduce a pseudo column: **RelationRows**.

RelationRows is a pseudo column of a relation used to represents the number of rows in a relation. As it's name indicates, RelationRows is not a real column in the relation(table/resultset and etc). Usually, It is used to represent a dataflow between a column and a relation.

RelationRows pseudo column can be used in both the source and target relation.

## 1 RelationsRows in target relation

Take this SQL for example:

```sql
SELECT a.empName "eName"
FROM scott.emp a
Where sal > 1000
```

The total number of rows of the select list is impacted by the value of column `sal` in the where clause. So, an indirect dataflow is created like this:

```
scott.emp.sal -> indirect -> RS-1.RelationRows
```

![image.png](https://images.gitee.com/uploads/images/2021/1206/120228_c087c542_8136809.png)

## 2 RelationRows in source relation

Here is another sample:

```sql
SELECT count() totalNum, sum(sal) totalSal 
FROM   scott.emp 
```

The value of `count()` function and `sum(sal)` function is impacted by the number of rows in the `scott.emp` source table.

```
scott.emp.RelationRows -> indirect -> count()
scott.emp.RelationRows -> indirect -> sum(sal)
```

![image.png](https://images.gitee.com/uploads/images/2021/1206/120353_cfebf6b1_8136809.png)

## 3. Table level dataflow using RelationRows

RelationRows is also used to represent table level dataflow.

```sql
alter table t2 rename to t3;
```

A table level dataflow is not built on a table, but on the pseudo column `RelationRows` like this:

```sql
t2.RelationRows -> direct -> t3.RelationRows
```

![image.png](https://images.gitee.com/uploads/images/2021/1206/120446_f7e66732_8136809.png)

Build a table to table dataflow that using the RelationRows pseudo column for 2 reasons:

* This pseudo column that used to represent a table to column dataflow can be re-used in a table to table dataflow later when SQLFlow generates a table-level relationship.
* If other columns in the same table are used in a column to column dataflow while this table itself is also in a table to table dataflow, then, this pseudo column will make it possible for a single table to includes  both the column to column dataflow and table to table dataflow.

take this SQL for example

```sql
create view v1 as select f1 from t2;
alter table t2 rename to t3;
```

The first create view statement will generate a column-level dataflow between the table `t2` and view `v1`,

```sql
t2.f1 -> direct -> RS-1.f1 -> direct -> v1.f1
```

while the second alter table statement will genereate a table-level dataflow between the table t2 and t3.

```sql
t2.RelationRows -> direct -> t3.RelationRows
```

![image.png](https://images.gitee.com/uploads/images/2021/1206/140840_6f229397_8136809.png)

As you can see, Table `t2` involved in the column to column dataflow generated by the `create view` statement, It also involved in a table to table dataflow generated by the `alter table` statement. A single table `t2` in the above digram shows that it includes both the column to column dataflow and a table to table dataflow.

## 4. References

1. xml code used in this article is generated by [DataFlowAnalyzer](https://github.com/sqlparser/gsp_demo_java/tree/master/src/main/java/demos/dlineage) tools
2. digram used in this article is generated by the [Gudu SQLFlow Cloud version](https://sqlflow.gudusoft.com/)