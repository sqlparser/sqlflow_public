## Gudu SQLFlow Documents

Firstly, use [SQLFlow cloud](https://sqlflow.gudusoft.com/) to get the data lineage of your SQL and feel how the data lineage diagram can help you understand the data flow and the data transformation.

Secondly, use [Dlineage command line tool](https://github.com/sqlparser/gsp_demo_java/releases) to get the data lineage of your SQL in the XML/JSON format and see how the data lineage is organized in the JSON/XML format and start to know various elements and attributes in the data lineage.

Thirdly, check the basic concepts and elements of the data lineage.

Fourthly, check the detailed reference of the data lineage model.

Finally, integrate the SQLFlow Rest API/Java API/Widget into your project and get the data lineage of your SQL in the Rest API/Java/Python code/JavaScript code.


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
- [Introduction](widget/readme.md)