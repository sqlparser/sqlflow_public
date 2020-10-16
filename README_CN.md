## SQLFlow 介绍

SQLFlow 是一个数据库工具，通过分析数据仓库中各个数据库的 SQL 脚本，来帮助用户了解数据是如何在
各个数据库、各个表、各个字段之间流动的，从而及时了解组织的IT系统中的数据组成和流向。

举例来说，可能会问财务报表中的统计结果，它是有哪些子系统（采购、生产、销售等）提供的数据汇总而成的？
当某个子系统（例如 销售子系统）的数据结构发生变化时，可能会影响其它子系统吗，财务报表子系统也是否需要进行改动？

SQLFlow 会帮助你回答这些问题，以可视化的图形方式把这些关系呈现在你面前，让你对组织的IT系统中的数据流动一目了然。


![SQLFlow Introduce](images/sqlflow_introduce1.png)

### SQLFlow 可以为你做什么
- 把IT系统中的数据流以图形方式提供给用户
- 分析数据仓库中各个数据库的 SQL 脚本，把分析所得的元数据(metadata)提供给用户
- 在图形中帮助用户快速追溯数据的前后流动，找到相关的数据源
- 支持多个21个主流数据库

### 如何使用 SQLFlow
- 通过官网 [the official website](https://gudusoft.com/sqlflow/#/)
- 在自己的系统中调用 SQLFlow 提供的 Restful API
- 在组织内部安装使用 SQLflow，保护数据隐私


### SQLFlow 报价
- [SQLFlow price plan](sqlflow_pricing_plans.md)

### Restful APIs
- [SQLFlow API document](https://github.com/sqlparser/sqlflow_public/blob/master/api/sqlflow_api.md)
- [Client in C#](https://github.com/sqlparser/sqlflow_public/tree/master/api/client/csharp)

### SQLFlow 的设计架构
- [Architecture document](sqlflow_architecture.md)

### 用户手册
- [开发中...]()
