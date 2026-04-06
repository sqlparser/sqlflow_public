# SQL Parser Comparison 2026: GSP vs JSQLParser vs sqlglot

Test scripts used in the blog post: [GSP vs JSQLParser vs sqlglot — SQL Parser Comparison 2026](https://www.dpriver.com/blog/?p=3181)

## Test Setup

| Parser | Version | Language | License |
|--------|---------|----------|---------|
| [General SQL Parser](https://www.gudusoft.com) | 4.1.0.10 | Java | Commercial |
| [JSQLParser](https://github.com/JSQLParser/JSqlParser) | 5.3 | Java | Apache 2.0 |
| [sqlglot](https://github.com/tobymao/sqlglot) | 30.2.1 | Python | MIT |

All tests run on 2026-04-05 with OpenJDK 21 and Python 3.12.

## 14 Test Cases Across 6 SQL Dialects

| # | Test Case | Dialect | Complexity |
|---|-----------|---------|------------|
| 1 | CTE with JOIN | Standard | Basic |
| 2 | Window function (PARTITION BY) | Standard | Basic |
| 3 | Correlated subquery | Standard | Basic |
| 4 | CONNECT BY hierarchical query | Oracle | Vendor-specific |
| 5 | MODEL clause | Oracle | Vendor-specific |
| 6 | MERGE with LOG ERRORS | Oracle | Vendor-specific |
| 7 | CROSS APPLY | SQL Server | Vendor-specific |
| 8 | Stored procedure with TRY/CATCH | SQL Server | Stored procedure |
| 9 | PL/pgSQL function (RETURN QUERY) | PostgreSQL | Stored procedure |
| 10 | PL/SQL with BULK COLLECT/FORALL | Oracle | Stored procedure |
| 11 | UNNEST with STRUCT | BigQuery | Vendor-specific |
| 12 | Procedural DECLARE/IF | BigQuery | Stored procedure |
| 13 | LATERAL FLATTEN | Snowflake | Vendor-specific |
| 14 | QUALIFY | Snowflake | Vendor-specific |

## Results

| Test Case | GSP 4.1.0 | JSQLParser 5.3 | sqlglot 30.2 |
|-----------|:---------:|:--------------:|:------------:|
| Standard CTE with JOIN | PASS | PASS | PASS |
| Window function with PARTITION BY | PASS | PASS | PASS |
| Subquery in SELECT | PASS | PASS | PASS |
| Oracle CONNECT BY | PASS | PASS | PASS |
| Oracle MODEL clause | PASS | FAIL | FAIL |
| Oracle MERGE with error logging | PASS | FAIL | FAIL |
| T-SQL CROSS APPLY | PASS | PASS | PASS |
| T-SQL stored procedure (TRY/CATCH) | PASS | PASS | PASS* |
| PL/pgSQL RETURN QUERY function | PASS | PASS | PASS |
| Oracle PL/SQL BULK COLLECT | PASS | PASS | FAIL |
| BigQuery UNNEST with STRUCT | PASS | PASS | PASS |
| BigQuery procedural DECLARE/IF | PASS | FAIL | PASS |
| Snowflake FLATTEN | PASS | PASS | PASS |
| Snowflake QUALIFY | PASS | PASS | PASS |
| **Total** | **14/14** | **11/14** | **11/14** |

\*sqlglot fell back to parsing as a "Command" — it did not error, but lost structural understanding of TRY/CATCH, variable declarations, and control flow.

## How to Run

### sqlglot (Python)
```bash
pip install sqlglot
python3 test_sqlglot.py
```

### JSQLParser (Java)
```bash
# Download JSQLParser 5.3
curl -sL "https://repo1.maven.org/maven2/com/github/jsqlparser/jsqlparser/5.3/jsqlparser-5.3.jar" -o jsqlparser-5.3.jar
javac -cp jsqlparser-5.3.jar TestJSQLParser.java
java -cp .:jsqlparser-5.3.jar TestJSQLParser
```

### General SQL Parser (Java)
```bash
# Requires GSP JAR — download trial from https://www.gudusoft.com
javac -cp gsqlparser.jar TestGSP.java
java -cp .:gsqlparser.jar TestGSP
```

## Related

- [Gudu SQL Omni](https://marketplace.visualstudio.com/items?itemName=gudusoftware.gudu-sql-omni) — VS Code extension with column-level lineage, ER diagrams, and impact analysis (100% offline, 34 dialects)
- [SQLFlow](https://sqlflow.gudusoft.com) — Data lineage visualization platform
- [General SQL Parser](https://www.gudusoft.com) — Commercial SQL parsing library for Java
