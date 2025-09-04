## Transforms

[toc]

### 1. What is a transform?

In SQLFlow, a transform is the piece of code that changes data as it flows
from a source to a target. Think: the expression or function applied on a
column.

```sql
SELECT SUM(Quantity) AS total_quantity
FROM OrderDetails;
```

Here, `SUM(Quantity)` is the transform that derives the target
`total_quantity` from the source `OrderDetails.Quantity`.

![transform sample](../../assets/images/get-started-transform1.png)

Transforms can be as simple as an alias (column passthrough), a function like
`ROUND()` or `UPPER()`, an aggregation like `SUM()`, or a multi-column
expression like `a + b`.

### 2. Where transforms live in the v2 lineage model

In the v2 JSON schema, transforms are recorded on the 1→1 relationship (edge)
between a single source and a single target:

- `relationships[*].transforms[]`: expression/function details that change the
  value (type + code, with optional coordinates)
- `relationships[*].effectType`: the strength/nature of the mapping
  (e.g., `EXACT_COPY`, `MODIFIED_COPY`, `AGGREGATION`, `PARTIAL_COPY`)
- `relationships[*].observations[*].transforms[]`: per-process evidence of the
  same, when multiple processes produce the same logical edge

This aligns with the data lineage design: each column-to-column mapping is a
separate 1→1 edge, and transforms describe how the value is produced.

### 3. Common patterns with examples

#### 3.1 Direct alias (no change)
```sql
SELECT order_id AS report_id
FROM orders;
```
Minimal v2 edge:
```json
{
  "type": "data_flow",
  "sourceId": "orders.order_id",
  "targetId": "RS.report_id",
  "processIds": ["proc_1"],
  "transforms": [ { "type": "expression", "code": "order_id AS report_id" } ],
  "effectType": "EXACT_COPY"
}
```

#### 3.2 Function transform (value changed)
```sql
SELECT ROUND(salary) AS salary_r
FROM employees;
```
Minimal v2 edge:
```json
{
  "type": "data_flow",
  "sourceId": "employees.salary",
  "targetId": "RS.salary_r",
  "processIds": ["proc_1"],
  "transforms": [ { "type": "function", "code": "ROUND(salary)" } ],
  "effectType": "MODIFIED_COPY"
}
```

#### 3.3 Aggregation (granularity changed)
```sql
SELECT deptno, SUM(amount) AS total_amount
FROM orders
GROUP BY deptno;
```
Minimal v2 edges:
```json
{
  "type": "data_flow",
  "sourceId": "orders.amount",
  "targetId": "RS.total_amount",
  "processIds": ["proc_1"],
  "transforms": [ { "type": "function", "code": "SUM(amount)" } ],
  "effectType": "AGGREGATION"
}
```
Optionally add a grouping influence edge:
```json
{ "type": "groups", "sourceId": "orders.deptno", "targetId": "RS.total_amount", "processIds": ["proc_1"] }
```

#### 3.4 Multi-source expression
```sql
SELECT a + b AS sum_ab
FROM t;
```
V2 uses multiple 1→1 edges (one per source column) with the same
`statementKey` and a transform on each edge:
```json
{
  "type": "data_flow",
  "sourceId": "t.a",
  "targetId": "RS.sum_ab",
  "processIds": ["proc_1"],
  "transforms": [ { "type": "expression", "code": "a + b" } ],
  "effectType": "PARTIAL_COPY",
  "statementKey": "h1#stmt1"
}
```
And a similar edge for `t.b -> RS.sum_ab`.

### 4. v1 compatibility (legacy XML) and mapping

In v1, transforms appeared inside the relationship XML. Example:
```xml
<relationship id="2" type="fdd" effectType="function">
    <target id="11" column="SUM" parent_id="10" parent_name="SUM"/>
    <source id="5" column="Quantity" parent_id="4" parent_name="OrderDetails">
    <transforms>
        <transform type="function">
            <code>SUM(Quantity)</code>
        </transform>
    </transforms>
    </source>
</relationship>
```

Mapping to v2:
- Relationship becomes a 1→1 `data_flow` edge with `sourceId` and `targetId`
- Transformation code moves to `relationships.transforms[]`
- Use `effectType` for strength: `EXACT_COPY` / `MODIFIED_COPY` / `AGGREGATION` /
  `PARTIAL_COPY`
- Add `sqlCoordinates` / `observations` when you have statement and evidence
  details

### 5. Practical tips

- Prefer simple, readable `transforms.code` (e.g., `SUM(amount)`,
  `ROUND(salary)`, `a + b`, `order_id AS report_id`)
- Set a reasonable `effectType`:
  - `EXACT_COPY` for aliases/equivalent casts
  - `MODIFIED_COPY` for functions/expressions that change values
  - `AGGREGATION` for aggregates (granularity change)
  - `PARTIAL_COPY` for multi-source contributions
- Record `coordinates` (and `sqlCoordinates`) when possible to enable
  one-click trace back to code
- Keep edges atomic (1 source → 1 target); use `statementKey` to group edges
  from the same statement

