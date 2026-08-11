## Transforms

[toc]

A transform is the expression or function that explains how a target value is derived from one or more sources. Legacy dlineage stores transform text inside relationship XML. SLPC v0.2 separates the stable semantic fact from statement-specific evidence and, when available, from the detailed typed expression graph.

## Direct alias

```sql
SELECT order_id AS report_id
FROM orders;
```

Legacy dlineage emits a direct `fdd` relation; the alias may appear in transform or coordinate metadata.

### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> `orders.order_id -> result.report_id` is `VALUE + DIRECT`. Alias text and its source location belong to
> the `Occurrence`; they do not change fact identity. An optional derived copy classification may say
> `EXACT_COPY`, but classification is not canonical identity.

## Function transform

```sql
SELECT ROUND(salary) AS salary_r
FROM employees;
```

Legacy dlineage emits `fdd`, often with `dependency=function` and transform code such as `ROUND(salary)`.

### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> `employees.salary -> result.salary_r` is `VALUE + TRANSFORM`. Its occurrence carries transformation
> evidence and source location. The producer may additionally emit a typed `ROUND` step and ordered input
> in `gsp.interactive-explain.v1`. If typed operation or operand order cannot be proven, it keeps the
> canonical fact and reports the detailed-profile loss instead of guessing.

## Aggregation

```sql
SELECT deptno, SUM(amount) AS total_amount
FROM orders
GROUP BY deptno;
```

Legacy dlineage normally combines direct aggregate input with indirect grouping influence:

```
orders.amount -> fdd -> result.total_amount
orders.deptno -> fdr -> result/RelationRows
```

### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> `orders.amount -> total_amount` is `VALUE + AGGREGATE` with `SUM(amount)` evidence.
> `orders.deptno -> result.deptno` is `VALUE + DIRECT`. Its grouping effect is an independent ROW fact
> with `operationKind=GROUP_BY` and `operationInputKind=GROUP_KEY`. This avoids treating grouping as value
> copying while preserving both paths.

## Multi-source expression

```sql
SELECT a + b AS sum_ab
FROM t;
```

Legacy dlineage emits two `fdd` sources, usually carrying the same expression text:

```
t.a -> fdd -> result.sum_ab
t.b -> fdd -> result.sum_ab
```

### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> SLPC emits two atomic `VALUE + TRANSFORM` facts, one for `t.a` and one for `t.b`, with occurrences tied
> to the same statement. Their facts do not claim operand position. When the analyzer proves the expression
> tree, `gsp.interactive-explain.v1` stores a typed addition step with ordered operands 1 and 2 and an
> `IntermediateGraph` path to `sum_ab`. Without that proof, the facts remain valid and a diagnostic reports
> that ordered interactive explanation is unavailable.

## Legacy XML mapping

A legacy transform can look like this:

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

The legacy adapter maps the proven source and target to a `VALUE + AGGREGATE` fact. The XML relation occurrence becomes SLPC occurrence/evidence. Raw expression text crosses a security boundary only when the evidence policy allows it; otherwise SLPC keeps an approved fingerprint or redaction. A legacy transform label alone is insufficient proof for a typed operation or operand order.

## Practical rules

- Keep semantic identity (`Fact`) separate from per-statement evidence (`Occurrence`).
- Use `DIRECT`, `TRANSFORM`, `AGGREGATE`, `CONDITION`, or `DERIVED` according to the source's actual value role.
- Emit one atomic fact for each proven source contribution.
- Put typed steps and ordered operands in the interactive profile, not in fact identity.
- Put source coordinates in evidence; put diagram x/y layout in the SQLFlow product layer.
- Redact secrets and sensitive literals before evidence, diagnostics, or extensions are serialized.
- Report partial analysis and profile loss explicitly; never manufacture a complete expression graph from display text.
