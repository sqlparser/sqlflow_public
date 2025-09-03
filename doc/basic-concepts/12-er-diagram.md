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

### 2. v2 modeling: structure vs. data flow

In v2, ER is modeled using 1→1 atomic edges with explicit types:

- `has`: table “has” column (table→column) for schema structure
- `restricts`: FK column restricts the referenced PK during joins or constraints

Minimal v2 structural edges:
```json
{ "type": "has", "sourceId": "Departments", "targetId": "Departments.department_id" }
```
```json
{ "type": "has", "sourceId": "Employees", "targetId": "Employees.department_id" }
```

Optional constraint influence (useful for impact analyses and when rendering
ER overlays on data-flow graphs):
```json
{
  "type": "restricts",
  "sourceId": "Employees.department_id",
  "targetId": "Departments.department_id",
  "processIds": ["ddl_proc"],
  "condition": "FK Employees.department_id REFERENCES Departments.department_id"
}
```

Notes:
- Keep ER (structure) separate from data movement. Use `has` for schema, and
  `data_flow` only for queries that actually move data.
- When a join uses this FK/PK, add join-time `restricts` edges (see Join doc).

### 3. Tips and v1→v2 mapping

- v1 `type="er"` → v2: emit `has` edges for table/column hierarchy; optionally
  add a `restricts` edge to capture FK enforcement.
- Use deterministic `qualifiedName` per v2 to merge ER from multiple files.
- UI: render ER separately or as an overlay; allow toggling constraint
  influences for clarity.

### 4. Why this matches industry practice

- ER is a structural view; lineage diagrams should not conflate ER with runtime
  data movement. Separating `has` (structure) from `data_flow`/`restricts`
  aligns with common tools and improves readability.
