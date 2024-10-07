```sql
-- oracle sample query
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

A relationship with type attribute value `er` will be generated in the ER diagram.

```xml
<relationship id="2" type="er">
    <target id="18" column="department_id" parent_id="11" parent_name="Employees"/>
    <source id="5" column="department_id" parent_id="4" parent_name="Departments"/>
</relationship>
```


