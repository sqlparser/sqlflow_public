## Dataflow between column used as aggregate function argument and the aggregate function

Aggregate function usually takes column as an argument, in this article, we will discuss what's kind of dataflow will be created between the column used as function argument and the aggregate function.

## 1. COUNT()

COUNT() may takes a star column, or any column name or even empty argument.

If the argument is empty or a star column, no dataflow will be generated between the argument and function. 
If a column is used as the argument, a direct dataflow will be generated between the column and function 
by setting `/treatArgumentsInCountFunctionAsDirectDataflow` option to `true`.

### 1.1 A direct dataflow

```sql
SELECT count(empId) total_num FROM scott.emp
```

In [SQLFlow Cloud](https://sqlflow.gudusoft.com), a direct dataflow will be generated between the empId column and COUNT() function by default.

However, in [Dlineage command line tool](https://github.com/sqlparser/gsp_demo_java/releases), a direct dataflow will not be generated between the empId column and COUNT() function by default.

To enable the direct dataflow in Dlineage command line tool, you can use the `/treatArgumentsInCountFunctionAsDirectDataflow` option.

```
scott.emp.empId -> direct -> COUNT()
```

This dataflow may seems strange since the result value of COUNT() doesn't depends on the value of empId column. But, this is an option if our users prefer to have such a dataflow.

![image.png](https://images.gitee.com/uploads/images/2021/1206/225504_c49c3750_8136809.png)

### 1.2 No dataflow

You can use an option to decide not to generate a dataflow between empId and COUNT() if preferred.

Please note that, no matter  a direct dataflow is generated between the empId and COUNT() or not. The following indirect dataflow will always be created.

```
scott.emp.RelationRows -> indirect -> COUNT()
```

## 2. Aggregate function exclude COUNT()

COUNT() function is a little bit difference when creating dataflow. All other aggregate functions such as SUM() will create a direct dataflow with the column used as the argument.

```sql
SELECT deptno, SUM(SAL) sal_sum
FROM scott.emp
group by deptno
```

A direct dataflow will be created from SAL to SUM().

```sql
scott.emp.SAL -> direct -> SUM()
```

![image.png](https://images.gitee.com/uploads/images/2021/1206/160142_54580f3a_8136809.png)