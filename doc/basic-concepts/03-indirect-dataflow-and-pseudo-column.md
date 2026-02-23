 [toc]
## Indirect dataflow

Indirect dataflow captures how certain columns influence the result without directly supplying values to the output columns. This typically happens in `WHERE`, `GROUP BY`, join conditions, and aggregate functions.


## WHERE Clause

Filtering predicates affect which rows appear in the output. In v1 this was modeled via a pseudo-column; in v2 it is modeled explicitly as `restricts`.

Take this SQL for example:

```sql
SELECT a.empName "eName"
FROM scott.emp a
WHERE sal > 1000
```

The total number of rows in the SELECT result is impacted by the value of column `sal` in the `WHERE` clause.

- v1 (using RelationRows):
```
scott.emp.sal -> indirect -> RS-1.RelationRows
```
  - relation type = `fdr` (indirect), effectType: select

- v2 (explicit filter influence):
```
restricts: scott.emp.sal -> RS-1."eName"
```
  - relationship type = `restricts` (no copy category); this shows `sal` filters the rows of the resultset

![image.png](https://images.gitee.com/uploads/images/2021/1206/120228_c087c542_8136809.png)

## GROUP BY Clause

Aggregations and grouping change values and granularity. V1 modeled these via `RelationRows` and indirect edges; v2 models them via `data_flow` with `effectType: AGGREGATION` plus `groups` for grouping keys.

### Group BY example (with v1 and v2 relationships):

```sql
SELECT deptno, COUNT(*) AS totalNum, SUM(sal) AS totalSal
FROM scott.emp
GROUP BY deptno;
```

- v1 relationships (using RelationRows and fdr/fdd):
```
scott.emp.deptno       -> indirect -> COUNT(*)    (effectType: select)
scott.emp.deptno       -> indirect -> SUM(sal)    (effectType: select)
scott.emp.sal          -> direct   -> SUM(sal)    (effectType: select)
```

- v2 relationships (atomic and explicit):
```
// Grouping influence
groups:    scott.emp.deptno  -> RS-1.totalSal
groups:    scott.emp.deptno  -> RS-1.totalNum


// Aggregation edges
data_flow: scott.emp.sal     -> RS-1.totalSal
  - transforms.code: "SUM(sal)"
  - effectType: AGGREGATION


// COUNT(*) depends on table rows, grouped by deptno
data_flow: scott.emp (table) -> RS-1.totalNum
  - transforms.code: "COUNT(*)"
  - effectType: AGGREGATION

```


### Aggregates Without GROUP BY: Table-Level Aggregation

When using aggregate functions like `COUNT(*)` or `SUM()` without a `GROUP BY` clause, the aggregation happens at the table level, producing a single row result. This is different from grouped aggregation because it collapses all rows into one summary value.

```sql
SELECT COUNT(*) AS totalNum, SUM(sal) AS totalSal
FROM scott.emp
```

The values of `COUNT(*)` and `SUM(sal)` are impacted by the number of rows in table `scott.emp`.

- v1 (indirect edges):
```
scott.emp.RelationRows -> indirect -> COUNT(*)
scott.emp.RelationRows -> indirect -> SUM(sal)
```
  - relation type = `fdr` (indirect), effectType: select

![image.png](https://images.gitee.com/uploads/images/2021/1206/120353_cfebf6b1_8136809.png)

- v2 (more precise breakdown):
  - `data_flow` from `emp.sal` to `totalSal`
    - transforms.code: `SUM(sal)`
    - effectType: `AGGREGATION` (aggregation changes granularity)
  - `data_flow` from `emp` to `totalNum`
    - transforms.code: `COUNT(*)`
    - effectType: `AGGREGATION`


## RelationRows (pseudo column)

To represent row-count influences and table-level movement in v1, SQLFlow uses a pseudo column named **RelationRows**.

- **RelationRows** represents the number of rows in a relation (table, view, resultset). As its name indicates, it is not a real column in the physical table.
- It connects a column’s influence to the row count of a relation, or expresses table-to-table lineage in a column-centric model.
- In v2, `RelationRows` is deprecated in favor of more precise relationship types:
  - `restricts` for filtering relationships (e.g., WHERE clauses)
  - `groups` for grouping relationships (e.g., GROUP BY)
  - `data_flow` with `effectType: AGGREGATION` for aggregation relationships
  These provide clearer semantics about how each column influences the result.

### Table-level dataflow using RelationRows

`RelationRows` is also used to represent table-level data movement, such as a rename:

```sql
ALTER TABLE t2 RENAME TO t3;
```

We represent it with pseudo columns to keep table-level lineage compatible with column-level models:

```sql
t2.RelationRows -> direct -> t3.RelationRows
```

- v1: relation type = `fdd` (direct), effectType: rename_table (or vendor-specific)
- v2: direct table-level `data_flow`; effectType: `EXACT_COPY` (row set preserved, name changed)

![image.png](https://images.gitee.com/uploads/images/2021/1206/120446_f7e66732_8136809.png)

Why use `RelationRows` for table-level edges in v1?
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
