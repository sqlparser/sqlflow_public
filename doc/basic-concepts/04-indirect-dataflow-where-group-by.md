## Indirect dataflow between columns in where clause and aggregate functions

Think of `WHERE` as a filter and `GROUP BY` as an organizer. They usually don’t copy values into the result, but they decide which rows are used and how rows are grouped before aggregate functions like `COUNT()` or `SUM()` run. That means they indirectly impact the output.

## Part 1: Current Data Lineage Model (v1)

### 1. Columns in where clause

Some columns in the source table in a WHERE clause do not influence the data of the target columns but are crucial for the selected row set numbers, so they should be saved for impact analyses, with an indirect dataflow to the target tables.

Take this SQL for example:

```sql
SELECT a.empName "eName"
FROM scott.emp a
WHERE sal > 1000
```

EffectType: select

The total number of rows in the select list is impacted by the value of column `sal` in the WHERE clause. We build an indirect dataflow for this relationship.

```
scott.emp.sal -> indirect -> RS-1.RelationRows
```

In v2 (right after the same SQL), the model becomes more explicit:

```
scott.emp -> data_flow (effectType: EXACT_COPY) -> RS-1.empName
scott.emp.sal -> restricts -> RS-1.empName
```

Explanation: `sal` filters which rows appear; it does not copy into the output. The `restricts` relationship captures this filtering effect. The name column flows directly unchanged.

If you want to filter the relation types to only include the direct dataflows, you can use the following option:

```
option.filterRelationTypes("fdd");
```

This will show only direct dataflows; indirect dataflows from the WHERE clause are excluded.



