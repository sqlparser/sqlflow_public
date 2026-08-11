[toc]
## Indirect dataflow

Indirect dataflow captures how columns influence which rows or groups appear without directly supplying the target value. This commonly occurs in `WHERE`, `HAVING`, `QUALIFY`, `GROUP BY`, join predicates, and window clauses.

## WHERE Clause

```sql
SELECT a.empName "eName"
FROM scott.emp a
WHERE sal > 1000
```

The total number of result rows is influenced by `sal`. Legacy dlineage expresses that influence through a pseudo-column:

```
scott.emp.sal -> indirect (fdr) -> RS-1.RelationRows
```

The relation type is `fdr`; its legacy `effectType` is `select`.

![image.png](https://images.gitee.com/uploads/images/2021/1206/120228_c087c542_8136809.png)

### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> SLPC does not publish `RelationRows` as a fake column. It emits
> `scott.emp.sal -> result relation` as an atomic `Fact` with `axis=ROW`, `role=FILTER`,
> `operationKind=NONE`, and `operationInputKind=NONE`. The selected value remains a separate
> `VALUE + DIRECT` fact from `empName` to `eName`. The filter `Occurrence` carries predicate evidence,
> `clauseKind=WHERE`, source location, and the fingerprinted literal `1000`.

## GROUP BY Clause

```sql
SELECT deptno, COUNT(*) AS totalNum, SUM(sal) AS totalSal
FROM scott.emp
GROUP BY deptno;
```

Legacy dlineage uses direct and indirect relations:

```
scott.emp.deptno -> indirect -> COUNT(*)
scott.emp.deptno -> indirect -> SUM(sal)
scott.emp.sal    -> direct   -> SUM(sal)
```

### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> The value facts are `emp.deptno -> result.deptno` as `VALUE + DIRECT`,
> `emp -> result.totalNum` as `VALUE + AGGREGATE` for `COUNT(*)`, and
> `emp.sal -> result.totalSal` as `VALUE + AGGREGATE`. Grouping is not a copy edge: it is a row fact from
> `emp.deptno` to the result relation with `role=UNKNOWN`, `operationKind=GROUP_BY`, and
> `operationInputKind=GROUP_KEY`. Row Impact Detail can expand that relation-level influence to the two
> aggregate targets when a projector needs field-level presentation.

### Aggregates Without GROUP BY: Table-Level Aggregation

```sql
SELECT COUNT(*) AS totalNum, SUM(sal) AS totalSal
FROM scott.emp
```

Legacy dlineage uses `RelationRows` for row-count influence:

```
scott.emp.RelationRows -> indirect -> COUNT(*)
scott.emp.RelationRows -> indirect -> SUM(sal)
```

![image.png](https://images.gitee.com/uploads/images/2021/1206/120353_cfebf6b1_8136809.png)

### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> `COUNT(*)` is a relation-to-field `VALUE + AGGREGATE` fact from `scott.emp` to `totalNum`.
> `SUM(sal)` is a field-to-field `VALUE + AGGREGATE` fact from `emp.sal` to `totalSal`. Their occurrences
> retain transformation evidence and source locations. No physical endpoint is invented for `COUNT(*)`,
> `SUM(sal)`, or `RelationRows`; optional function-result nodes belong only in `IntermediateGraph`.

## RelationRows (pseudo column)

Legacy SQLFlow uses **RelationRows** (also displayed as `PseudoRows`) to represent a relation's row set or row count in a column-centric graph. It fills two legacy needs:

- connecting predicate and grouping influence to result rows;
- displaying table-level operations in a column-level diagram.

It is useful as a compatibility presentation node, but it is not a database column and must not receive a canonical field identity in SLPC.

### Table-level rename using RelationRows

```sql
ALTER TABLE t2 RENAME TO t3;
```

Legacy dlineage can render the table-level operation through pseudo-columns:

```
t2.RelationRows -> direct (fdd) -> t3.RelationRows
```

![image.png](https://images.gitee.com/uploads/images/2021/1206/120446_f7e66732_8136809.png)

### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> Rename is not value copying. SLPC emits `StatementOperation(RENAME)` with participants
> `BEFORE_OBJECT=t2` and `AFTER_OBJECT=t3`, and `contentSemantics=IDENTITY_CONTINUITY`. It must not create
> a guessed `VALUE + DIRECT` fact. A legacy projector may synthesize the old `RelationRows` arrow for UI
> compatibility, but must label it `COMPATIBILITY_SYNTHESIZED` and point back to the operation.

The following batch shows why legacy SQLFlow used the pseudo-column in both column-level and table-level views:

```sql
CREATE VIEW v1 AS SELECT f1 FROM t2;
ALTER TABLE t2 RENAME TO t3;
```

Legacy dlineage represents the view value chain and the rename separately:

```
t2.f1           -> direct -> RS-1.f1 -> direct -> v1.f1
t2.RelationRows -> direct -> t3.RelationRows
```

![image.png](https://images.gitee.com/uploads/images/2021/1206/140840_6f229397_8136809.png)

### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> The first statement produces a `VALUE + DIRECT` fact `t2.f1 -> v1.f1` plus
> `StatementOperation(CREATE_VIEW, DEFINITION_ONLY)`. Its select-list hop remains available in an
> `IntermediateGraph` for the clickable diagram. The second statement produces the typed `RENAME`
> operation described above. Because both records carry ordered artifact and statement identities, impact
> traversal can respect the rename boundary without pretending it is column value flow.

## How SLPC replaces RelationRows

| Legacy use | SLPC v0.2 record |
|---|---|
| `WHERE`, `HAVING`, `QUALIFY` influence | `Fact(axis=ROW, role=FILTER)` targeting a relation |
| Join condition influence | `Fact(axis=ROW, role=JOIN)` plus `JoinSemantics` |
| `GROUP BY` influence | `Fact(axis=ROW, operationKind=GROUP_BY, operationInputKind=GROUP_KEY)` |
| `COUNT(*)` | relation-to-field `Fact(axis=VALUE, role=AGGREGATE)` |
| Rename | `StatementOperation(RENAME, IDENTITY_CONTINUITY)` |
| UI-only pseudo row node | projector compatibility node derived from an SLPC owner |

The replacement preserves both VALUE and ROW paths. It does not apply the old shortcut of selecting a single "stronger" chain when several paths exist. If path collapse is incomplete or ambiguous, the full path remains in `IntermediateGraph` and the producer reports completeness or a diagnostic.

## References

1. XML output described here is generated by [DataFlowAnalyzer](https://github.com/sqlparser/gsp_demo_java/tree/master/src/main/java/demos/dlineage).
2. Diagrams are generated by the [Gudu SQLFlow Cloud version](https://sqlflow.gudusoft.com/).
