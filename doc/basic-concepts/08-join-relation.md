## Joins and lineage

[toc]

### 1. v1 model: what is a join and how it’s captured

In SQL, a JOIN combines rows from two or more tables based on a condition. In
v1, joins are represented via relations with `type = join` for the condition
edge, and `type = fdd`/`fdr` to capture data movement and influence:

- `fdd` (direct data flow): input columns that feed the target columns
- `fdr` (indirect/impact): columns in conditions (e.g., `ON`, `WHERE`) that
  restrict or influence results
- `join`: dedicated relation capturing join conditions between sources

Example (simplified):
```sql
SELECT o.order_id, c.customer_name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;
```
v1 intent:
- fdd: `orders.order_id -> RS.order_id`, `customers.customer_name -> RS.customer_name`
- join: `orders.customer_id <-> customers.customer_id` (join key relation)
- fdr: join condition influences the result rows

This gives both the value lineage (which columns produce outputs) and the
filtering influence (which columns limit or shape the result via the join).

### 2. v2 best practice: atomic edges with data_flow and restricts

In v2, all edges are 1→1. Model joins using two complementary edge types:

- `data_flow`: each output column has one or more source columns
- `restricts`: join-key columns from one side constrain the output columns
  produced by the other side (or vice versa)

We also use `statementKey` to group the edges produced by the same join
statement, and `sqlCoordinates` to anchor edges back to the `JOIN ... ON ...`
location.

#### 2.1 INNER JOIN
```sql
SELECT o.order_id, c.customer_name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;
```
Minimal v2 edges:
```json
{
  "type": "data_flow",
  "sourceId": "orders.order_id",
  "targetId": "RS.order_id",
  "processIds": ["proc"],
  "statementKey": "h1#stmt1"
}
```
```json
{
  "type": "data_flow",
  "sourceId": "customers.customer_name",
  "targetId": "RS.customer_name",
  "processIds": ["proc"],
  "statementKey": "h1#stmt1"
}
```
```json
{
  "type": "restricts",
  "sourceId": "orders.customer_id",
  "targetId": "RS.customer_name",
  "processIds": ["proc"],
  "condition": "o.customer_id = c.customer_id",
  "statementKey": "h1#stmt1"
}
```
```json
{
  "type": "restricts",
  "sourceId": "customers.customer_id",
  "targetId": "RS.order_id",
  "processIds": ["proc"],
  "condition": "o.customer_id = c.customer_id",
  "statementKey": "h1#stmt1"
}
```

Explanation:
- Each output column is mapped by a `data_flow` edge from its source table.
- The join keys from the opposite side add `restricts` edges, capturing the
  semantics that both sides must match.

#### 2.2 LEFT JOIN
```sql
SELECT o.order_id, c.customer_name
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id;
```
- `data_flow` stays the same (outputs sourced from `orders` and `customers`).
- `restricts` from the left key (`orders.customer_id`) to any outputs remains,
  since the left side determines which rows appear.
- The right key (`customers.customer_id`) may be represented as a weaker
  influence (optional). In practice, use `restricts` for both sides but
  optionally set lower `confidence` on the right side to signal null-extended
  semantics.

#### 2.3 RIGHT/FULL/CROSS JOIN
- RIGHT JOIN mirrors LEFT JOIN.
- FULL OUTER JOIN: both sides are optional; use `restricts` from both sides and
  optionally set lower `confidence`.
- CROSS JOIN: no condition; omit `restricts`. Only `data_flow` edges apply.

### 3. v1 → v2 mapping and tips

- v1 `join` relations become pairs of `restricts` edges in v2 (one per join key
  direction, targeting influenced outputs). v1 `fdd/fdr` split into 1→1
  `data_flow`/`restricts` edges.
- Use `statementKey` to group all edges from the same `JOIN` statement, and
  `sqlCoordinates` to anchor the edges at the `ON` clause.
- Keep edges atomic (1 source → 1 target). For composite keys, create one
  `restricts` edge per participating column.
- For UI, default to show `data_flow` edges; allow toggling `restricts` for
  clarity in dense graphs. Summarize join condition inline (short preview of
  `condition`).

### 4. Why this matches industry practice

- Commercial tools focus on clear column-to-column mappings and show join
  constraints as separate, optional overlays. Our v2 approach mirrors this by
  keeping value lineage (`data_flow`) separate from conditional influence
  (`restricts`), with statement grouping and precise coordinates for trace-back.