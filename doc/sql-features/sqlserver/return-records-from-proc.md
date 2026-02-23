以下 SQL Server 的 SQL 语句通过执行 INSERT INTO TestTable(Column1, Column2) EXEC dbo.testPro，会将存储过程 dbo.testPro 返回的结果集插入到表 TestTable 中。

```sql
CREATE TABLE [dbo].[NewTable] (
  [Column1] varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS  NULL,
  [Column2] varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS  NULL,
  [Column3] varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS  NULL
);

CREATE TABLE [dbo].[NewTable2] (
  [Column1] varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS  NULL,
  [Column2] varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS  NULL,
  [Column3] varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS  NULL
);

CREATE PROCEDURE dbo.testPro
AS
BEGIN
SELECT Column1, Column2 FROM NewTable;
SELECT Column1, Column2 FROM NewTable2;
end;

INSERT INTO TestTable(Column1, Column2) EXEC dbo.testPro;
```

存储过程 dbo.testPro 中有两个 SELECT 语句:
```sql
SELECT Column1, Column2 FROM NewTable;
SELECT Column1, Column2 FROM NewTable2;
```

因此，存储过程会返回 NewTable 和 NewTable2 两个表的 Column1 和 Column2 列的数据。这些数据会被插入到 TestTable 表的 Column1 和 Column2 列中。

SQL Server 的以上实现在其他数据库中不见得能正常工作，更通用的实现应该是：
```sql
CREATE PROCEDURE dbo.testPro
AS
BEGIN
    SELECT Column1, Column2 FROM NewTable
    union all
    SELECT Column1, Column2 FROM NewTable2;
end;
```