## Temporary table

This section is about how to handle the temporary table in the data lineage analysis.

Some user like to see the temporary table in the data lineage analysis, but some user don't like to see the temporary table in the data lineage analysis.

thus we provide an option `/withTemporaryTable` to let user decide whether to output the temporary table in the data lineage analysis.

Temporary table such as `#temp_table` in SQL Server will not be output in simple output by default.

If you want to output the temporary table, you can use `/withTemporaryTable` option.

```
/withTemporaryTable true
```

### Temporary table in different database

Different database products have different syntax for temporary table.

For example:

- In SQL Server, the temporary table is like `#temp_table`.
- In MySQL, The temporary table is like `tmp_table`.

