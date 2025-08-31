[toc]
## Indirect dataflow and RelationRows (pseudo column)

Indirect dataflow captures how certain columns influence the result without directly supplying values to the output columns. This typically happens in `WHERE`, `GROUP BY`, join conditions, and aggregate functions.

To represent these influences precisely, SQLFlow uses a pseudo column named **RelationRows**.

- **RelationRows** represents the number of rows in a relation (table, view, resultset). As its name indicates, it is not a real column in the physical table.
- We use it to connect a column’s influence to the row count of a relation, or to express table-to-table lineage.

Effect type notes:
- v1: `effectType` denotes the statement/operation kind (e.g., `select`, `insert`, `create_view`).
- v2: `effectType` denotes copy/transform strength for `data_flow` edges (e.g., `EXACT_COPY`, `WEAK_COPY`, `AGGREGATION`, `AMBIGUOUS`). For `restricts` and `groups` (non-copy edges), no copy category is applied.

## 1. RelationRows in the target relation (WHERE filters)

Take this SQL for example:

```sql
SELECT a.empName "eName"
FROM scott.emp a
WHERE sal > 1000
```

The total number of rows in the SELECT result is impacted by the value of column `sal` in the `WHERE` clause. We model this as an indirect influence on the resultset’s row count via `RelationRows`:

```
scott.emp.sal -> indirect -> RS-1.RelationRows
```

- v1: relation type = `fdr` (indirect), effectType: select
- v2: relationship type = `restricts` (no copy category); this shows `sal` filters the rows of the resultset

