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

### Part 2: Next-Generation Data Lineage Model (v2)

v2 refines the chain into smaller, precise parts so it scales better and is easier to trace.

- **Key improvements**:
  - More precise, 1→1 relationships between specific lineage objects (e.g., a column to an output column).
  - Stronger traceability via `qualifiedName`, `observations` (evidence), and `transforms` (logic snippets).
  - Clearer meaning using `effectType` on each relationship.
- **Concept mapping**:
  - v1 `fdd` becomes explicit copy/transform edges (use `effectType: EXACT_COPY` for pass-through or alias; `MODIFIED_COPY` if function transforms value).
  - v1 `fdr` is captured as constraints like `restricts` (filters) and `groups` (grouping impact).

Applying v2 to the same example:

```
Employees.ManagerID  restricts  -> temp.cteReports (table)
  condition: "ManagerID IS NULL"
  effectType: AMBIGUOUS  (filter affects presence of rows)

temp.cteReports.EmpID   -> temp.result.count_empid (column)
  transforms.code: "COUNT(EmpID)"
  effectType: AGGREGATION  (aggregation changes granularity)

temp.cteReports.EmpLevel -> temp.result.sum_emplevel (column)
  transforms.code: "SUM(EmpLevel)"
  effectType: AGGREGATION  (aggregation changes granularity)
```

Tips for reading v2:
- Each edge is atomic (1 source → 1 target) and can share a `statementKey` to indicate they come from the same SQL statement.
- Use `transforms.code` to show the function/expression that produced the target value.
- Choose an `effectType` that describes the mapping strength:
  - `EXACT_COPY`: simple alias/passthrough
  - `MODIFIED_COPY`: function changes value (e.g., `UPPER(name)`)
  - `AGGREGATION`: `COUNT`, `SUM`, `AVG`, etc.
  - `PARTIAL_COPY`: multi-source expression (e.g., `a + b`)
  - `AMBIGUOUS`: uncertain or heuristic mapping

Note:
- `temp.cteReports` and `temp.result` represent temporary tables (v2 `lineageObjects` of type `table` with `properties.isTemporary = true`), and their fields like `EmpID`, `count_empid`, `sum_emplevel` are `column` lineageObjects. Use a deterministic `qualifiedName` for temporary objects (e.g., `server.database.resultset.{processId}#{sqlHash}#{queryId}`).

Source of truth:
- v2 Schema: [data_lineage_schema.json](mdc:gsp_java/docs/AI/cline_sqlflow/data_lineage_schema.json)
- v2 Design: [data_lineage_design_explanation.md](mdc:gsp_java/docs/AI/cline_sqlflow/data_lineage_design_explanation.md)

#### diagram

![image.png](/images/basic-concepts-dataflow-chain.png)