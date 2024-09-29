### case expression

```sql
 select
 	case when a.kamut=1 and b.teur IS null
 			 then 'no locks'
 		 when a.kamut=1
 			then b.teur
 	else 'locks'
 	end teur
 from tbl a left join TT b on (a.key=b.key)
```

During the analyzing of dataflow, case expression is treated as a function. The column used inside the case expression will be treated like the arguments of a function.
So for the above SQL, the following relation is discovered:

```
tbl.kamut -> direct -> teur
TT.teur -> direct -> teur
```

#### diagram

![image.png](https://images.gitee.com/uploads/images/2021/0704/140751_da11dcf1_8136809.png)
