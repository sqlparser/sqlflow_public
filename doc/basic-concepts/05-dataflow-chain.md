## Dataflow chain

Think of a dataflow chain like passing a message up a line: when one query produces a result (a subquery/CTE), and the next query uses that result, the influence from the lower step continues to the upper step.

```sql
WITH
  cteReports (EmpID, FirstName, LastName, MgrID, EmpLevel)
AS (
  SELECT EmployeeID, FirstName, LastName, ManagerID, EmpLevel  -- RS-1
  FROM Employees
  WHERE ManagerID IS NULL
)
SELECT
  COUNT(EmpID), SUM(EmpLevel)  -- RS-2
FROM cteReports;
```

### Part 1: Current Data Lineage Model (v1)

- **Core concepts**: v1 captures data objects as `dbobjs` (tables, columns, result sets) and edges as `relations`.
- **Relationship types**:
  - **fdd**: direct dataflow (value is directly copied/derived without filtering/aggregation semantics).
  - **fdr**: indirect/impact flow (conditions or grouping that affect which rows/aggregations appear upstream).

In the CTE above, the filter `WHERE ManagerID IS NULL` makes `Employees.ManagerID` affect which rows exist in the CTE result:

```
Employees.ManagerID -> indirect (fdr) -> RS-1.RelationRows   (effectType: select)
```

Because `cteReports` is used by the upper query, this impact continues upward:

```
Employees.ManagerID -> indirect (fdr) -> RS-1.RelationRows -> indirect (fdr) -> CTE-CTEREPORTS.RelationRows   (effectType: select)
```

Ignoring the intermediate result set, the end-to-end impact is:

```
Employees.ManagerID -> indirect (fdr) -> RS-2.COUNT(EmpID)   (effectType: select)
Employees.ManagerID -> indirect (fdr) -> RS-2.SUM(EmpLevel)  (effectType: select)
```

Notes:
- **effectType (v1)** here records the SQL statement kind (both are `select`).
- This helps explain why the upper-level aggregations depend on the lower-level filter.

Source of truth:
- v1 Schema: [data_lineage_schema_v1.json](mdc:gsp_java/docs/AI/cline_sqlflow/data_lineage_schema_v1.json)
- v1 Design: [data_lineage_design_explanation_v1.md](mdc:gsp_java/docs/AI/cline_sqlflow/data_lineage_design_explanation_v1.md)

### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> SLPC stores the canonical end-to-end semantics and the explainable chain at the same time:
>
> - `Employees.ManagerID -> CTE/result relation` is a `ROW + FILTER` fact with predicate evidence for
>   `ManagerID IS NULL`.
> - `Employees.EmployeeID -> result.COUNT(EmpID)` is a `VALUE + AGGREGATE` path; the relation endpoint may
>   also be the proven source for `COUNT(*)`-style row aggregation.
> - `Employees.EmpLevel -> result.SUM(EmpLevel)` is a separate `VALUE + AGGREGATE` fact.
> - `IntermediateGraph` keeps `SELECT_LIST`, `CTE`, and upper select-list nodes, their local names,
>   containment, edges, and all proven paths for the clickable diagram.
> - Each collapsed fact points to occurrence/evidence from the statement. If collapse cannot prove a
>   single safe semantic path, SLPC keeps the graph paths and reports `PARTIAL` or a diagnostic instead of
>   deleting the path.
>
> VALUE and ROW paths are never ranked against each other. Both survive when both are proven, and multiple
> chains between the same boundaries remain separately explainable.

#### diagram

![image.png](/images/basic-concepts-dataflow-chain.png)
