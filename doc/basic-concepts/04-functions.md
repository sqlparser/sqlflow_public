[toc]
## Functions in Data Lineage

This page first shows the current dlineage/SQLFlow output and then explains how SLPC v0.2 preserves the same proven lineage with clearer semantics. Built-in functions are expression logic, while user-defined routines can additionally be catalog endpoints and dependency targets.

## 1. Scalar built-in functions

Legacy dlineage treats scalar functions as part of direct flow (`fdd`) and may show a function node in the detailed diagram.

### ROUND

```sql
SELECT ROUND(salary) AS salary_r
FROM emp;
```

Legacy lineage:

```
emp.salary -> fdd -> RS-1.salary_r   (effectType: select)
```

#### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> The semantic edge is a `Fact` from `emp.salary` to `RS-1.salary_r` with `axis=VALUE` and
> `role=TRANSFORM`. Its `Occurrence` carries transformation evidence for `ROUND(salary)` and source
> location. A detailed SQLFlow view may show a `FUNCTION_RESULT` node and typed transform step inside
> `IntermediateGraph`; the built-in `ROUND` is not published as a catalog endpoint.

### CONCAT with two column inputs and one literal

```sql
SELECT CONCAT(first_name, ' ', last_name) AS full_name
FROM users;
```

Legacy lineage:

```
users.first_name -> fdd -> RS-1.full_name   (effectType: select)
users.last_name  -> fdd -> RS-1.full_name   (effectType: select)
```

#### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> SLPC emits two atomic `VALUE + TRANSFORM` facts, one from each source field to `full_name`. Their
> occurrences retain the shared CONCAT evidence. The space literal is an ordered `literalInputs` entry,
> fingerprinted or redacted by policy; it is not a fake column endpoint. If the producer can prove operand
> order, `gsp.interactive-explain.v1` records ordered operands `first_name`, literal, `last_name`.

### Alias without value change

```sql
SELECT order_id AS report_id FROM orders;
```

Legacy lineage:

```
orders.order_id -> fdd -> RS-1.report_id   (effectType: select)
```

#### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> This is `VALUE + DIRECT`, not `TRANSFORM`: the alias changes display naming but not value semantics.
> Optional copy classification is `EXACT_COPY` and is explicitly non-identity metadata. The SQL alias and
> its location remain occurrence evidence.

## 2. Aggregation functions

### Aggregation without GROUP BY

```sql
SELECT COUNT(*) AS total_num, SUM(sal) AS total_sal
FROM emp;
```

Legacy dlineage combines pseudo-row influence with direct aggregate input:

```
emp.RelationRows -> fdr -> RS-1.total_num
emp.RelationRows -> fdr -> RS-1.total_sal
emp.sal          -> fdd -> RS-1.total_sal
```

#### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> `COUNT(*)` becomes a relation-to-field `VALUE + AGGREGATE` fact from `emp` to `total_num`.
> `SUM(sal)` becomes a field-to-field `VALUE + AGGREGATE` fact from `emp.sal` to `total_sal`.
> Transformation evidence distinguishes the two expressions. No `RelationRows` endpoint is created.

### Aggregation with GROUP BY

```sql
SELECT deptno, COUNT(*) AS total_num, SUM(sal) AS total_sal
FROM emp
GROUP BY deptno;
```

Legacy dlineage adds indirect flows from the grouping column:

```
emp.RelationRows -> fdr -> RS-1.total_num
emp.RelationRows -> fdr -> RS-1.total_sal
emp.deptno       -> fdr -> RS-1.total_num
emp.deptno       -> fdr -> RS-1.total_sal
emp.sal          -> fdd -> RS-1.total_sal
```

#### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> SLPC keeps `deptno -> result.deptno` as `VALUE + DIRECT`; COUNT and SUM as `VALUE + AGGREGATE`; and
> grouping as a relation-targeted ROW fact with `operationKind=GROUP_BY` and
> `operationInputKind=GROUP_KEY`. This preserves value derivation and row/granularity influence as
> different facts instead of collapsing them into one generic indirect edge.

## 3. Table-valued functions

```sql
SELECT product_name
FROM dbo.get_user_orders(123) AS user_orders;
```

Legacy dlineage normally treats the TVF result like a table source:

```
get_user_orders.product_name -> fdd -> RS-1.product_name
```

Routine dependency and parameter lineage may be absent from older output.

#### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> The routine definition is a `ROUTINE/FUNCTION` `Endpoint`. A top-level invocation is
> `StatementOperation(CALL_ROUTINE)` with `CALLEE_ROUTINE`; a call from another routine is
> `ObjectRelationship(CALLS)`. The literal `123` is parameter occurrence evidence, and a proven binding
> may create a `VALUE` fact to a `PARAMETER` endpoint. The call's table result is represented locally in
> `IntermediateGraph` with containment, while `user_orders.product_name -> RS-1.product_name` remains
> `VALUE + DIRECT`. Missing parameter or return bindings must produce candidates/diagnostics, not guessed
> edges.

## 4. CASE expressions

```sql
SELECT
  CASE
    WHEN score >= 60 THEN 'Pass'
    ELSE 'Fail'
  END AS status
FROM exams;
```

Legacy dlineage treats CASE similarly to a function:

```
exams.score -> fdd -> RS-1.status   (effectType: select)
```

#### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> `exams.score -> status` is `axis=VALUE`, `role=CONDITION`: `score` chooses the returned branch but is
> not copied into `status`. Because the result values are synthesized entirely from literals, a separate
> source-null `VALUE + DERIVED` fact represents that derivation. The literals `60`, `'Pass'`, and `'Fail'`
> are ordered, fingerprinted/redacted occurrence inputs. When available, the interactive profile records a
> typed CASE step and branch operand order. It must not expose literal secrets in evidence, diagnostics, or
> extension text.

## 5. Scalar user-defined functions

```sql
SELECT dbo.calculate_tax(o.price) AS final_price
FROM orders o;
```

Legacy dlineage usually retains the value dependency as direct flow and may not expose a separate routine dependency:

```
orders.price -> fdd -> RS-1.final_price
```

#### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> `orders.price -> final_price` is a `VALUE + TRANSFORM` fact with call-expression evidence. If
> `dbo.calculate_tax` resolves to an authoritative routine, SLPC also emits `CALL_ROUTINE` or `CALLS` as
> appropriate and connects proven argument/return `PARAMETER` endpoints with VALUE facts. The built-in
> expression path and the catalog routine dependency are complementary; neither substitutes for the other.

## 6. Practical rules

- Built-ins belong in transformation evidence and optionally the interactive graph, not in canonical catalog identity.
- UDFs and TVFs may be routine endpoints only when their identity is proven.
- Multi-source expressions produce one atomic fact per proven source; ordered operands belong in the interactive profile.
- `VALUE + DIRECT`, `TRANSFORM`, `AGGREGATE`, and `CONDITION` state why a value contributes.
- Predicate, join, grouping, and window effects remain on the ROW axis or use the contract's operation fields.
- Copy classifications such as `EXACT_COPY`, `MODIFIED_COPY`, and `AGGREGATION` are derived occurrence annotations, never fact identity.
- Unresolved calls, parameters, return values, or operand order are represented with Candidate, Diagnostic, and completeness status.

## References

- For grouping and row influence, see [Indirect Dataflow and Pseudo Columns](./03-indirect-dataflow-and-pseudo-column.md).
- For detailed expression paths, see [Transforms](./08-transforms.md).
