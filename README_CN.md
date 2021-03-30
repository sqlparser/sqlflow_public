## 一、SQLFlow 是什么

数据库中视图(View)的数据来自表(Table)或其他视图，视图中字段(Column)的数据可能来自多个表中多个字段的聚集(aggregation)。
表中的数据可能通过ETL从外部系统中导入。这种从数据的源头经过各个处理环节，到达数据终点的数据链路关系称为数据血缘关系([data lineage](https://en.wikipedia.org/wiki/Data_lineage))。

[SQLFlow](https://sqlflow.gudusoft.com/) 通过分析各种数据库对象的定义(DDL)、DML 语句、ETL/ELT中使用的存储过程(Proceudre,Function)、
触发器(Trigger)和其他 SQL 脚本，给出完整的数据血缘关系。


在大型数据仓库中，完整的数据血缘关系可以用来进行数据溯源、表和字段变更的影响分析、数据合规性的证明、数据质量的检查等。

举例来说，可能会问财务报表中的统计结果，它是有哪些子系统（采购、生产、销售等）提供的数据汇总而成的？
当某个子系统（例如 销售子系统）的表和字段等数据结构发生变化时，可能会影响其它子系统吗？
财务报表子系统中的表和字段是否也需要进行相应的改动？

SQLFlow 会帮助你回答这些问题，以可视化的图形方式把这些关系呈现在你面前，让你对组织的IT系统中的数据流动一目了然。

![SQLFlow Introduce](images/sqlflow_introduce1.png)

## 二、SQLFlow 是怎样工作的

1. 从数据库、版本控制系统、文件系统中获取 SQL 脚本。
2. 解析 SQL 脚本，分析其中的各种数据库对象关系，建立数据血缘关系。
3. 以各种形式呈现数据血缘关系，包括交互式 UI、CSV、JSON、GRAPHML 格式。

## 三、SQLFlow 的组成

1. Backend， 后台由一系列 Java 程序组成。负责 SQL 的解析、数据血缘分析、可视化元素的布局、身份认证等。
2. Frontend，前端由一系列 javascript、html 代码组成。负责 SQL 的递交、数据血缘关系的可视化展示。
3. [Grabit 工具](https://www.gudusoft.com/grabit/)，一个 Java 程序。负责从数据库、版本控制系统、文件系统中收集 SQL 脚本，递交给后台进行数据血缘分析。
4. [Restful API](https://github.com/sqlparser/sqlflow_public/tree/master/api)，一套完整的 API。让用户可以通过 Java、C#、Python、PHP 等编程语言与后台进行交互，完成数据血缘分析。

![SQLFlow Components](https://github.com/sqlparser/sqlflow_public/raw/master/sqlflow_components.png)

## 四、SQLFlow的使用

1. 通过浏览器访问[SQLFlow的前端](https://sqlflow.gudusoft.com/)。
2. 在浏览器中上传SQL文本或文件。
3. 点击分析按钮后，查看数据血缘关系的可视化结果。
4. 在浏览器中，以交互形式，查看特定表或视图的完整血缘关系图。
5. 用 grabit 工具或 API，提交需要处理的 SQL 文件，然后在浏览器中查看结果，或在自己的代码中对返回的结果做进一步处理。

## 五、SQLFlow 的局限

SQLFlow 仅仅通过分析 SQL 脚本，包含存储过程(proceudre, function, trigger)来获取数据库中的数据血缘关系。
但在 ETL 数据转换过程中，会用到很多其它技术和工具，由此产生的数据血缘关系目前 SQLFlow 无法探知。

## 六、进一步了解 SQLFlow
1. 支持多达21个主流数据库
2. [Architecture document](sqlflow_architecture.md)