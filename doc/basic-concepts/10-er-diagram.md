## ER diagrams and lineage

[toc]

### 1. ER basics and v1 representation

An Entity-Relationship (ER) diagram shows how tables relate, typically through
primary keys (PK) and foreign keys (FK). In v1 outputs, ER links are emitted as
`relationship type="er"` between the FK column (target) and the referenced PK
column (source).

Example DDL (Oracle):
```sql
-- Create the Departments table
CREATE TABLE Departments (
    department_id NUMBER PRIMARY KEY,
    department_name VARCHAR2(50) NOT NULL,
    location VARCHAR2(100)
);

-- Create the Employees table with a foreign key referencing Departments
CREATE TABLE Employees (
    employee_id NUMBER PRIMARY KEY,
    first_name VARCHAR2(50) NOT NULL,
    last_name VARCHAR2(50) NOT NULL,
    email VARCHAR2(100) UNIQUE,
    hire_date DATE,
    salary NUMBER(10,2),
    department_id NUMBER,
    CONSTRAINT fk_department
        FOREIGN KEY (department_id)
        REFERENCES Departments(department_id)
);
```

v1 ER extract:
```xml
<relationship id="2" type="er">
    <target id="18" column="department_id" parent_id="11" parent_name="Employees"/>
    <source id="5" column="department_id" parent_id="4" parent_name="Departments"/>
</relationship>
```

This captures the FK→PK structural link used by tools to render ER diagrams.

### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> PK and FK declarations are structural facts, not data movement. SLPC emits `Endpoint` records for both
> tables and fields, `ObjectRelationship(PRIMARY_KEY)` for each primary key, and one
> `ObjectRelationship(FOREIGN_KEY_REFERENCE)` with participants
> `FOREIGN_KEY_RELATION=Employees` and `REFERENCED_RELATION=Departments`. Its ordered `keyPairs` binds
> `Employees.department_id` to `Departments.department_id`. The DDL statement evidence is attached through
> an occurrence. No `VALUE` or `ROW` fact is emitted merely because the FK exists.

### 2. Structure and query-time lineage stay separate

- Table/field containment is part of endpoint structure and display, not a synthetic value edge.
- A declared FK remains an `ObjectRelationship` even if no query joins the tables.
- If a SQL statement later joins these fields, that statement independently creates `ROW + JOIN` facts and `JoinSemantics`.
- Legacy adapters that previously encoded FK as `fdd` must convert it to the structural relationship and report a compatibility correction; retaining the false VALUE fact is forbidden.
- Projectors may render ER as a separate diagram or overlay. If a target tool cannot represent PK/FK structure, its projection report must account for the loss.
