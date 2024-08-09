```sql
create view vEmp(eName) as
SELECT a.empName "eName"
FROM scott.emp a
Where sal > 1000
```

### fdd

Data in the column `eName` of the view `vEmp` comes from column `empName` of the table `scott.emp` via the chain like this:

```
scott.emp.empName -> fdd -> RS-1."eName" -> vEmp.eName
```

#### diagram

![image.png](https://images.gitee.com/uploads/images/2021/0704/145716_35ee907e_8136809.png)

### fdr

From this query, you will see how the column `sal` in where clause impact the number of rows in the top level view `vEmp`.

```
scott.emp.sal -> fdr -> resultset1.PseudoRows -> fdr -> vEmp.PseudoRows
```

So, from an end to end point of view, there will be a `fdr` relation between column `sal` and view `vEmp` like this:

```
scott.emp.sal -> fdr -> vEmp.PseudoRows
```

#### diagram

![image.png](https://images.gitee.com/uploads/images/2021/0704/145810_66a232d3_8136809.png)
