 [toc]
## Functions in Data Lineage (Beginner Guide)

This page explains how SQL functions are modeled in data lineage. Start
with the simpler v1 view, then see the more precise v2 model. Short
examples and effectType notes help you connect edges to the code.

## Overview: how functions are modeled in v1 vs v2

- v1 (classic model):
  - Functions (including built‑ins and user‑defined) are often modeled
    as lineage objects/nodes. Data then flows (fdd/fdr) through or
    alongside these, and `effectType` reflects the statement kind (e.g.,
    `select`).
  - Aggregations may use the pseudo column `RelationRows` to express row
    count influence (indirect flow, fdr), alongside direct flow for
    aggregate inputs (e.g., `sal -> SUM(sal)`).
  - TVFs are typically treated as table sources; columns flow directly
    to outputs.
- v2 (next‑generation model):
  - Functions are usually not nodes in the dataflow path; they are
    attached to `data_flow` relationships via `transforms.code`, while
    `effectType` describes copy strength (`EXACT_COPY`, `MODIFIED_COPY`,
    `AGGREGATION`, `PARTIAL_COPY`, `AMBIGUOUS`).
  - User‑defined functions (scalar UDFs and TVFs) do get lineage objects
    for dependency/impact analysis (with `calls` edges), but are still
    used on relationships (as transforms) rather than as intermediate
    dataflow nodes.
  - Use `restricts`/`groups` for non‑copy influences; model TVF call
    instances as temporary resultsets linked to the function object.


## 1.1 scalar functions (e.g., ROUND, UPPER, CONCAT)

### v1 modeling

- Treat scalar functions as part of a direct flow (fdd) from the input
  column(s) to the output column; `effectType: select`.

Example (ROUND):
```sql
SELECT ROUND(salary) AS salary_r
FROM emp;
```
```
emp.salary -> fdd -> RS-1.salary_r   (effectType: select)
```

Example (CONCAT):
```sql
SELECT CONCAT(first_name, ' ', last_name) AS full_name
FROM users;
```
```
users.first_name -> fdd -> RS-1.full_name   (effectType: select)
users.last_name  -> fdd -> RS-1.full_name   (effectType: select)
```

Example (alias):
```sql
SELECT order_id AS report_id FROM orders;
```
```
orders.order_id -> fdd -> RS-1.report_id   (effectType: select)
```

### v2 modeling

Do not model scalar functions as nodes. Express them as `data_flow`
edges with a `transform` and a suitable `effectType`.

Example: rounding changes values
```sql
SELECT ROUND(salary) AS salary_r
FROM emp;
```
```
data_flow: emp.salary -> RS-1.salary_r
  - transforms.code: "ROUND(salary)"
  - effectType: MODIFIED_COPY
```

Example: concatenation from multiple inputs
```sql
SELECT CONCAT(first_name, ' ', last_name) AS full_name
FROM users;
```
```
data_flow: users.first_name -> RS-1.full_name
  - transforms.code: "CONCAT(first_name, ' ', last_name)"
  - effectType: MODIFIED_COPY

data_flow: users.last_name  -> RS-1.full_name
  - transforms.code: "CONCAT(first_name, ' ', last_name)"
  - effectType: MODIFIED_COPY
```

Example: alias/identity
```sql
SELECT order_id AS report_id FROM orders;
```
```
data_flow: orders.order_id -> RS-1.report_id
  - transforms.code: "order_id AS report_id"
  - effectType: EXACT_COPY
```

## 1.2 Aggregations (e.g.,SUM, COUNT, AVG, MIN, MAX)

### v1 modeling

- Without GROUP BY, show row‑count influence via `RelationRows` (fdr)
  and direct flow for aggregate inputs where applicable.

Example (no GROUP BY):
```sql
SELECT COUNT(*) AS total_num, SUM(sal) AS total_sal
FROM emp;
```
```
emp.RelationRows -> fdr -> RS-1.total_num   (effectType: select)
emp.RelationRows -> fdr -> RS-1.total_sal   (effectType: select)
emp.sal          -> fdd -> RS-1.total_sal   (effectType: select)
```

- With GROUP BY, add indirect flows from grouping columns and row count;
  keep direct flow from aggregate input columns to aggregate outputs.

Example (with GROUP BY):
```sql
SELECT deptno, COUNT(*) AS total_num, SUM(sal) AS total_sal
FROM emp
GROUP BY deptno;
```
```
emp.RelationRows -> fdr -> RS-1.total_num   (effectType: select)
emp.RelationRows -> fdr -> RS-1.total_sal   (effectType: select)
emp.deptno       -> fdr -> RS-1.total_num   (effectType: select)
emp.deptno       -> fdr -> RS-1.total_sal   (effectType: select)
emp.sal          -> fdd -> RS-1.total_sal   (effectType: select)
```

### v2 modeling

Aggregation changes granularity; mark `effectType: AGGREGATION`. If the
aggregation is over a column, model column→column; for `COUNT(*)` over
the entire table, model table→column.

Example (no GROUP BY):
```sql
SELECT COUNT(*) AS total_num, SUM(sal) AS total_sal
FROM emp;
```
```
data_flow: emp           -> RS-1.total_num
  - transforms.code: "COUNT(*)"
  - effectType: AGGREGATION

data_flow: emp.sal       -> RS-1.total_sal
  - transforms.code: "SUM(sal)"
  - effectType: AGGREGATION
```

