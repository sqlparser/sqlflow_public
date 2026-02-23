# Getting Started with GSP

This guide will help you get started with GSP by walking through installation, basic setup, and simple examples.

## Installation

GSP can be added to your Java project using Maven or Gradle.

### Maven

Add the following dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.example</groupId>
    <artifactId>gsp</artifactId>
    <version>1.0.0</version>
</dependency>
```

### Gradle

Add the following to your `build.gradle`:

```gradle
dependencies {
    implementation 'com.example:gsp:1.0.0'
}
```

## Basic Usage

### Parsing SQL

Here's a simple example of parsing a SQL statement:

```java
import com.example.gsp.parser.SQLParser;
import com.example.gsp.model.SQLStatement;

public class Example {
    public static void main(String[] args) {
        // Create a parser for the specific database vendor
        SQLParser parser = SQLParser.createParser("mysql");
        
        // Parse SQL statement
        String sql = "SELECT id, name FROM employees WHERE department = 'Engineering'";
        SQLStatement statement = parser.parse(sql);
        
        // Now you can analyze or manipulate the statement
        System.out.println("SQL type: " + statement.getType());
        
        // Get tables referenced in the query
        List<String> tables = statement.getTables();
        System.out.println("Tables: " + String.join(", ", tables));
    }
}
```

### Handling Multiple Database Dialects

GSP supports multiple database dialects. You can specify the database type when creating a parser:

```java
// For MySQL
SQLParser mysqlParser = SQLParser.createParser("mysql");

// For Oracle
SQLParser oracleParser = SQLParser.createParser("oracle");

// For PostgreSQL
SQLParser postgresParser = SQLParser.createParser("postgresql");
```

## Advanced Features

For more advanced usage and features, see:

- [SQL Analysis Guide](advanced-sql-analysis.md)
- [Schema Extraction](schema-extraction.md)
- [Query Transformation](query-transformation.md)

## Troubleshooting

If you encounter issues while using GSP, check the following:

- Ensure you're using the correct database dialect for your SQL statements
- Validate that your SQL syntax is correct for the specified database
- Check for version compatibility issues

If problems persist, refer to the [Troubleshooting Guide](troubleshooting.md) or create an issue in our GitHub repository. 