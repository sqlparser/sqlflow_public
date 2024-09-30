## Intermediate result set

### 1. What is intermediate result set?

In the SQLFlow, intermediate result set is the result set of a select statement.

For example:

```sql
CREATE VIEW v1 AS
SELECT EmployeeID, FirstName, LastName, ManagerID, EmpLevel  -- resultset1
FROM Employees
WHERE ManagerID IS NULL
```

The intermediate result set is:

```
EmployeeID, FirstName, LastName, ManagerID, EmpLevel
```
in the select list and shown in the data flow graph as below:

![intermediate-resultset](../../assets/images/get-started-intermediate-resultset1.png)

### CTE example:

CTE will be treated as a intermediate result set.
```sql
CREATE VIEW V1 AS
WITH
  cteReports (EmpID, FirstName, LastName, MgrID, EmpLevel)
  AS
  (
    SELECT EmployeeID, FirstName, LastName, ManagerID, EmpLevel  -- resultset1
    FROM Employees
    WHERE ManagerID IS NULL
  )
SELECT
  count(EmpID), sum(EmpLevel)  -- resultset2
FROM cteReports 
```
So, there are there intermediate result sets:

1. resultset1: EmployeeID, FirstName, LastName, ManagerID, EmpLevel
2. cte: cteReports (EmpID, FirstName, LastName, MgrID, EmpLevel) 
3. resultset3: count(EmpID), sum(EmpLevel)

And the data flow graph is like this:

![intermediate-resultset](../../assets/images/get-started-intermediate-resultset2.png)




### 2. How to use intermediate result set?

In the SQLFlow, intermediate result is used to show the details of the data flow and let you know ex

For example:

```sql