Example (with GROUP BY):
```sql
SELECT deptno, COUNT(*) AS total_num, SUM(sal) AS total_sal
FROM emp
GROUP BY deptno;
```
```
// Pass‑through of grouping key
data_flow: emp.deptno -> RS-1.deptno
  - effectType: EXACT_COPY

// Grouping influence
groups: emp.deptno -> RS-1.total_num
groups: emp.deptno -> RS-1.total_sal

// Aggregation edges
data_flow: emp       -> RS-1.total_num
  - transforms.code: "COUNT(*)"
  - effectType: AGGREGATION

data_flow: emp.sal   -> RS-1.total_sal
  - transforms.code: "SUM(sal)"
  - effectType: AGGREGATION
```

## 1.3 Table‑Valued Functions (TVFs)

### v1 modeling

- Treat TVFs as table sources; use direct flows (fdd) from TVF output
  columns to query outputs; `effectType: select`.
- Parameters and function dependency are typically not modeled.

Example:
```sql
SELECT product_name
FROM dbo.get_user_orders(123) AS user_orders;
```
```
get_user_orders.product_name -> fdd -> RS-1.product_name   (effectType: select)
```

### v2 modeling

TVFs return a result set. Model the function definition, a temporary
resultset instance for the call, and connect them with edges.

Example:
```sql
SELECT product_name
FROM dbo.get_user_orders(123) AS user_orders;
```

Conceptual edges and objects:
```
// Process depends on the physical function
calls:   process(sql_script) -> function dbo.get_user_orders

// Function produces a temporary resultset for this call instance
data_flow: function dbo.get_user_orders -> resultset user_orders

// Optional: parameter lineage (constant/column -> function)
data_flow: <param-source> -> function dbo.get_user_orders

// Final value movement into the outer SELECT output
data_flow: user_orders.product_name -> RS-1.product_name
  - effectType: EXACT_COPY
```

Notes:
- Make the resultset a temporary lineage object (unique `qualifiedName`
  using `processId#sqlHash#queryId`).
- Keep edges atomic (1→1). A multi‑source expression becomes multiple
  edges, all sharing the same `statementKey`.

## 2.1 Built‑in

- v1:
  - Built‑in scalar functions appear as direct flows (fdd) from input
    columns to targets; `effectType: select`.
  - Aggregations combine direct flows for inputs with indirect flows via
    `RelationRows` for row‑count influence.
- v2:
  - Built‑in scalar functions (e.g., `ROUND`, `UPPER`, `CONCAT`) and
    built‑in aggregates (`SUM`, `COUNT`, `AVG`, `MIN`, `MAX`) are
    modeled as `data_flow` edges.
- Put the expression in `transforms.code` and set an appropriate
  `effectType`:
  - Scalar value changes: `MODIFIED_COPY`
  - Alias/identity: `EXACT_COPY`
  - Aggregations: `AGGREGATION`
- See sections 1.1 and 1.2 for examples.

## 2.2 User‑Defined Functions (UDFs)

UDFs include both scalar UDFs and table‑valued functions (TVFs). The key
v2 difference from built‑ins is that user‑defined functions are modeled
as first‑class lineage objects (built‑ins are not).

- v1:
  - Treat UDF calls like other function expressions within a direct flow
    (fdd) from input columns to targets; no explicit function object or
    `calls` relationship; `effectType: select`.
  - TVFs are typically treated as table sources; direct flows (fdd) from
    TVF output columns to query outputs.
- v2:
  - Create a lineage object for the function definition (scalar UDF or
    TVF) to support impact analysis and dependency tracking.
  - Add a `calls` edge from the `process` (SQL script/query) to the
    function object.
  - Keep value movement as `data_flow` edges with `transforms.code`
    capturing the call expression.
  - For TVFs, also create a temporary resultset object per call and a
    `data_flow` from the function object to that resultset.

Scalar UDF example:
```sql
SELECT dbo.calculate_tax(o.price) AS final_price
FROM orders o;
```
```
calls:   process(sql_script) -> function dbo.calculate_tax

data_flow: orders.price -> RS-1.final_price
  - transforms.code: "dbo.calculate_tax(o.price)"
  - effectType: MODIFIED_COPY
```

TVF example (see also 1.3):
```sql
SELECT product_name
FROM dbo.get_user_orders(123) AS user_orders;
```
```
calls:     process(sql_script) -> function dbo.get_user_orders
data_flow: function dbo.get_user_orders -> resultset user_orders
data_flow: user_orders.product_name -> RS-1.product_name
  - effectType: EXACT_COPY
```

## v1 → v2 concept mapping (for functions)

- **Built‑ins as expressions**:
  - v1: Direct flow with a function appearing implicitly in the mapping
  - v2: `data_flow` with `transforms.code` and `effectType`
- **Aggregations**:
  - v1: May combine direct and indirect edges (via `RelationRows`)
  - v2: `data_flow + AGGREGATION`, plus `groups` for grouping columns
- **UDFs**:
  - v1: Just part of direct flow
  - v2: Keep `data_flow` for values; add `calls` to the function object
- **TVFs**:
  - v1: Often treated like a table reference
  - v2: Function object + temporary resultset + `data_flow` + `calls`

## Quick effectType guidance (v2)

- **EXACT_COPY**: Alias or reversible/no‑change mapping
- **MODIFIED_COPY**: Value‑changing functions/expressions (ROUND, UPPER,
  CONCAT, hashing, masking)
- **AGGREGATION**: Aggregates (SUM, COUNT, AVG, MIN, MAX, ARRAY_AGG)
- **PARTIAL_COPY**: Multi‑source contributions (e.g., `a + b`) when you
  want to signal partial attribution
- **AMBIGUOUS**: Uncertain mapping or unresolved source

Tip: Always set `transforms.code` to the actual function/expression to
improve traceability for beginners.

## References

- v2 Design Explanation: see `docs/data_lineage_v2/data_lineage_design_explanation.md`
- For aggregation, grouping, and filters, also see `02-direct-dataflow.md`
  and `03-indirect-dataflow-and-pseudo-column.md` for complementary
  background.


