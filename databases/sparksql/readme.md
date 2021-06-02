## SparkSQL column-level data lineage

Discover and visualization lineage from SparkSQL script.
SQLFlow supports alls SQL statements of SparkSQL 3. Below are some examples that
illustrate how SQLFlow works. You may try your SparkSQL query to get the lineage
using the [SQLFlow Cloud](https://sqlflow.gudusoft.com).

### INSERT OVERWRITE DIRECTORY
```sql
INSERT OVERWRITE DIRECTORY 's3:///bucket/path/to/report'
    USING parquet
    OPTIONS (col1 1, col2 'sum')
    SELECT bar.my_flag,sum(foo.amount) as amount_sum 
	FROM mydb.foo foo 
	left join mydb.bar bar
	on foo.bar_fk = bar.pk
	group by bar.my_flag;
```

The lineage diagram:

[![sparksql insert overwrite directory](/images/sparksql-insert-overwrite-directory.png)](https://sqlflow.gudusoft.com)


### Pivot clause
```sql
CREATE TABLE person (id INT, name STRING, age INT, class INT, address STRING);

SELECT * FROM person
    PIVOT (
        SUM(age) AS a, AVG(class) AS c
        FOR name IN ('John' AS john, 'Mike' AS mike)
    );
```

The lineage diagram:

[![sparksql pivot clause](/images/sparksql-pivot-clause.png)](https://sqlflow.gudusoft.com)


### [Try you SparkSQL using the SQLFlow Cloud Version](https://sqlflow.gudusoft.com)

### Programmatically using [Restful APIs](/api) or [SDKs](https://www.gudusoft.com/sqlflow-java-library-2/) to get lineage in CSV, JSON, Graphml format.

### SparkSQL sapmle SQLs for reference
```sql
INSERT OVERWRITE DIRECTORY 's3:///bucket/path/to/report'
    USING parquet
    OPTIONS (col1 1, col2 'sum')
    SELECT bar.my_flag,sum(foo.amount) as amount_sum 
	FROM mydb.foo foo 
	left join mydb.bar bar
	on foo.bar_fk = bar.pk
	group by bar.my_flag;

INSERT OVERWRITE DIRECTORY
    USING parquet
    OPTIONS ('path' 's3:///bucket/path/to/report', col1 1, col2 'sum')
    SELECT bar.my_flag,sum(foo.amount) as amount_sum 
	FROM mydb.foo foo 
	left join mydb.bar bar
	on foo.bar_fk = bar.pk
	group by bar.my_flag;


create schema mydb;

create table mydb.bar(
	pk int,
	my_flag int
);
	

create table mydb.foo(
	bar_fk int,
	amount int
);

insert into mydb.bar(pk,my_flag) values(1, 100);
insert into mydb.bar(pk,my_flag) values(2, 200);
insert into mydb.bar(pk,my_flag) values(3, 300);
insert into mydb.bar(pk,my_flag) values(4, 400);
insert into mydb.foo(bar_fk,amount) values(1, 10);
insert into mydb.foo(bar_fk,amount) values(1, 20);
insert into mydb.foo(bar_fk,amount) values(2, 200);
insert into mydb.foo(bar_fk,amount) values(2, 300);
insert into mydb.foo(bar_fk,amount) values(3, 250);
insert into mydb.foo(bar_fk,amount) values(4, 350);


SELECT bar.my_flag,sum(foo.amount) as amount_sum 
FROM mydb.foo foo 
left join mydb.bar bar
on foo.bar_fk = bar.pk
group by bar.my_flag
;
```