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
