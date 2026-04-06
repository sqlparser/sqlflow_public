import net.sf.jsqlparser.parser.CCJSqlParserUtil;
import net.sf.jsqlparser.statement.Statement;
import net.sf.jsqlparser.statement.Statements;

public class TestJSQLParser {
    static int passed = 0;
    static int failed = 0;

    static void test(String name, String sql) {
        try {
            // Try single statement first
            Statement stmt = CCJSqlParserUtil.parse(sql);
            if (stmt != null) {
                System.out.println("  PASS: " + name);
                passed++;
            } else {
                System.out.println("  FAIL: " + name + " — parsed but returned null");
                failed++;
            }
        } catch (Exception e) {
            String msg = e.getMessage();
            if (msg != null && msg.length() > 120) msg = msg.substring(0, 120) + "...";
            System.out.println("  FAIL: " + name + " — " + msg);
            failed++;
        }
    }

    public static void main(String[] args) {
        System.out.println("JSQLParser 5.3\n");

        // Standard SQL
        test("Standard CTE with JOIN",
            "WITH cte AS (SELECT a.id, b.name FROM orders a JOIN customers b ON a.cust_id = b.id) SELECT id, name FROM cte WHERE id > 10");

        test("Window function with PARTITION BY",
            "SELECT id, name, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) as rn FROM employees");

        test("Subquery in SELECT",
            "SELECT e.name, (SELECT d.name FROM departments d WHERE d.id = e.dept_id) as dept_name FROM employees e");

        // Oracle
        test("Oracle CONNECT BY",
            "SELECT employee_id, manager_id, LEVEL FROM employees CONNECT BY PRIOR employee_id = manager_id START WITH manager_id IS NULL");

        test("Oracle MODEL clause",
            "SELECT country, product, year, sales FROM sales_data MODEL DIMENSION BY (country, product, year) MEASURES (amount AS sales) RULES (sales['US', 'Electronics', 2026] = sales['US', 'Electronics', 2025] * 1.1)");

        test("Oracle MERGE with error logging",
            "MERGE INTO target t USING source s ON (t.id = s.id) WHEN MATCHED THEN UPDATE SET t.val = s.val WHEN NOT MATCHED THEN INSERT (id, val) VALUES (s.id, s.val) LOG ERRORS INTO err_log REJECT LIMIT UNLIMITED");

        // SQL Server
        test("T-SQL CROSS APPLY",
            "SELECT d.name, e.name FROM departments d CROSS APPLY (SELECT TOP 3 name FROM employees WHERE dept_id = d.id ORDER BY salary DESC) e");

        test("T-SQL TRY/CATCH stored procedure",
            "CREATE PROCEDURE usp_TransferFunds @FromAcct INT, @ToAcct INT, @Amount DECIMAL(10,2)\n" +
            "AS BEGIN\n" +
            "    BEGIN TRY\n" +
            "        BEGIN TRANSACTION\n" +
            "        UPDATE accounts SET balance = balance - @Amount WHERE id = @FromAcct\n" +
            "        UPDATE accounts SET balance = balance + @Amount WHERE id = @ToAcct\n" +
            "        COMMIT TRANSACTION\n" +
            "    END TRY\n" +
            "    BEGIN CATCH\n" +
            "        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION\n" +
            "        DECLARE @ErrorMsg NVARCHAR(4000) = ERROR_MESSAGE()\n" +
            "        RAISERROR(@ErrorMsg, 16, 1)\n" +
            "    END CATCH\n" +
            "END");

        // PostgreSQL
        test("PL/pgSQL function with RETURN QUERY",
            "CREATE OR REPLACE FUNCTION get_dept_employees(p_dept_id INT)\n" +
            "RETURNS TABLE(emp_id INT, emp_name VARCHAR, emp_salary NUMERIC)\n" +
            "LANGUAGE plpgsql AS $$\n" +
            "BEGIN\n" +
            "    RETURN QUERY SELECT e.id, e.name, e.salary FROM employees e WHERE e.department_id = p_dept_id;\n" +
            "END;\n" +
            "$$");

        // Oracle PL/SQL
        test("Oracle PL/SQL with BULK COLLECT",
            "CREATE OR REPLACE PROCEDURE sync_customers IS\n" +
            "    TYPE t_cust IS TABLE OF customers%ROWTYPE;\n" +
            "    l_batch t_cust;\n" +
            "    CURSOR c_new IS SELECT * FROM staging_customers WHERE status = 'NEW';\n" +
            "BEGIN\n" +
            "    OPEN c_new;\n" +
            "    LOOP\n" +
            "        FETCH c_new BULK COLLECT INTO l_batch LIMIT 1000;\n" +
            "        EXIT WHEN l_batch.COUNT = 0;\n" +
            "        FORALL i IN 1..l_batch.COUNT\n" +
            "            MERGE INTO customers t USING (SELECT l_batch(i).id AS id FROM dual) s ON (t.id = s.id)\n" +
            "            WHEN MATCHED THEN UPDATE SET t.name = l_batch(i).name\n" +
            "            WHEN NOT MATCHED THEN INSERT (id, name) VALUES (l_batch(i).id, l_batch(i).name);\n" +
            "        COMMIT;\n" +
            "    END LOOP;\n" +
            "    CLOSE c_new;\n" +
            "EXCEPTION\n" +
            "    WHEN OTHERS THEN\n" +
            "        IF c_new%ISOPEN THEN CLOSE c_new; END IF;\n" +
            "        RAISE;\n" +
            "END sync_customers;");

        // BigQuery
        test("BigQuery UNNEST with STRUCT",
            "SELECT u.id, item.name, item.quantity FROM users u, UNNEST(u.order_items) AS item WHERE item.quantity > 5");

        test("BigQuery procedural DECLARE/IF",
            "DECLARE threshold INT64 DEFAULT 100;\n" +
            "DECLARE result STRING;\n" +
            "IF threshold > 50 THEN\n" +
            "    SET result = 'high';\n" +
            "ELSE\n" +
            "    SET result = 'low';\n" +
            "END IF;\n" +
            "SELECT result;");

        // Snowflake
        test("Snowflake FLATTEN",
            "SELECT d.id, f.value::STRING AS tag FROM documents d, LATERAL FLATTEN(input => d.metadata:tags) f");

        test("Snowflake QUALIFY",
            "SELECT id, name, dept, salary FROM employees QUALIFY ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) = 1");

        System.out.println("\n============================================================");
        System.out.println("JSQLParser 5.3: " + passed + " passed, " + failed + " failed out of " + (passed + failed));
        System.out.println("============================================================");
    }
}