![image.png](https://images.gitee.com/uploads/images/2021/1206/120228_c087c542_8136809.png)

## 2. RelationRows in the source relation (aggregates)

Another common case is aggregates:

```sql
SELECT COUNT(*) AS totalNum, SUM(sal) AS totalSal
FROM scott.emp
```

The values of `COUNT(*)` and `SUM(sal)` are impacted by the number of rows in table `scott.emp`.

v1 (indirect edges):
```
scott.emp.RelationRows -> indirect -> COUNT(*)
scott.emp.RelationRows -> indirect -> SUM(sal)
```
- v1: relation type = `fdr` (indirect), effectType: select

v2 (more precise breakdown):
- `data_flow` from `emp.sal` to `totalSal`
  - transforms.code: `SUM(sal)`
  - effectType: `AGGREGATION` (aggregation changes granularity)
- `groups` or `restricts` is not used in this no-GROUP-BY example; the influence comes from the table’s row count and the aggregated input column

If a `GROUP BY` exists, v2 adds a `groups` edge from the group-by columns to the aggregate output, and keeps the `data_flow` + `AGGREGATION` from the aggregated column(s) to the output.

![image.png](https://images.gitee.com/uploads/images/2021/1206/120353_cfebf6b1_8136809.png)

## 3. Table-level dataflow using RelationRows

`RelationRows` is also used to represent table-level data movement, such as a rename:

```sql
ALTER TABLE t2 RENAME TO t3;
```

We represent it with pseudo columns to keep table-level lineage compatible with column-level models:

```sql
t2.RelationRows -> direct -> t3.RelationRows
```

- v1: relation type = `fdd` (direct), effectType: rename_table (or vendor-specific)
- v2: relationship type = `data_flow` at table level via `RelationRows`; effectType: `EXACT_COPY` (row set preserved, name changed)

![image.png](https://images.gitee.com/uploads/images/2021/1206/120446_f7e66732_8136809.png)

Why use `RelationRows` for table-level edges?
- It unifies modeling so a single table can participate in both column-level (via real columns) and table-level (via `RelationRows`) relationships without conflicts.
- It allows later derivation of table-level lineage by folding column-level edges.

Take this SQL for example:

```sql
CREATE VIEW v1 AS SELECT f1 FROM t2;
ALTER TABLE t2 RENAME TO t3;
```

- The `CREATE VIEW` statement generates a column-level lineage between `t2` and `v1`:

```sql
t2.f1 -> direct -> RS-1.f1 -> direct -> v1.f1
```

- The `ALTER TABLE` statement generates a table-level edge via `RelationRows`:

```sql
t2.RelationRows -> direct -> t3.RelationRows
```

As you can see, table `t2` is involved in both a column-to-column lineage (from the view creation) and a table-to-table lineage (from the rename). Using `RelationRows` enables both to coexist cleanly.

![image.png](https://images.gitee.com/uploads/images/2021/1206/140840_6f229397_8136809.png)

## A Look Ahead: Indirect Data Flow in the v2 Model

To make indirect effects more explicit and traceable, the v2 model (under development) represents them with dedicated relationship types and clearer evidence:

- **fdr → restricts/groups**: Indirect effects are split into:
  - `restricts`: filters (e.g., `WHERE`, `JOIN ON`, `HAVING` conditions)
  - `groups`: grouping effects (`GROUP BY` columns affecting aggregates)
- **Aggregates**: Use `data_flow` edges from input columns to aggregate outputs with `effectType: AGGREGATION` and `transforms.code` (e.g., `SUM(sal)`). Grouping columns connect via `groups`.
- **Traceability**: Each relationship can carry `observations` (file/line anchors) and `statementKey` (groups edges from the same statement), while objects use stable `qualifiedName`.
- **Effect types on non-copy edges**: `restricts`/`groups` are non-copy influences; they do not carry copy categories like `EXACT_COPY`.

This approach keeps the intuition of indirect impact while making the “how and where” of that impact far more transparent.

## References

1. XML code used in this article is generated by [DataFlowAnalyzer](https://github.com/sqlparser/gsp_demo_java/tree/master/src/main/java/demos/dlineage) tools.
2. Diagrams used in this article are generated by the [Gudu SQLFlow Cloud version](https://sqlflow.gudusoft.com/).

## Discussion: Should we use RelationRows? v1→v2 guidance with examples

Summary:
- RelationRows fills real gaps (row-count influence and table-level lineage) but, as a pseudo-column, can add confusion and graph noise.
- In v2, prefer first-class relationships: `restricts`, `groups`, and table-level `data_flow` with `effectType` and `transforms`.
- If needed, keep RelationRows as a hidden metric object for special cases.

### Pros of RelationRows (v1)
- Expresses row-count impact even when no output column exists (e.g., `WHERE`).
- Enables table→table lineage in a column-centric model (e.g., rename, clone).
- Lets one table participate in both table-level and column-level edges.

### Cons in complex environments
- Not a real column; can confuse users and tools.
- Increases node/edge count without direct code anchors.
- Overlaps with clearer v2 primitives (`restricts`, `groups`, table-level `data_flow`).

### Recommended v2 replacement patterns
- Filters/row-count impacts: use `restricts` edges from predicate columns to affected outputs; optionally a single `restricts` to a temporary resultset for coarse folding.
- Aggregates: use `data_flow` with `effectType=AGGREGATION` and `transforms.code`; add `groups` from grouping columns.
- Table→table lineage: use table-level `data_flow` (`operation=RENAME/CTAS/CLONE`, `effectType` set accordingly).

If you choose to retain RelationRows in v2, model it as a hidden metric (e.g., `properties.isPseudo=true`, `properties.metric='rows'`) and hide by default in UI.

---

### Example 1: WHERE filter (row-count impact)

```sql
SELECT a.empName AS "eName"
FROM scott.emp a
WHERE sal > 1000;
```

v1 relationships (using RelationRows):
```
scott.emp.sal -> fdr -> RS-1.RelationRows   (effectType: select)
```

v2 relationships (atomic edges, no pseudo-column):
```
restricts: scott.emp.sal -> RS-1."eName"
```
- effectType: (none for restricts)
- Notes: Optionally, also add `restricts: scott.emp.sal -> RS-1` (temporary resultset) for coarse UI.

---

### Example 2: Aggregates (COUNT/SUM) with GROUP BY

```sql
SELECT deptno, COUNT(*) AS totalNum, SUM(sal) AS totalSal
FROM scott.emp
GROUP BY deptno;
```

v1 relationships (typical):
```
scott.emp.RelationRows -> fdr -> COUNT(*)    (effectType: select)
scott.emp.RelationRows -> fdr -> SUM(sal)    (effectType: select)
scott.emp.deptno       -> fdr -> COUNT(*)    (effectType: select)
scott.emp.deptno       -> fdr -> SUM(sal)    (effectType: select)
scott.emp.sal          -> fdd -> SUM(sal)    (effectType: select)
```

v2 relationships (more precise):
```
// Aggregation edges
data_flow: scott.emp.sal -> RS-1.totalSal
  - transforms.code: "SUM(sal)"
  - effectType: AGGREGATION

// Grouping influence
groups:    scott.emp.deptno -> RS-1.totalSal

// COUNT(*) depends on table rows, grouped by deptno
data_flow: scott.emp (table) -> RS-1.totalNum
  - transforms.code: "COUNT(*)"
  - effectType: AGGREGATION
groups:    scott.emp.deptno -> RS-1.totalNum

// Pass-through of grouping key
data_flow: scott.emp.deptno -> RS-1.deptno
  - effectType: EXACT_COPY
```

---

### Example 3: Table rename (table→table lineage)

```sql
ALTER TABLE t2 RENAME TO t3;
```

v1 relationships (via RelationRows):
```
t2.RelationRows -> fdd -> t3.RelationRows   (effectType: rename_table)
```

v2 relationships (direct table-level edge):
```
data_flow: t2 -> t3
  - operation: RENAME
  - effectType: EXACT_COPY
```

---

### Decision
- Prefer v2 primitives (`restricts`, `groups`, table-level `data_flow`) for clarity, atomicity, and traceability (`observations`, `statementKey`).
- Ensure `effectType` and `transforms.code` are set consistently so beginners can immediately understand the strength and nature of each relationship.