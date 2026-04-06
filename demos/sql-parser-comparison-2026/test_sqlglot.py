#!/usr/bin/env python3
"""Test sqlglot against challenging SQL and stored procedures."""
import sqlglot
import sys
import traceback

print(f"sqlglot version: {sqlglot.__version__}\n")

tests = [
    # --- Standard SQL ---
    ("Standard CTE with JOIN", "generic",
     "WITH cte AS (SELECT a.id, b.name FROM orders a JOIN customers b ON a.cust_id = b.id) SELECT id, name FROM cte WHERE id > 10"),

    ("Window function with PARTITION BY", "generic",
     "SELECT id, name, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) as rn FROM employees"),

    ("Subquery in SELECT", "generic",
     "SELECT e.name, (SELECT d.name FROM departments d WHERE d.id = e.dept_id) as dept_name FROM employees e"),

    # --- Oracle-specific ---
    ("Oracle CONNECT BY", "oracle",
     "SELECT employee_id, manager_id, LEVEL FROM employees CONNECT BY PRIOR employee_id = manager_id START WITH manager_id IS NULL"),

    ("Oracle MODEL clause", "oracle",
     "SELECT country, product, year, sales FROM sales_data MODEL DIMENSION BY (country, product, year) MEASURES (amount AS sales) RULES (sales['US', 'Electronics', 2026] = sales['US', 'Electronics', 2025] * 1.1)"),

    ("Oracle MERGE with error logging", "oracle",
     "MERGE INTO target t USING source s ON (t.id = s.id) WHEN MATCHED THEN UPDATE SET t.val = s.val WHEN NOT MATCHED THEN INSERT (id, val) VALUES (s.id, s.val) LOG ERRORS INTO err_log REJECT LIMIT UNLIMITED"),

    # --- SQL Server T-SQL ---
    ("T-SQL CROSS APPLY", "tsql",
     "SELECT d.name, e.name FROM departments d CROSS APPLY (SELECT TOP 3 name FROM employees WHERE dept_id = d.id ORDER BY salary DESC) e"),

    ("T-SQL TRY/CATCH stored procedure", "tsql",
     """CREATE PROCEDURE usp_TransferFunds @FromAcct INT, @ToAcct INT, @Amount DECIMAL(10,2)
AS BEGIN
    BEGIN TRY
        BEGIN TRANSACTION
        UPDATE accounts SET balance = balance - @Amount WHERE id = @FromAcct
        UPDATE accounts SET balance = balance + @Amount WHERE id = @ToAcct
        COMMIT TRANSACTION
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION
        DECLARE @ErrorMsg NVARCHAR(4000) = ERROR_MESSAGE()
        RAISERROR(@ErrorMsg, 16, 1)
    END CATCH
END"""),

    # --- PostgreSQL PL/pgSQL ---
    ("PL/pgSQL function with RETURN QUERY", "postgres",
     """CREATE OR REPLACE FUNCTION get_dept_employees(p_dept_id INT)
RETURNS TABLE(emp_id INT, emp_name VARCHAR, emp_salary NUMERIC)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
        SELECT e.id, e.name, e.salary
        FROM employees e
        WHERE e.department_id = p_dept_id
        ORDER BY e.salary DESC;
END;
$$"""),

    # --- Oracle PL/SQL ---
    ("Oracle PL/SQL package with BULK COLLECT", "oracle",
     """CREATE OR REPLACE PROCEDURE sync_customers IS
    TYPE t_cust IS TABLE OF customers%ROWTYPE;
    l_batch t_cust;
    CURSOR c_new IS SELECT * FROM staging_customers WHERE status = 'NEW';
BEGIN
    OPEN c_new;
    LOOP
        FETCH c_new BULK COLLECT INTO l_batch LIMIT 1000;
        EXIT WHEN l_batch.COUNT = 0;
        FORALL i IN 1..l_batch.COUNT
            MERGE INTO customers t
            USING (SELECT l_batch(i).id AS id, l_batch(i).name AS name FROM dual) s
            ON (t.id = s.id)
            WHEN MATCHED THEN UPDATE SET t.name = s.name
            WHEN NOT MATCHED THEN INSERT (id, name) VALUES (s.id, s.name);
        COMMIT;
    END LOOP;
    CLOSE c_new;
EXCEPTION
    WHEN OTHERS THEN
        IF c_new%ISOPEN THEN CLOSE c_new; END IF;
        RAISE;
END sync_customers;"""),

    # --- BigQuery ---
    ("BigQuery UNNEST with STRUCT", "bigquery",
     "SELECT u.id, item.name, item.quantity FROM users u, UNNEST(u.order_items) AS item WHERE item.quantity > 5"),

    ("BigQuery procedural DECLARE/IF", "bigquery",
     """DECLARE threshold INT64 DEFAULT 100;
DECLARE result STRING;
IF threshold > 50 THEN
    SET result = 'high';
ELSE
    SET result = 'low';
END IF;
SELECT result;"""),

    # --- Snowflake ---
    ("Snowflake FLATTEN", "snowflake",
     "SELECT d.id, f.value::STRING AS tag FROM documents d, LATERAL FLATTEN(input => d.metadata:tags) f"),

    ("Snowflake QUALIFY", "snowflake",
     "SELECT id, name, dept, salary FROM employees QUALIFY ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) = 1"),
]

passed = 0
failed = 0
errors = []

for name, dialect, sql in tests:
    try:
        result = sqlglot.parse(sql, read=dialect if dialect != "generic" else None)
        if result and all(r is not None for r in result):
            print(f"  PASS: {name} ({dialect})")
            passed += 1
        else:
            print(f"  FAIL: {name} ({dialect}) — parsed but returned None/empty")
            failed += 1
            errors.append((name, dialect, "Parsed but returned None"))
    except Exception as e:
        err_msg = str(e)[:150]
        print(f"  FAIL: {name} ({dialect}) — {err_msg}")
        failed += 1
        errors.append((name, dialect, err_msg))

print(f"\n{'='*60}")
print(f"sqlglot {sqlglot.__version__}: {passed} passed, {failed} failed out of {passed+failed}")
print(f"{'='*60}")
if errors:
    print("\nFailed tests:")
    for name, dialect, err in errors:
        print(f"  - {name} ({dialect}): {err}")