![image.png](https://images.gitee.com/uploads/images/2021/1206/120228_c087c542_8136809.png)

### 2. COUNT()

COUNT() function is an aggregate function that is used to calculate the total number of rows of a relation.

#### 2.1 where clause without group by clause

```sql
SELECT COUNT() total_num
FROM scott.emp
WHERE city=1
```

EffectType: select

In the above SQL, two indirect dataflows will be created, 
- The value of COUNT() is impacted by the city column in the WHERE clause 
```sql
scott.emp.city -> indirect -> COUNT()
```

- The value of COUNT() is also impacted by the total number of rows of the `scott.emp` table.
```sql
scott.emp.RelationRows -> indirect -> COUNT()
```

v2 view of the same:

```
scott.emp -> data_flow (transform: COUNT(), effectType: AGGREGATION) -> total_num
scott.emp.city -> restricts -> total_num
```

Explanation: COUNT aggregates rows (aggregation effect), while `city` filters the record set used by COUNT.

![image.png](https://images.gitee.com/uploads/images/2021/1206/150203_a4bbf172_8136809.png)

#### 2.2 where clause and group by clause

```sql
SELECT deptno, COUNT() total_num
FROM scott.emp
WHERE city=1
GROUP BY deptno
```

EffectType: select

As you can see, in addition to the two indirect dataflows created in the previous SQL, a third indirect dataflow is created from `deptno` in the GROUP BY clause.

```sql
scott.emp.city -> indirect -> COUNT()
scott.emp.RelationRows -> indirect -> COUNT()
scott.emp.deptno -> indirect -> COUNT()
```

v2 view of the same:

```
scott.emp -> data_flow (transform: COUNT(), effectType: AGGREGATION) -> total_num
scott.emp.city -> restricts -> total_num
scott.emp.deptno -> groups -> total_num
```

Explanation: `deptno` defines the grouping keys for COUNT, while `city` filters rows before grouping.

![image.png](https://images.gitee.com/uploads/images/2021/1206/150427_bad8e1d6_8136809.png)

### 3. Other aggregate functions

When creating indirect dataflow, other aggregate functions such as SUM() work **a little differently** from the COUNT() function.

#### 3.1 where clause and group by clause

```sql
SELECT deptno, SUM(SAL) sal_sum
FROM scott.emp
WHERE city=1
GROUP BY deptno
```

EffectType: select

An aggregate function such as SUM() calculates the value from a record set determined by the columns used in the GROUP BY clause, so the `deptno` column in the GROUP BY clause is used to create an indirect dataflow to the SUM() function.

An indirect dataflow is created from `deptno` to SUM().

```sql
scott.emp.deptno -> indirect -> SUM()
```

v2 view of the same:

```
scott.emp.SAL -> data_flow (transform: SUM(SAL), effectType: AGGREGATION) -> sal_sum
scott.emp.deptno -> groups -> sal_sum
scott.emp.city -> restricts -> sal_sum
```

Explanation: SUM is an aggregation over `SAL` per `deptno`; `city` restricts which rows are considered.

**RelationRows pseudo column will not be used to create an indirect dataflow if a GROUP BY clause is present. This is because the value of the SUM() function is calculated from a record set determined by the columns used in the GROUP BY clause, so the total number of rows of the record set is not needed for the calculation of the SUM() function.**

![image.png](https://images.gitee.com/uploads/images/2021/1210/170231_fd2cfc92_8136809.png)

#### 3.2 where clause without group by clause

```sql
SELECT SUM(SAL) sal_sum
FROM scott.emp
WHERE city=1
```

EffectType: select

The above SQL uses the whole table's record set to calculate the value of the SUM() function.

So, two indirect dataflows will be created as below:

```sql
scott.emp.city -> indirect -> SUM()
scott.emp.RelationRows -> indirect -> SUM()
```

v2 view of the same:

```
scott.emp.SAL -> data_flow (transform: SUM(SAL), effectType: AGGREGATION) -> sal_sum
scott.emp.city -> restricts -> sal_sum
```

Explanation: Without GROUP BY, SUM aggregates over the whole filtered table; there is no grouping key.

![image.png](https://images.gitee.com/uploads/images/2021/1206/143844_5a1e3bad_8136809.png)

### 4. Summary

- Columns in the WHERE clause always create a restricting influence on aggregates used in the select list.
- Prefer v2 modeling without `RelationRows`. For aggregates:
  - Use `data_flow` with `transforms` and `effectType: AGGREGATION` from real sources (argument columns for SUM/AVG/MIN/MAX; table or FROM result for COUNT(*)).
  - Add `restricts` from WHERE/HAVING columns and `groups` from GROUP BY columns.
- Columns in the GROUP BY clause always create a grouping influence on aggregates.

### References (v1)

- v1 Schema: [data_lineage_schema_v1.json](mdc:gsp_java/docs/AI/cline_sqlflow/data_lineage_schema_v1.json)
- v1 Design Explanation: [data_lineage_design_explanation_v1.md](mdc:gsp_java/docs/AI/cline_sqlflow/data_lineage_design_explanation_v1.md)

## Part 2: Next-Generation Data Lineage Model (v2)

To provide a more precise and auditable lineage, Schema v2 replaces the generic "indirect" concept with explicit relationship types and captures transformations and effect types directly.

### Key Improvements and Concept Mapping

| Current Concept (v1) | New Concept (v2 Preview) | Improvement |
| :--- | :--- | :--- |
| Indirect flow from WHERE (`fdr`) | `restricts` relationship | Clearly models filtering columns that affect result sets and aggregates. |
| Indirect flow from GROUP BY (`fdr`) | `groups` relationship | Explicitly captures grouping columns driving aggregate outputs. |
| Direct flow (`fdd`) | `data_flow` relationship | Same core idea with a clearer name; includes `transforms` for functions. |
| `RelationRows` pseudo column | Represented by transform context | Aggregates operate over a record set; pseudo columns are unnecessary. |

Schema v2 also introduces `lineageObjects` (with stable `qualifiedName`s) and `observations` that tie each relationship back to exact files and line numbers for full traceability.

EffectType guidance (v2):

- Simple passthrough/alias: EXACT_COPY
- Function or expression (e.g., UPPER, ROUND): WEAK_COPY
- Aggregations (e.g., SUM, COUNT, AVG): AGGREGATION (or WEAK_COPY if AGGREGATION isn’t supported)
- Multi-source expressions (e.g., a + b): PARTIAL_COPY
- Uncertain/heuristic mapping: AMBIGUOUS

### Examples in v2

#### WHERE without GROUP BY: COUNT()

```sql
SELECT COUNT() total_num
FROM scott.emp
WHERE city = 1
```

Relationships in v2:

```
scott.emp -> data_flow (transform: COUNT(), effectType: AGGREGATION) -> total_num
scott.emp.city -> restricts -> total_num
```

#### WHERE and GROUP BY: COUNT()

```sql
SELECT deptno, COUNT() total_num
FROM scott.emp
WHERE city = 1
GROUP BY deptno
```

Relationships in v2:

```
scott.emp -> data_flow (transform: COUNT(), effectType: AGGREGATION) -> total_num
scott.emp.city -> restricts -> total_num
scott.emp.deptno -> groups -> total_num
```

#### WHERE and GROUP BY: SUM()

```sql
SELECT deptno, SUM(SAL) sal_sum
FROM scott.emp
WHERE city = 1
GROUP BY deptno
```

Relationships in v2:

```
scott.emp.SAL -> data_flow (transform: SUM(SAL), effectType: AGGREGATION) -> sal_sum
scott.emp.deptno -> groups -> sal_sum
scott.emp.city -> restricts -> sal_sum
```

#### WHERE without GROUP BY: SUM()

```sql
SELECT SUM(SAL) sal_sum
FROM scott.emp
WHERE city = 1
```

Relationships in v2:

```
scott.emp.SAL -> data_flow (transform: SUM(SAL), effectType: AGGREGATION) -> sal_sum
scott.emp.city -> restricts -> sal_sum
```

These explicit relationships make it clear which columns supply data, which columns filter the record set, and which provide grouping, while the `transform` captures the exact function used.

### References (v2)

- v2 Schema: [data_lineage_schema.json](mdc:gsp_java/docs/AI/cline_sqlflow/data_lineage_schema.json)
- v2 Design Explanation: [data_lineage_design_explanation.md](mdc:gsp_java/docs/AI/cline_sqlflow/data_lineage_design_explanation.md)

## Expert Guidance: Best Practices for Modeling Aggregations (v2)

Short answer:

- Drop the `RelationRows` pseudo column.
- Model aggregates with three explicit relationships:
  - `data_flow` from actual source columns (or FROM result/table for COUNT(*)), include the aggregate in `transforms.code`, and set `effectType: AGGREGATION`.
  - `restricts` from WHERE/HAVING columns to each aggregate output.
  - `groups` from each GROUP BY column to each aggregate output.

Why this helps governance:

- Shows clearly what sources feed the metric, what filters apply, and how it’s grouped.
- Removes noise and confusion from pseudo columns, improving impact analysis and RCA.

Modeling rules:

- SUM/AVG/MIN/MAX(arg): `data_flow` from the argument column(s) with `transforms` and `effectType: AGGREGATION`.
- COUNT(*) single-table: `data_flow` from the table object with `effectType: AGGREGATION`.
- COUNT(*) multi-table join: `data_flow` from the logical FROM result (implementation node) with `effectType: AGGREGATION`.
- Always add `restricts` from WHERE/HAVING columns and `groups` from GROUP BY columns.

Concrete patterns:

```
-- WHERE without GROUP BY, COUNT(*)
scott.emp -> data_flow (transform: COUNT(), effectType: AGGREGATION) -> total_num
scott.emp.city -> restricts -> total_num

-- WHERE + GROUP BY, COUNT(*)
scott.emp -> data_flow (transform: COUNT(), effectType: AGGREGATION) -> total_num
scott.emp.city -> restricts -> total_num
scott.emp.deptno -> groups -> total_num

-- WHERE + GROUP BY, SUM(sal)
scott.emp.SAL -> data_flow (transform: SUM(SAL), effectType: AGGREGATION) -> sal_sum
scott.emp.city -> restricts -> sal_sum
scott.emp.deptno -> groups -> sal_sum

-- WHERE without GROUP BY, SUM(sal)
scott.emp.SAL -> data_flow (transform: SUM(SAL), effectType: AGGREGATION) -> sal_sum
scott.emp.city -> restricts -> sal_sum
```