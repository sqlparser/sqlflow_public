[toc]
## Exploring Direct Data Flow

In our introduction, we learned that a **direct data flow** is when data moves from a source to a target. This is the most common and straightforward type of data lineage. This article explores several common SQL patterns that create these direct data flows.

### 1. Direct Flow in `SELECT` Statements

The simplest example of a direct data flow is a basic `SELECT` statement. When you select a column, its data is directly copied to the result of your query.

```sql
SELECT a.empName AS "eName"
FROM scott.emp a
WHERE sal > 1000
```

In this query, the data from the `empName` column in the `scott.emp` table flows directly to the output column, which is renamed to `"eName"`.

The lineage is clear and simple:

`scott.emp.empName -> direct -> Result."eName"`

Effect type:
- v1: effectType: select (produced by a SELECT projection)

This is visualized with a solid arrow from the source column to the target column.

![Direct data flow in a SELECT statement](https://images.gitee.com/uploads/images/2021/0702/165128_bef55fd4_8136809.png)

#### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> `scott.emp.empName` and `Result.eName` are field `Endpoint` records. Their atomic `Fact` is
> `axis=VALUE`, `role=DIRECT`, `operationKind=NONE`, `operationInputKind=NONE`. The alias is display and
> occurrence evidence; it does not change the fact identity. `sal` is not another value source—it creates
> a separate `ROW + FILTER` fact to the result relation. The query is also represented by
> `StatementOperation(QUERY, CONTENT_READ)`.

### 2. Direct Flow Through Functions

Functions are a common way to transform data. Even when a function modifies a value (like rounding a number or changing text to uppercase), SQLFlow still considers this a direct data flow because the output is directly derived from the input.

```sql
SELECT ROUND(salary) AS sal 
FROM scott.emp
```

The lineage here is a two-step process:
1.  Data flows from the `salary` column *into* the `ROUND()` function.
2.  The result from the `ROUND()` function flows *out to* the final `sal` column.

This detailed view shows the function as an intermediate step in the transformation:

`scott.emp.salary -> direct -> ROUND() -> direct -> sal`

Effect type:
- v1: function edge: effectType: function; function result to select list: effectType: select

![Data flow through a function](https://images.gitee.com/uploads/images/2021/0702/172358_bc2c88ad_8136809.png)

#### Simplified View

For a higher-level view, you might want to hide the function and just see the direct relationship from the original source to the final target. SQLFlow allows you to toggle this view, simplifying the diagram to show:

`scott.emp.salary -> direct -> sal`

![Simplified data flow, hiding the function](https://images.gitee.com/uploads/images/2021/0702/172626_96c936a1_8136809.png)

#### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> The canonical semantic spine contains one `VALUE + TRANSFORM` fact from `emp.salary` to `Result.sal`.
> Its `Occurrence` carries transformation evidence for `ROUND(salary)` and the source location. The
> detailed clickable view may additionally show a `FUNCTION_RESULT` node and typed transform step inside
> `IntermediateGraph`; a simpler projector can hide those nodes without changing the canonical fact. A
> projector that cannot consume the detailed graph must report that projection loss.

### 3. Direct Flow Between Tables

Direct data flows are not limited to queries(SELECT). They are fundamental to how data moves between tables using statements like `INSERT`, `UPDATE`, `MERGE`, or `CREATE TABLE AS SELECT`.

#### `INSERT ... SELECT` Example

An `INSERT ... SELECT` statement is a classic example of data flowing directly from one table to another.

```sql
INSERT INTO employees_archive (emp_id, emp_name)
SELECT emp_no, emp_name
FROM employees
WHERE hire_date < '2020-01-01';
```

Here, SQLFlow will create two direct data flows:
*   `employees.emp_no -> direct -> employees_archive.emp_id`
*   `employees.emp_name -> direct -> employees_archive.emp_name`

Effect type:
- v1: effectType: insert (produced by an INSERT ... SELECT)

This clearly shows that data from the `employees` table is being used to populate the `employees_archive` table.

#### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> SLPC emits two independent `VALUE + DIRECT` facts:
> `employees.emp_no -> employees_archive.emp_id` and
> `employees.emp_name -> employees_archive.emp_name`. The statement is
> `StatementOperation(INSERT, CONTENT_WRITE)` with `WRITE_TARGET=employees_archive` and
> `READ_SOURCE=employees`. The date literal belongs to the filter occurrence as redacted/fingerprinted
> `literalInputs`; `employees.hire_date` creates a `ROW + FILTER` fact to the write-producing relation.
> All records share the same `statementId`, so a separate ad-hoc grouping key is unnecessary.

### References

1. Data lineage code used in this article is generated by [DataFlowAnalyzer](https://github.com/sqlparser/gsp_demo_java/tree/master/src/main/java/demos/dlineage) tools.
2. Diagrams used in this article are generated by the [Gudu SQLFlow Cloud version](https://sqlflow.gudusoft.com/).
