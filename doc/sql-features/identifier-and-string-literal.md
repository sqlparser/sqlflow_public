## Identifier（标识符） and String literal（字符串常量）

关于 Identifier（标识符） and String literal（字符串常量）详细介绍见：
https://www.dpriver.com/blog/2023/12/mastering-sql-syntax-a-comprehensive-guide-for-2024-and-beyond/

TODO: add String literal section in this article.

这篇文章讨论一些具体问题。

### 常用的 Identifier 和 String literal
#### Identifier
- name
- [my name]
- "this is my name"

#### String literal
- 'name'


```sql
use master
create table dbo.person(name varchar(100), age int );
insert into dbo.person(name,age) values('Tom',11),('Alice',12);
create table dbo.student(sname varchar(100), sage int );
insert into dbo.student(sname,sage) values('sTom',21),('sAlice',22);
```

### Column in select list
执行
```sql
 select name,[name],"name",'name', age from dbo.person
```
上面这个语句中的 name,[name],"name" 都是 identifier, 而 'name' 为 string literal。

看下面的输出就知道它们的区别：
![images](identifier-and-string-literal01.png)


### Table alias
创建 table alias 时，Identifier 可以作为 table alias，但 string constant 不行
```sql
-- 语法正确
select name, [ps].age from dbo.person "ps"
select name, "ps".age from dbo.person [ps]
```

```sql
-- 语法错误
select name, age from dbo.person 'ps'
```

### Column alias

在创建 column alias 时，Identifier 和 string constant 都可以作为 column alias，
```sql
-- 语法正确
select name name, name "first name", name "second name", name 'third name'  from dbo.person
```

但在引用 column alias 时，仅能使用 identifier， 不能使用 string constant。
```sql
-- 语法正确
select p."first name" from (select name name, name "first name", name [second name], name 'third name'  from dbo.person) p
```

```sql
-- 语法错误
select p.'third name' from (select name name, name "first name", name [second name], name 'third name'  from dbo.person) p
```

以上测试目前在 SQL Server 下通过，其他数据库还需要测试。