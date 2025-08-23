## Gudu SQLFlow Documents

1. Start with [SQLFlow Cloud](https://sqlflow.gudusoft.com/) - A web-based tool that visualizes data lineage diagrams from your SQL queries. This helps you understand how data flows and transforms between different tables and columns in your database.

2. Try the [DLineage Command Line Tool](https://github.com/sqlparser/gsp_demo_java/releases) to generate data lineage in XML/JSON format. This will help you understand the structured representation of data lineage and familiarize yourself with the key elements and attributes used.

3. Learn the fundamental concepts and components of data lineage by reviewing our basic concepts documentation. This covers important topics like direct/indirect dataflows, transforms, and relationships between database objects.

4. Explore the detailed data lineage model reference to gain a deeper technical understanding of how SQLFlow represents and tracks data lineage information.

5. When you're ready to integrate data lineage into your own applications, use our REST API, Java API, or JavaScript Widget. These integration options let you programmatically generate and visualize data lineage using your preferred development approach.


### Concepts
- [1. Introduction](basic-concepts/1-introduction.md)
- [2. Direct dataflow](basic-concepts/2-direct-dataflow.md)
- [3. Indirect dataflow and pseudo column](basic-concepts/3-indirect-dataflow-and-pseudo-column.md)
- [4. Indirect dataflow: where clause and group by clause](basic-concepts/4-indirect-dataflow-where-group-by.md)
- [5. Dataflow: column used in aggregate function](basic-concepts/5-dataflow-column-used-in-aggregate-function.md)
- [6. Dataflow chain](basic-concepts/6-dataflow-chain.md)
- [7. Intermediate result set](basic-concepts/7-intermediate-resultset.md)
- [8. Join relation](basic-concepts/8-join-relation.md)
- [9. Temporary table](basic-concepts/9-temporary-table.md)
- [10. Transforms](basic-concepts/10-transforms.md)


### Data lineage model (TODO)
- [1. Introduction](data-lineage-model/readme.md)
- [2. Detailed reference](data-lineage-model/data-lineage-model-reference.md)

### The structure and elements of the data lineage result(JSON/XML).
- [1. Introduction](data-lineage-format/readme.md)
- [2. Detailed reference](data-lineage-format/data-lineage-format-reference.md)

### SQLFlow widget

The SQLFlow widget is a Javascript library that enables instantaneous data lineage visualisation on your website.

- [Introduction](../widget/doc/readme.md)