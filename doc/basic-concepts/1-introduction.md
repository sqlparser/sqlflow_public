## Introduction

SQLFlow generates data lineage by analyzing SQL queries and stored procedures.

The entity in the data lineage model includes table, column, function, relation and other entities . The combination of the entity and dataflow shows the lineage from one table/column to another.

![image.png](https://images.gitee.com/uploads/images/2021/0706/171437_139f041e_8136809.png)

[toc]

## 1. A dataflow unit

A dataflow unit includes a source entity, a target entity and a dataflow type between them.

```sql
SELECT p.FirstName
from Person.Person AS p 
```

This is the dataflow generated for the above SQL query.

```
person.persion.FirstName -> direct -> RS-1.FirstName
```

![image.png](https://images.gitee.com/uploads/images/2021/1204/185152_c18593ce_8136809.png)

### 1.1 Source, target entity

Source and target entity usually referes to table, view and other relations such as Common Table Expression (CTE), result set generated during the execution of the query. It may also refers to a file in the HDFS system and etc.

### 1.2 Relationship types

There are several relationship types in SQLFlow, the dataflow type is the most important realtionship type which is used to represents the dataflow between 2 objects, and there are two dataflow types: direct and indirect.

SQLFlow also supports other relationship types, such as join, function call and so on.

#### 1.2.1 Direct dataflow

The direct dataflow means the data of the target entity comes directly from the source entity.

In the above diagram, the data of `RS-1.FirstName` comes from the `Person.FirstName` directly.

An arrow is used to represent a direct dataflow in the diagram:

![image.png](https://images.gitee.com/uploads/images/2021/1204/202053_bfe8900f_8136809.png)

#### 1.2.2 Indirect dataflow

The indirect dataflow means the data of the target column is not comes from the source column, but the data of the source column/table impact the result data of the target column.

A dotted line arrow is used to represent an indirect dataflow in the diagram:

![image.png](https://images.gitee.com/uploads/images/2021/1204/202348_3a9d1e71_8136809.png)

The source column in the indirect dataflow usually appears in the following clause:

- Where clause
- Group by clause
- Winddows function
- Join condition

```sql
SELECT deptno, COUNT() num_emp, SUM(SAL) sal_sum
FROM scott.emp
GROUP BY deptno
```

The value of COUNT() and SUM(SAL) is impacted by the value of column `deptno` in the group by clause. So the indirect dataflows will be created like this:

```
scott.emp.deptno -> indirect -> COUNT()
scott.emp.deptno -> indirect -> SUM(SAL)
```

![image.png](https://images.gitee.com/uploads/images/2021/1206/174012_ba0c83f4_8136809.png)

For other indirect dataflow types, we will discuss later.

#### 1.2.3 Join

The `join` relationship build a link between 2 or more columns in the join condition. Striclty speaking, the relation is not a dataflow type.

```sql
 select b.teur
 from tbl a left join TT b on (a.key=b.key)
```

A join relationship will be created after analzying the above SQL. It indicates a join relationship betwee `tbl.key` and `TT.key`.

![image.png](https://images.gitee.com/uploads/images/2021/0711/185405_036c2a1a_8136809.png)

#### 1.2.4 function call

## 2. The entity in dataflow

When build dataflow between 2 entities: the source and target entity. They can be column to column, or, table to colum, or table to table.

### 2.1 column to column

This is the most often cases. Both entites in a dataflow are columns.

### 2.2 table to column

When we say a table impact the value of a column, we usually means the total number of rows of a table impact the value of a column, usually, this column is derived from a COUNT() function.

```sql
SELECT COUNT() num_emp
FROM scott.emp
```

A table to column dataflow is represented by using a RelationRows pseduo column. This build an indirect dataflow from scott.emp.RelationRows to RS-1.num_emp

```sql
scott.emp.RelationRows -> indirect -> COUNT() -> RS-1.num_emp
```

![image.png](https://images.gitee.com/uploads/images/2021/1206/174427_2f800ff4_8136809.png)

### 2.3 table to table

Sometimes, there will be a dataflow between 2 tables. For example, in an `alter table rename` SQL statement, a table to table dataflow will be created. Acutally, a table to table dataflow is represented by a column to column dataflow using the `RelationRows` pseudo column.

```sql
alter table t2 rename to t3;
```

![image.png](https://images.gitee.com/uploads/images/2021/1204/231703_d06e3c39_8136809.png)

## 3. Data lineage

A data lineage consists of lots of basic dataflow units.

```sql
CREATE VIEW vsal 
AS 
  SELECT a.deptno                  "Department", 
         a.num_emp / b.total_count "Employees", 
         a.sal_sum / b.total_sal   "Salary" 
  FROM   (SELECT deptno, 
                 Count()  num_emp, 
                 SUM(sal) sal_sum 
          FROM   scott.emp 
          WHERE  city = 'NYC' 
          GROUP  BY deptno) a, 
         (SELECT Count()  total_count, 
                 SUM(sal) total_sal 
          FROM   scott.emp 
          WHERE  city = 'NYC') b 
```

The data lineage diagram:

![image.png](https://images.gitee.com/uploads/images/2021/0711/221337_e8f731a5_8136809.png)

The output also available in XML or JSON format .

## 4. References

1. xml code used in this article is generated by [DataFlowAnalyzer](https://github.com/sqlparser/gsp_demo_java/tree/master/src/main/java/demos/dlineage) tools
2. digram used in this article is generated by the [Gudu SQLFlow Cloud version](https://sqlflow.gudusoft.com/)