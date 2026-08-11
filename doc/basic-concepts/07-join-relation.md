## Joins and lineage

[toc]

SQL joins have two different lineage meanings:

- selected fields supply output values;
- join keys and predicates determine which combinations of rows survive.

Legacy dlineage uses `fdd`, `fdr`, and `join` relations. SLPC v0.2 keeps value and row influence separate and adds a typed `JoinSemantics` record for join type, side behavior, and ordered key pairs.

## INNER JOIN

```sql
SELECT o.order_id, c.customer_name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;
```

Legacy dlineage intent:

```
orders.order_id       -> fdd  -> RS.order_id
customers.customer_name -> fdd -> RS.customer_name
orders.customer_id    <-> join <-> customers.customer_id
orders.customer_id    -> fdr  -> RS.PseudoRows
customers.customer_id -> fdr  -> RS.PseudoRows
```

### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> The output mappings are two `VALUE + DIRECT` facts. Each key contributes a separate `ROW + JOIN` fact
> to the result relation. One `JoinSemantics` record has `joinType=INNER`, `conditionForm=ON`, an ordered
> key pair `orders.customer_id = customers.customer_id`, and `leftSideSemantics=FILTERED` /
> `rightSideSemantics=FILTERED`. It refines the row facts and keeps predicate/source-location evidence.

## LEFT JOIN

```sql
SELECT o.order_id, c.customer_name
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id;
```

Legacy dlineage still emits direct value mappings and join/indirect relations. The old edges alone do not reliably distinguish the preserved side from the null-extended side.

### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> VALUE and ROW facts have the same atomic shape as the INNER JOIN case. `JoinSemantics` supplies the
> missing outer-join meaning: `joinType=LEFT`, `leftSideSemantics=PRESERVED`, and
> `rightSideSemantics=NULL_EXTENDED`. This is semantic truth, not a lower-confidence approximation. If the
> analyzer cannot prove a side or key binding, it reports `UNKNOWN`, candidate references, or a diagnostic.

## RIGHT, FULL, and CROSS JOIN

- RIGHT JOIN mirrors LEFT JOIN: the right side is preserved and the left side is null-extended.
- FULL JOIN records both sides as null-extended/preserved according to the contract's proven side semantics.
- CROSS JOIN has `conditionForm=NONE`, no key pairs, and no fabricated `ROW + JOIN` facts. Its `JoinSemantics(CROSS)` record preserves row-multiplication meaning.

## SEMI JOIN with IN/EXISTS

```sql
SELECT o.order_id
FROM orders o
WHERE o.customer_id IN (SELECT c.id FROM customers c);
```

Legacy SQLFlow commonly presents the subquery key as an indirect restriction on the outer result.

### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> `orders.order_id -> result.order_id` is `VALUE + DIRECT`. The existence test decides whether an outer
> row survives, so the canonical influence is `ROW + FILTER`, not `ROW + JOIN`. A
> `JoinSemantics` record with `joinType=SEMI` and `conditionForm=IN` preserves the relational form and key
> pairing. The subquery is retained as a contained intermediate graph node.

## ANTI JOIN with NOT EXISTS/NOT IN

```sql
SELECT o.order_id
FROM orders o
WHERE NOT EXISTS (
  SELECT 1 FROM returns r WHERE r.order_id = o.order_id
);
```

Legacy SQLFlow represents the correlated key as an indirect influence on result rows.

### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> The selected order ID remains `VALUE + DIRECT`. The correlated existence test becomes `ROW + FILTER`,
> refined by `JoinSemantics(joinType=ANTI, conditionForm=EXISTS)`. Literal `1` is occurrence evidence, not
> a catalog field. The correlated subquery, predicate path, and containment remain in `IntermediateGraph`.

## Modeling rules

- Emit one Fact per proven source/target contribution; do not pack a composite key into one opaque edge.
- Keep `VALUE` output flow, `ROW` influence, and `JoinSemantics` together—they answer different questions.
- Assign `joinOrdinal` and `keyPairs[].ordinal` from SQL source order.
- Record ON/USING/NATURAL/EXISTS/IN in `conditionForm` and preserve source locations as evidence.
- Never use confidence to encode preserved/null-extended join sides.
- A declared FK is an `ObjectRelationship(FOREIGN_KEY_REFERENCE)`; an actual SQL join is represented by ROW facts and `JoinSemantics`. Neither implies the other.
- A projector may hide join overlays for readability, but must account for any omitted join semantics in its projection report.
