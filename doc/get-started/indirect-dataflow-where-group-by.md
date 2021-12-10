## 1. Columns in where clause

Some of the columns in source tables in WHERE clause do not influence target columns but are crucial for the selected row set, so they should be saved for impact analyses, with an indirect dataflow to the target tables.

Take this SQL for example:

```sql
SELECT a.empName "eName"
FROM scott.emp a
Where sal > 1000
```

The total number of rows of the select list is impacted by the value of column `sal` in the where clause. We build an indirect dataflow for this relationship.

```
scott.emp.sal -> indirect -> RS-1.RelationRows
```

![image.png](https://images.gitee.com/uploads/images/2021/1206/120228_c087c542_8136809.png)

## 2. COUNT()

COUNT() function is an aggregate function that used to calculate the total number of rows of a relation.

### 2.1 where clause without group by clause

```sql
SELECT COUNT() num_emp
FROM scott.emp
where city=1
```

In above SQL, two indirect dataflows will be created, because the value of COUNT() is impacted by the city column in where clause and the total number of rows of scott.emp table.

```sql
scott.emp.city -> indirect -> COUNT()
scott.emp.RelationRow -> indirect -> COUNT()
```

![image.png](https://images.gitee.com/uploads/images/2021/1206/150203_a4bbf172_8136809.png)

### 2.2 where clause with group by clause

```sql
SELECT deptno, count() total_num
FROM scott.emp
where city=1
group by deptno
```

As you can see, besides the two indirect dataflows created in the previous SQL, a third indirect dataflow is created using the deptno in the group by clause.

```sql
scott.emp.city -> indirect -> COUNT()
scott.emp.Relations -> indirect -> COUNT()
scott.emp.deptno -> indirect -> COUNT()
```

![image.png](https://images.gitee.com/uploads/images/2021/1206/150427_bad8e1d6_8136809.png)

## 3. Other aggregate function

When creating indirect dataflow, other aggregate functions such as SUM() works **a little difference** to the COUNT() function.

### 3.1 where clause with group by clause

```sql
SELECT deptno, SUM(SAL) sal_sum
FROM scott.emp
where city=1
group by deptno
```

aggregate function such as SUM() calculates the value from a  record set determined by the columns used in the group by clause, so deptno column in the group by clause is used to create an indirect dataflow to SUM() function.

an indirect dataflow is created from deptno to SUM().

```sql
scott.emp.deptno -> indirect -> SUM()
```

**RelationRows pseudo column will not be used to create an indirect dataflow if group by clause if presented.**

![image.png](https://images.gitee.com/uploads/images/2021/1210/170231_fd2cfc92_8136809.png)

### 3.2 where clause without group by clause

```sql
SELECT SUM(SAL) sal_sum
FROM scott.emp
where city=1
```

The above SQL means that the whole record set of the table will be used to calculate the value of SUM() function.

So, two indirect dataflows will be created as below:

```sql
scott.emp.city -> indirect -> SUM()
scott.emp.RelationRows -> indirect -> SUM()
```

![image.png](https://images.gitee.com/uploads/images/2021/1206/143844_5a1e3bad_8136809.png)

## 4. Summary

- Columns in where clause always create an indirect dataflow to all aggregate functions used in the select list.
- RelationRows pseudo column always create an indirect dataflow to COUNT() function, but only create an indirect dataflow to other aggregate functions such as SUM()  when the group by clause is not used.
- Columns in the group by clause always create an indirect dataflow to all aggregate functions used in the select list.