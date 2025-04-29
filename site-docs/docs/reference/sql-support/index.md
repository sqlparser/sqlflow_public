# SQL Syntax Support

This section documents the SQL syntax support for different database systems in GSP. The information is automatically generated from test cases and provides a comprehensive overview of which SQL features are supported for each database.

## Supported Databases

GSP provides parsing support for the following database systems:

- [Oracle](oracle.md)
- [MySQL](mysql.md)
- [PostgreSQL](postgresql.md)
- [SQL Server](sqlserver.md)
- [DB2](db2.md)
- [Snowflake](snowflake.md)
- [Redshift](redshift.md)
- [Teradata](teradata.md)

## Support Matrix

Below is a high-level overview of SQL feature support across different database systems:

| Feature | Oracle | MySQL | PostgreSQL | SQL Server | DB2 | Snowflake | Redshift | Teradata |
|---------|:------:|:-----:|:----------:|:----------:|:---:|:---------:|:--------:|:--------:|
| SELECT  | ✅     | ✅    | ✅         | ✅         | ✅  | ✅        | ✅       | ✅       |
| INSERT  | ✅     | ✅    | ✅         | ✅         | ✅  | ✅        | ✅       | ✅       |
| UPDATE  | ✅     | ✅    | ✅         | ✅         | ✅  | ✅        | ✅       | ✅       |
| DELETE  | ✅     | ✅    | ✅         | ✅         | ✅  | ✅        | ✅       | ✅       |
| CREATE TABLE | ✅ | ✅    | ✅         | ✅         | ✅  | ✅        | ✅       | ✅       |
| ALTER TABLE  | ✅ | ✅    | ✅         | ✅         | ✅  | ✅        | ✅       | ✅       |
| DROP TABLE   | ✅ | ✅    | ✅         | ✅         | ✅  | ✅        | ✅       | ✅       |
| CREATE INDEX | ✅ | ✅    | ✅         | ✅         | ✅  | ❌        | ✅       | ✅       |
| CREATE VIEW  | ✅ | ✅    | ✅         | ✅         | ✅  | ✅        | ✅       | ✅       |
| WITH (CTE)   | ✅ | ✅    | ✅         | ✅         | ✅  | ✅        | ✅       | ✅       |
| MERGE        | ✅ | ❌    | ✅         | ✅         | ✅  | ✅        | ❌       | ✅       |
| WINDOW Functions | ✅ | ✅ | ✅         | ✅         | ✅  | ✅        | ✅       | ✅       |

## How to Read This Documentation

For each database, detailed support information is provided including:

1. **SQL Statement Types** - Which statements are supported (SELECT, INSERT, CREATE, etc.)
2. **Clauses and Operators** - Support for specific SQL clauses and operators
3. **Functions** - Built-in functions supported by the parser
4. **Data Types** - Supported data types
5. **Special Features** - Database-specific features and syntax

## Test Coverage

This documentation is automatically generated from our test suite, which ensures that all documented features are actually supported and tested. For each feature, the documentation includes:

- Feature name
- Support status
- Example SQL syntax
- Any limitations or notes

For details about a specific database's SQL syntax support, click on the corresponding link above. 