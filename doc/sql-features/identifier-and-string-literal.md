## Identifier（标识符） and String literal（字符串常量）

关于 Identifier（标识符） and String literal（字符串常量）详细介绍见：
https://www.dpriver.com/blog/2023/12/mastering-sql-syntax-a-comprehensive-guide-for-2024-and-beyond/

TODO: add String literal section in this article.

这篇文章讨论一些具体问题。

## SQLServer

### 常见的 Identifier 和 String literal 形式
#### Identifier
- name
- [my name]
- "this is my name"

#### String literal
- 'name'


### Column in select list
```sql
 select name,[name],"name",'name', age from dbo.person
```
上面这个语句中的 name,[name],"name" 都是 identifier, 而 'name' 为 string literal。

看下面的输出，identifier 会返回数据库表中对应字段的值，但 string literal 返回该字符串本身：
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
select p.[third name] from (select name name, name "first name", name [second name], name 'third name'  from dbo.person) p
```
**上面的这个 SQL 说明，subquery 中的 name 'third name' 和 外部的 p.[third name] 是指同一个 column，因此我们在比较时，仅比较 `third name`, 外面的 ' 和 [] 符号都需要去掉**。

```sql
-- 语法错误
select p.'third name' from (select name name, name "first name", name [second name], name 'third name'  from dbo.person) p
```

### 测试用的脚本
```sql
use master
create table dbo.person(name varchar(100), age int );
insert into dbo.person(name,age) values('Tom',11),('Alice',12);
create table dbo.student(sname varchar(100), sage int );
insert into dbo.student(sname,sage) values('sTom',21),('sAlice',22);
```

## mysql

#### Identifier

- name
- \`name\`

#### String literal

- 'name'
- "name"

### Column in select list：

```sql
select name,`name`,"name",'name' from dbo.person
```

上面这个语句中的 name,\`name\` 都是 identifier, 而 'name',"name" 为 string literal。

### Table alias

创建 table alias 时，Identifier 可以作为 table alias，但 string constant 不行，**且Identifier类型 无需保持一致**

```sql
-- 语法正确
select name, \`ps\`.age from dbo.person ps
select name, ps.age from dbo.person \`ps\`
```

```sql
-- 语法错误
select name, age from dbo.person 'ps'
select name, age from dbo.person "ps"
```

### Column alias

在创建 column alias 时，Identifier 和 string constant 都可以作为 column alias

```sql
-- 语法正确
select name name, name "first name", name 'second name',  name \`third name\` from dbo.person
```

但在引用 column alias 时，仅能使用 identifier， 不能使用 string constant。**且Identifier 类型无需保持一致**

```sql
-- 语法正确
SELECT renta.staff FROM (SELECT rental_id "staff" FROM rental) `renta`
```


## Oracle

#### Identifier

- name
- "name"

#### String literal

- 'name'

### Column in select list：

```sql
select name,"name",'name' from dbo.person
```

上面这个语句中的 name,"name" 都是 identifier, 而 'name', 为 string literal。

### Table alias

创建 table alias 时，Identifier 可以作为 table alias，但 string constant 不行, **且Identifier类型 需要保持一致，不可混用**

```sql
-- 语法正确
select name, ps.age from dbo.person ps
select name, "ps".age from dbo.person "ps"
```

```sql
-- Identifier 语法错误
select name, "ps".age from dbo.person ps
select name, ps.age from dbo.person "ps"
select name, 'ps'.age from dbo.person 'ps'
```

### Column alias

在创建 column alias 时，Identifier 作为 column alias,但 string constant 不行

```sql
-- 语法正确
select name name, name "first name" from dbo.person
```

在创建 column alias 时，Identifier 作为 column alias,但 string constant 不行

```sql
-- 语法错误
select name 'name' from dbo.person
```

但在引用 column alias 时，仅能使用 identifier， 不能使用 string constant。**且Identifier 类型无需保持一致**

```sql
-- 语法正确
SELECT "P".REGION_ID2 FROM (SELECT REGION_ID "REGION_ID2" FROM REGIONS )P 
```





## PostgreSQL

#### Identifier

- name
- "name"

#### String literal

- 'name'

### Column in select list：

```sql
select name,"name",'name' from dbo.person
```

上面这个语句中的 name,"name" 都是 identifier, 而 'name', 为 string literal。identifier和string literal都支持。

### Table alias

创建 table alias 时，Identifier 可以作为 table alias，但 string constant 不行,**且Identifier类型 无需保持一致**

```sql
-- 语法正确
select name, "ps".age from dbo.person ps
select name, ps.age from dbo.person "ps"
```

```sql
-- Identifier 语法错误
select name, 'ps'.age from dbo.person ps
```

### Column alias

在创建 column alias 时，Identifier 作为 column alias,但 string constant 不行

```sql
-- 语法正确
select name name, name "first name" from dbo.person
```

在创建 column alias 时，Identifier 作为 column alias,但 string constant 不行

```sql
-- 语法错误
select name 'name' from dbo.person
```

但在引用 column alias 时，仅能使用 identifier， 不能使用 string constant。**且Identifier类型 需要保持一致，不可混用**

```sql
-- 语法正确
SELECT "P".REGION_ID2 FROM (SELECT column1 REGION_ID2 FROM newtable_1 ) "P" 
select P."REGION_ID2" FROM (SELECT column1 "REGION_ID2" FROM newtable_1 ) P 
```

```sql
-- 语法错误
SELECT "P".REGION_ID2 FROM (SELECT column1 REGION_ID2 FROM newtable_1 ) P 
select P."REGION_ID2" FROM (SELECT column1 REGION_ID2 FROM newtable_1 ) P 
```
