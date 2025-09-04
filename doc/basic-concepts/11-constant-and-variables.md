## 1 Constant

Constants used in the SQL statement will be collected and saved in a pseudo table: `constantTable`.
Each SQL statement will create a `constantTable` table to save the constants used in the SQL statement.

So SQLFlow able to generate the data flow to trace the constant value.
> Constants only will be collected when the /showConstant is set to true in the SQLFlow.
and constants used in the insert statement WILL NOT BE collected in order to avoid too many constants even if the /showConstant is set to true.

>By default, the /showConstant is set to false in the SQLFlow which means constants will not be collected.

```sql
SELECT 'constant' as field1, 2 as field2;
```

a `table` XML tag and type attribute value `constantTable`:

```xml
  <table id="5" name="SQL_CONSTANTS-1" type="constantTable">
      <column id="6" name="'constant'"/>
      <column id="8" name="2"/>
  </table>
```

```sql
UPDATE table1 t1 JOIN table2 t2 ON t1.field1 = t2.field1 
SET t1.field2='constant' and t1.field3=2;
```

a `table` XML tag and type attribute value `constantTable`:

```xml
  <table id="15" name="SQL_CONSTANTS-1" type="constantTable">
      <column id="16" name="'constant'"/>
      <column id="17" name="2"/>
  </table>
```

### v1 representation (schema perspective)

- In v1, constants are represented via a pseudo table `constantTable` in the
  object list (dbobjs). Each literal appears as a column under that table.
- Relations may mark synthesized sources with `source = "system"` and can
  label how the target is derived via `dependency = simple/function/expression`.
- `effectType` in v1 expresses the operation kind (e.g., `select`, `insert`,
  `update`, `merge_insert`), not the copy strength used in v2.

Simplified v1-style snapshot (illustrative):
```json
{
  "dbobjs": [
    { "id": 5, "type": "constantTable", "name": "SQL_CONSTANTS-1" , "columns": [
      { "id": 6, "name": "'constant'" },
      { "id": 8, "name": "2" }
    ]}
  ],
  "relations": [
    {
      "id": 9001,
      "type": "fdd",
      "effectType": "select",
      "dependency": "expression",
      "target": { "id": 101, "column": "price_with_tax", "parent_id": 100, "parent_name": "RS" },
      "source": [
        { "id": 11, "column": "price", "parent_id": 10, "parent_name": "orders" },
        { "id": 8, "column": "2", "parent_id": 5, "parent_name": "SQL_CONSTANTS-1", "source": "system" }
      ]
    }
  ]
}
```

## 2 Variables

SQLFlow able to generate the data flow to trace the variable value which usually used in the stored procedure and return value.
Without the trace of the variable, the data flow is not complete.

```sql
-- sql server sample query
CREATE FUNCTION dbo.ufnGetInventoryStock(@ProductID int)
RETURNS int
AS
-- Returns the stock level for the product.
BEGIN
    DECLARE @ret int;
    SELECT @ret = SUM(p.Quantity)
    FROM Production.ProductInventory p
    WHERE p.ProductID = @ProductID
        AND p.LocationID = '6';
     IF (@ret IS NULL)
        SET @ret = 0;
    RETURN @ret;
END;

create view v_product as
SELECT ProductModelID, Name, dbo.ufnGetInventoryStock(ProductID)AS CurrentSupply
FROM Production.Product
WHERE ProductModelID BETWEEN 75 and 80;
```

As you can see, with the trace of the variable, the data flow from `Production.ProductInventory.Quantity` to the `v_product.CurrentSupply` is complete.

![trace variable](../../assets/images/get-started-11-variables1.png)

The data lineage in xml format is as follows:

```xml
<variable id="19" name="@ret" type="variable" subType="record" parent="dbo.ufnGetInventoryStock">
    <column id="20" name="@ret"/>
</variable>
```

### v1 representation (schema perspective)

- In current v1 XML outputs, variables appear as separate `<variable>` nodes
  (see example above), with `type="variable"`, optional `subType`, and an
  owning parent (e.g., a function/procedure).
- The v1 JSON schema focuses on `dbobjs` + `relations` and does not enumerate a
  dedicated `variable` type; implementers may serialize variables as objects in
  practice and reference them from relations to complete end-to-end lineage.



