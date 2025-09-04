[toc]
## Introduction: What is Data Lineage?

Think of data lineage as a family tree for your data. It shows you the complete journey of your data—where it comes from, how it changes, and where it ends up. SQLFlow is a tool that automatically creates this data lineage by analyzing your SQL code.

Understanding data lineage is crucial for tasks like:
*   **Impact Analysis:** If you need to change a table or column, you can see everything that will be affected downstream.
*   **Troubleshooting:** When you see a bad report, you can trace the data back to its source to find the root cause of the problem.
*   **Data Governance:** Knowing the origin and transformations of data helps ensure compliance and data quality.

![A high-level view of data lineage](https://images.gitee.com/uploads/images/2021/0706/171437_139f041e_8136809.png)

## The Core Components of SQLFlow Lineage

SQLFlow breaks down data lineage into two main components:

1.  **Data Objects:** These are the individual "things" in your database that hold data. This includes tables, views, and their columns.
2.  **Relationships:** These are the connections that show how data flows between the data objects.

Let's explore the most common types of relationships you'll see in SQLFlow.

## Understanding Relationship Types

### 1. Direct Data Flow: Where Data Comes From

A direct data flow is the simplest type of relationship: data from a source object is moved directly into a target object.

For example, consider this query:

```sql
SELECT p.FirstName
FROM Person.Person AS p 
```

Here, the data from the `FirstName` column in the `Person.Person` table flows directly into a new `FirstName` column in the result of the query. SQLFlow represents this as:

`Person.Person.FirstName -> direct -> Result.FirstName`

In a diagram, a solid arrow represents this direct flow:
![Direct data flow](https://images.gitee.com/uploads/images/2021/1204/202053_bfe8900f_8136809.png)

This is the most common and fundamental type of lineage. In the technical SQLFlow output, this relationship is often called **`fdd`** (short for data flow dependency).

### 2. Indirect Data Flow: What Influences the Data

Sometimes, a column can influence the outcome of a query without its data being directly copied. This is called an indirect data flow or an "impact" relationship.

A dotted line arrow is used to represent an indirect dataflow in the diagram:

![Indirect data flow](https://images.gitee.com/uploads/images/2021/1204/202348_3a9d1e71_8136809.png)

Common places where you see indirect flows are:

*   `WHERE` clauses
*   `GROUP BY` clauses
*   `JOIN` conditions
*   Window functions (`OVER (...)`)

**Example: `WHERE` clause**

```sql
SELECT a.empName
FROM scott.emp a
WHERE sal > 1000
```

In this case, the `sal` column doesn't appear in the output. However, its value *filters* the rows, impacting which `empName` values are returned. SQLFlow captures this relationship to show that `sal` has an effect on the result.

![fdr relationship diagram](https://images.gitee.com/uploads/images/2021/0711/184450_e112148b_8136809.png)

**Example: `GROUP BY` clause**

```sql
SELECT deptno, COUNT(*) AS num_emp, SUM(SAL) AS sal_sum
FROM scott.emp
GROUP BY deptno
```

Here, the `deptno` column is used to group the rows. This means the values of `COUNT(*)` and `SUM(SAL)` are calculated for each department. Therefore, `deptno` indirectly impacts both of the aggregated columns.

SQLFlow would create relationships showing that `scott.emp.deptno` impacts both `num_emp` and `sal_sum`.

![Indirect dataflow in GROUP BY](https://images.gitee.com/uploads/images/2021/1206/174012_ba0c83f4_8136809.png)

In the technical SQLFlow output, this relationship is called **`fdr`** (short for data restriction/impact).

### 3. Join Relationships

SQLFlow also identifies relationships created by `JOIN` conditions. While not strictly a data flow, it's a critical relationship for understanding how tables are connected in a query.

```sql
SELECT b.teur
FROM tbl a 
LEFT JOIN TT b ON (a.key = b.key)
```

SQLFlow will create a `join` relationship between `tbl.key` and `TT.key`, showing they are linked in the query.

![Join relationship](https://images.gitee.com/uploads/images/2021/0711/185405_036c2a1a_8136809.png)

## Putting It All Together: A Complex Example

By combining these different relationship types, SQLFlow can analyze complex queries and build a complete data lineage graph.

Consider this `CREATE VIEW` statement which calculates the percentage of employees and salary for each department:

```sql
CREATE VIEW vsal 
AS 
  SELECT a.deptno                  "Department", 
         a.num_emp / b.total_count "Employees", 
         a.sal_sum / b.total_sal   "Salary" 
  FROM   (SELECT deptno, 
                 Count()  num_emp, 
                 SUM(sal) sal_sum 
          FROM   scott.emp 
          WHERE  city = 'NYC' 
          GROUP  BY deptno) a, 
         (SELECT Count()  total_count, 
                 SUM(sal) total_sal 
          FROM   scott.emp 
          WHERE  city = 'NYC') b 
```

Even in this complex query with subqueries and calculations, SQLFlow can trace every column back to its ultimate source, showing both direct and indirect relationships.

The resulting data lineage diagram provides a clear visual map of the entire flow:

![Complex data lineage diagram](https://images.gitee.com/uploads/images/2021/0711/221337_e8f731a5_8136809.png)

The output is also available in a structured format like JSON or XML, which allows for further analysis and integration with other tools.

## References

1. The lineage model is generated by the [DataFlowAnalyzer](https://github.com/sqlparser/gsp_demo_java/tree/master/src/main/java/demos/dlineage) tool.
2. Diagrams used in this article are generated by the [Gudu SQLFlow Cloud version](https://sqlflow.gudusoft.com/).

## A Look Ahead: The Next Generation of SQLFlow's Lineage Model

To provide even more powerful and precise data lineage, SQLFlow's data model is evolving. While the core concepts you've learned here remain the foundation, the new model (currently under development) introduces a more structured and detailed way of representing lineage. This gives you deeper insights, especially in complex, enterprise-scale environments.

Here’s a preview of the key improvements and how the concepts map to the new design.

### Key Improvements and Concept Mapping

The new model focuses on being more explicit, traceable, and scalable.

| Current Concept (v1) | New Concept (v2 Preview) | Improvement |
| :--- | :--- | :--- |
| Direct Flow (`fdd`) | `data_flow` Relationship | A clearer, more descriptive name for the same core concept. |
| Indirect Flow (`fdr`) | `restricts` & `groups` Relationships | Instead of a single "impact" type, the new model specifies *how* data is impacted. `restricts` is used for filtering (e.g., `WHERE` clauses), and `groups` is for aggregation (`GROUP BY` clauses). |
| Data Objects | `lineageObjects` | A more robust definition for objects, including a unique `qualifiedName` (e.g., `server.database.schema.table.column`) that prevents confusion between objects with the same name in different systems. |
| Relationships | `relationships` with `observations` | Relationships are simplified to be "atomic" (one source to one target). The new `observations` feature provides detailed "evidence" for each relationship, linking it to the exact file and line of code that created it. |
| N/A | Transformation Details (`transforms`) | The new model explicitly captures the transformation logic within the relationship itself. You can see the exact expression or function (e.g., `SUM(amount)`) that converted the source to the target. |


### Example: A More Precise `GROUP BY`

Let's revisit the `GROUP BY` example:

```sql
SELECT deptno, SUM(SAL) AS sal_sum
FROM scott.emp
GROUP BY deptno
```

- In the **current model**, this is captured with two relationships:
    1.  A direct data flow (`fdd`) relationship from `scott.emp.SAL` to `sal_sum`.
    2.  An indirect flow (`fdr`) relationship from `scott.emp.deptno` to `sal_sum`.
    This tells us `sal_sum` is derived from `SAL` and influenced by `deptno`, but the generic `fdr` relationship doesn't specify *how* `deptno` creates the impact.

- In the **new model**, this is broken down into two more precise relationships:
    1.  A `data_flow` relationship from `scott.emp.SAL` to `sal_sum`, which includes a `transform` showing the `SUM()` function was used and an `effectType` of `AGGREGATION` to clarify the nature of the transformation.
    2.  A `groups` relationship from `scott.emp.deptno` to `sal_sum`, clearly stating that `deptno` provides the grouping for the aggregation.

This level of detail makes it much easier to understand the exact logic without having to go back to the original SQL.

### Enhanced Traceability and Auditability

Perhaps the biggest improvement is the ability to trace any lineage relationship back to its origin with complete confidence. The new model introduces **`processes`** (the scripts or jobs that were analyzed) and **`observations`**.

Think of it this way: a single logical relationship (e.g., `column A` flows to `column B`) might be created by several different ETL scripts across your organization. The new model captures this by creating one logical `relationship` and attaching multiple `observations` to it—one for each script that creates the flow. Each observation acts as a piece of evidence, complete with file names and line numbers, giving you a full audit trail of your data's lineage.
