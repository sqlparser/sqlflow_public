In order to meet the user's various requirements about data lineage analysis, it is necessary to divide the SQLFlow data lineage model into several levels, each fitting a specific requirement.

## 1. The complete data lineage model

In this model, SQLFlow generates the data lineage includes all detailed information such as the RESULT SET generated during a SELECT statement, FUNCTION CALL used to calculate the new column value based on the input column, CASE EXPRESSION used to transform the data from one column to another, and so on.

This complete lineage model is the base of all other higher level lineage models which only includes some lineages in this complete model by omitting or aggregating some relations and entities in this model.

The higher level model is not only remove some relations and entities but also merge some relations to create a new relation. The most important entity introduced in the higher level model is PROCESS which is a SQL query/statement that do the transformation. The higher level model use the SQL query as the smallest unit to tells you how the data is transffered from one table/column to the other. On the other hand, the complete model tells you how data is transferred inside a SQL query.

When analyzing data lineage, the complete model is always generated since all other higher level models are based on this model. However, the complete model is not suitable to present to the user in a diagram if it includes too many entities and relations. The reason is:

1. Diagram includes thousands of entities and relations is a chaos and almost impossible to navigate in a single picture.
2. It's time comsuing and maybe impossible for the SQLFlow to layout the complete model with thousands of realtions.

The complete model is good when analyzing the SQL query or stored procedure less than 1000 thousands code lines. In this model, you can see all detailed information you need. For project includes thousands of stored procedures, It is much better to use the higher level model to visualize the dataflow for a specific table/column.

## 2. The column-level lineage model

As it name implied, this model traces the dataflow from column to column based on the SQL statement. In other words, from this model, you can see what SQL statement is used to move/impact data from one column to the other.

This model only includes 3 kinds of entity: the source column, the target column and the SQL statement( we call it PROCESS in the model) and the relation among them.

If you want to see how data is moved/impacted inside the SQL statement, you can use the complete model of this SQL statement to find more.

## 3. The table-level lineage model

As it name implied, this model traces the dataflow from table totable based on the SQL statement. In other words, from this model, you can see what SQL statement is used to move/impact data from onetable to the other.

This model only includes 3 kinds of entity: the source table, the target table and the SQL statement( we call it PROCESS in the model) and the relation among them.

If you want to see how data is moved inside the SQL statement, you can use the complete model of this SQL statement to find more.

## 4. SQLFlow UI

![image.png](https://images.gitee.com/uploads/images/2021/0707/145133_6f1ed32d_8136809.png)
