/**
 * LineageQuickstart.java
 *
 * Extract column-level data lineage in ~10 lines of Java using
 * General SQL Parser (GSP) by Gudu Software.
 *
 * This example:
 *   1. Parses an Oracle INSERT...SELECT statement
 *   2. Runs DataFlowAnalyzer to compute data lineage
 *   3. Iterates over every column-level relationship
 *   4. Prints source -> target column mappings
 *
 * Download GSP:  https://www.sqlparser.com
 * Javadoc:       https://www.sqlparser.com/gsp_javadoc.php
 */

import gudusoft.gsqlparser.EDbVendor;
import gudusoft.gsqlparser.dlineage.DataFlowAnalyzer;
import gudusoft.gsqlparser.dlineage.dataflow.model.xml.dataflow;
import gudusoft.gsqlparser.dlineage.dataflow.model.xml.relationship;
import gudusoft.gsqlparser.dlineage.dataflow.model.xml.sourceColumn;
import gudusoft.gsqlparser.dlineage.dataflow.model.xml.targetColumn;

import java.util.List;

public class LineageQuickstart {

    public static void main(String[] args) {

        // ----- Sample SQL: INSERT...SELECT with expressions -----
        String sql =
            "CREATE TABLE employees (\n" +
            "  emp_id   NUMBER,\n" +
            "  name     VARCHAR2(100),\n" +
            "  dept_id  NUMBER,\n" +
            "  salary   NUMBER\n" +
            ");\n" +
            "\n" +
            "CREATE TABLE departments (\n" +
            "  dept_id    NUMBER,\n" +
            "  dept_name  VARCHAR2(100)\n" +
            ");\n" +
            "\n" +
            "CREATE TABLE dept_salary_report (\n" +
            "  department_name  VARCHAR2(100),\n" +
            "  total_salary     NUMBER,\n" +
            "  head_count       NUMBER\n" +
            ");\n" +
            "\n" +
            "INSERT INTO dept_salary_report (department_name, total_salary, head_count)\n" +
            "SELECT d.dept_name,\n" +
            "       SUM(e.salary),\n" +
            "       COUNT(e.emp_id)\n" +
            "  FROM employees e\n" +
            "  JOIN departments d ON e.dept_id = d.dept_id\n" +
            " GROUP BY d.dept_name;\n";

        // ----- Step 1: Create the analyzer (parse + analyze in one shot) -----
        DataFlowAnalyzer analyzer = new DataFlowAnalyzer(sql, EDbVendor.dbvoracle, false);

        // ----- Step 2: Generate the data-flow graph -----
        analyzer.generateDataFlow();

        // ----- Step 3: Retrieve the dataflow model -----
        dataflow df = analyzer.getDataFlow();

        // ----- Step 4: Walk every relationship and print source -> target -----
        List<relationship> relations = df.getRelationships();
        if (relations == null || relations.isEmpty()) {
            System.out.println("No lineage relationships found.");
            return;
        }

        System.out.println("=== Column-Level Lineage ===\n");
        for (relationship rel : relations) {
            targetColumn target = rel.getTarget();
            String targetLabel = target.getParent_name() + "." + target.getColumn();

            for (sourceColumn src : rel.getSources()) {
                String sourceLabel = src.getParent_name() + "." + src.getColumn();
                System.out.printf("  %-40s  -->  %s%n", sourceLabel, targetLabel);
            }
        }
        System.out.println("\nDone. " + relations.size() + " relationship(s) found.");
    }
}