## 3 Best practices in v2 (constants and variables)

This section explains how to model constants and variables elegantly in the v2
lineage schema for better precision, scalability, and traceability.

### 3.1 Constants (literals)

Goal: capture when a literal value contributes to a target column without
blowing up the graph.

- Represent the literal as a dedicated lineage object only when helpful for
  analysis; otherwise, keep it inline in the transform expression.
- When modeled as an object, use `type: column` with a deterministic
  `qualifiedName` under a logical `constantTable` for that statement.
- Prefer atomic edges (1 source → 1 target) with a transform showing the
  expression that includes the literal.

Option A — inline in transform (simple and sufficient for most cases):
```json
{
  "type": "data_flow",
  "sourceId": "orders.price",
  "targetId": "RS.price_with_tax",
  "processIds": ["proc_1"],
  "transforms": [ { "type": "expression", "code": "price + 2" } ],
  "effectType": "MODIFIED_COPY"
}
```

Option B — explicit constant object (when you need literal provenance):
```json
{
  "lineageObjects": [
    { "id": "const_table_stmt1", "name": "SQL_CONSTANTS-1", "type": "table", "qualifiedName": "default_server.default_db.resultset.const#h1#stmt1", "properties": { "isTemporary": true } },
    { "id": "const_2_stmt1", "name": "2", "type": "column", "qualifiedName": "default_server.default_db.resultset.const#h1#stmt1.2" }
  ],
  "relationships": [
    { "type": "data_flow", "sourceId": "orders.price", "targetId": "RS.price_with_tax", "processIds": ["proc_1"], "transforms": [{ "type": "expression", "code": "price + 2" }], "effectType": "MODIFIED_COPY", "statementKey": "h1#stmt1" },
    { "type": "data_flow", "sourceId": "const_2_stmt1", "targetId": "RS.price_with_tax", "processIds": ["proc_1"], "transforms": [{ "type": "expression", "code": "price + 2" }], "effectType": "PARTIAL_COPY", "statementKey": "h1#stmt1" }
  ]
}
```

Recommendations:
- Default to Option A. Use Option B for security/lineage audits (e.g., PII
  masking thresholds, business constants) where literal traceability matters.
- Never create constants for every INSERT value by default; guard with
  configuration to avoid graph bloat.

### 3.2 Variables (procedure/session variables, return values)

Goal: keep end-to-end lineage complete across procedural code while preventing
node explosion.

- Model variables as temporary lineage objects (usually `type: column`, under a
  `type: table` variable scope if desired) with deterministic `qualifiedName`
  tied to the process and query block (e.g., `...variable.{processId}#{sqlHash}#{queryId}.@ret`).
- Use 1→1 edges to connect from source columns/constants to variables, and from
  variables to downstream results or return values.
- Record transforms to show assignments and expressions.

Example (aligning with the v1 function sample):
```json
{
  "lineageObjects": [
    { "id": "var_ret", "name": "@ret", "type": "column", "qualifiedName": "default_server.default_db.variable.procA#h2#stmt5.@ret", "properties": { "isTemporary": true } }
  ],
  "relationships": [
    { "type": "data_flow", "sourceId": "Production.ProductInventory.Quantity", "targetId": "var_ret", "processIds": ["proc_fn"], "transforms": [{ "type": "function", "code": "SUM(Quantity)" }], "effectType": "AGGREGATION", "statementKey": "h2#stmt5" },
    { "type": "data_flow", "sourceId": "var_ret", "targetId": "RS.CurrentSupply", "processIds": ["proc_view"], "effectType": "EXACT_COPY", "statementKey": "h3#stmt1" }
  ]
}
```

Recommendations:
- Use variables sparingly as explicit nodes. Create them when they bridge
  non-SQL or multi-statement logic, or are returned outward.
- Prefer expression-only edges when the variable is purely local and does not
  affect downstream objects.

### 3.3 Governance and performance notes

- Deterministic IDs: follow the qualifiedName rules (process-aware for temporary
  objects), then hash to `id` for stable merges.
- Keep edges atomic (1 source → 1 target). Use `statementKey` to group all
  edges from the same statement.
- Use `observations` to capture per-process evidence and `sqlCoordinates` for
  jump-to-code.
- Provide configuration switches akin to v1’s `/showConstant` to enable
  constants/variables only when needed.
