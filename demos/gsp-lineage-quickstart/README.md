# Extract Column-Level Lineage in 10 Lines of Java

A minimal quickstart showing how to use **General SQL Parser (GSP)** to extract
column-level data lineage from a SQL statement.

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Java        | 8+      |
| GSP JAR     | 3.x     |

Download `gudusoft.gsqlparser.jar` from <https://www.sqlparser.com>.

## Maven / Gradle dependency

GSP is distributed as a local JAR.  Install it into your local Maven repo first:

```bash
mvn install:install-file \
  -Dfile=gudusoft.gsqlparser.jar \
  -DgroupId=gudusoft.gsqlparser \
  -DartifactId=gsqlparser \
  -Dversion=3.1.0 \
  -Dpackaging=jar
```

Then add the dependency:

```xml
<dependency>
    <groupId>gudusoft.gsqlparser</groupId>
    <artifactId>gsqlparser</artifactId>
    <version>3.1.0</version>
</dependency>
```

## Quick run (no build tool)

```bash
# Compile
javac -cp gudusoft.gsqlparser.jar LineageQuickstart.java

# Run
java -cp .:gudusoft.gsqlparser.jar LineageQuickstart
```

## What the code does

1. **Define SQL** -- An `INSERT INTO ... SELECT` that joins `employees` with
   `departments` and aggregates salary data into `dept_salary_report`.

2. **Create `DataFlowAnalyzer`** -- Pass the SQL string, the database vendor
   (`EDbVendor.dbvoracle`), and a `simpleOutput` flag.

3. **`generateDataFlow()`** -- Parses the SQL, resolves column references, and
   builds the internal lineage graph.

4. **`getDataFlow()`** -- Returns the `dataflow` model containing tables, views,
   result sets, and relationships.

5. **Iterate `getRelationships()`** -- Each `relationship` has a `targetColumn`
   and a list of `sourceColumn` objects.  Print them as
   `source_table.column --> target_table.column`.

## Expected output

```
=== Column-Level Lineage ===

  departments.dept_name                     -->  dept_salary_report.department_name
  employees.salary                          -->  dept_salary_report.total_salary
  employees.emp_id                          -->  dept_salary_report.head_count

Done. 3 relationship(s) found.
```

Each line shows which source column feeds into which target column, even through
aggregate functions like `SUM()` and `COUNT()`.

## Supported databases

GSP supports 20+ SQL dialects including Oracle, MySQL, SQL Server, PostgreSQL,
Snowflake, BigQuery, Hive, Redshift, Teradata, DB2, and more.  Change
`EDbVendor.dbvoracle` to match your dialect.

## Next steps

- **Simplify output**: Call `analyzer.setShowResultSetTypes(...)` to filter
  intermediate result sets.
- **JSON output**: Use `analyzer.getDataFlowJSON()` for machine-readable lineage.
- **File/directory mode**: Pass a `File` object instead of a SQL string to
  analyze `.sql` files or entire directories.
- **Metadata environment**: Use `analyzer.setSqlEnv(...)` to supply external
  schema metadata for more accurate lineage.

## Resources

- GSP download: <https://www.sqlparser.com>
- GSP Javadoc: <https://www.sqlparser.com/gsp_javadoc.php>
- SQLFlow (visual lineage): <https://sqlflow.gudusoft.com>
- GitHub demos: <https://github.com/nicknguyen-gudu/sqlflow_public>
