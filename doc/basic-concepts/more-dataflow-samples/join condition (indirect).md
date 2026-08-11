### frd relation

```sql
 select b.teur
 from tbl a left join TT b on (a.key=b.key)
```

Columns in the join condition also effect the number of row in the resultset of the select list just like column in the where clause do.

So, the following relation will be discoverd in the above SQL.

```
tbl.key -> fdr -> resultset.PseudoRows
TT.key -> fdr -> resultset.PseudoRows
```

#### diagram

![image.png](https://images.gitee.com/uploads/images/2021/0704/145001_bf601741_8136809.png)

### join relation

A join relation will be created after analzye the above SQL. It indicates a join relation betwee `tbl.key` and `TT.key`.

#### diagram

![image.png](https://images.gitee.com/uploads/images/2021/0711/185405_036c2a1a_8136809.png)

### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> `tbl.key` and `TT.key` each produce an atomic `ROW + JOIN` fact to the result relation; the selected
> `TT.teur` produces a separate `VALUE + DIRECT` fact. `JoinSemantics(joinType=LEFT, conditionForm=ON)`
> pairs the two keys with `EQUALS`, marks `tbl` as preserved and `TT` as null-extended, and points back to
> the row facts. This replaces both the pseudo-row encoding and the untyped legacy join overlay without
> losing either value or row meaning.
