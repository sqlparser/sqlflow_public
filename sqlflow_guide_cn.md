# SQLFlow frontend guide

## 原理

SQLFlow frontend 最主要依赖的接口是 [**/sqlflow/generation/sqlflow/graph**](https://github.com/sqlparser/sqlflow_public/blob/master/api/sqlflow_api.md)。从这个接口获得数据后，分析其中的 graph 和 sqlflow 字段，绘制对应的图形，并进行相关的交互。在 SQLFlow frontend 中点击不同的按钮，或者在 setting 区域做不同的设置，实质上是给这个接口传递了不同的参数，从而获得了对应的图形结果。

参考：[SQLFlow api 文档](https://github.com/sqlparser/sqlflow_public/blob/master/api/sqlflow_api.md)

## overview

![1660980210797](https://user-images.githubusercontent.com/6293752/185734076-58a7b974-7c5e-41ae-86ee-7bf67eb21c35.png)

### sqltext editor

![1](https://user-images.githubusercontent.com/6293752/185734862-10a41894-eeb8-4331-a25f-1c764ae0ebc0.gif)

在代码编辑框输入 sql 代码，点击 dbvendor 菜单选择数据库，点击 visualize 按钮或者 visualize join 按钮，可以绘制对应的图像。

点击 visualize 按钮实际上是请求了[graph 接口](#graph)，并传入了下面的参数：

| 参数             | 值                                         |
| ---------------- | ------------------------------------------ |
| sqltext          | 代码编辑框中的代码，例如 select \* from a; |
| dbvendor         | dbvendor 菜单选择的数据库，例如 dbvoracle  |
| showRelationType | fdd                                        |
| ignoreFunction   | true                                       |

点击 visualize join 按钮实际上是请求了[graph 接口](#graph)，并传入了下面的参数：

| 参数             | 值                                         |
| ---------------- | ------------------------------------------ |
| sqltext          | 代码编辑框中的代码，例如 select \* from a; |
| dbvendor         | dbvendor 菜单选择的数据库，例如 dbvoracle  |
| showRelationType | join                                       |
| ignoreFunction   | true                                       |

### switch sample sql

点击 dbvendor 菜单，选择数据库后，点击 sample sql 可以在代码编辑框中获得这个 dbvendor 对应的示例 sql，随后可以 visualize。

![2](https://user-images.githubusercontent.com/6293752/185735004-847cdb63-88a4-49db-8482-8820920daded.gif)

### visualize a column or table by dropdown menu

![11](https://user-images.githubusercontent.com/6293752/185736807-21bb3f70-3fb2-47d6-a97d-c910b139fcbc.gif)

### hover sqltext to highlight graph

鼠标在 sqltext 上悬停，可以在图形中找到对应的图形。

![3](https://user-images.githubusercontent.com/6293752/185735065-d22debe6-6dbf-417d-9e61-798b28d9ddf6.gif)

### hover graph to highlight sqltext

鼠标在图形上悬停，可以在 sqltext 中找到对应的代码。

![4](https://user-images.githubusercontent.com/6293752/185735156-de5d071a-1a55-4914-81a4-90aac85aa036.gif)

### resize left panel width

鼠标悬停在面板边缘悬停，如果有高亮效果，则可以拖动跳转宽度。

![5](https://user-images.githubusercontent.com/6293752/185735279-20b41fb1-a191-40fa-9fc1-d258246ea0fe.gif)

### pin graph, drag graph, and cancel

点击图形某个 column，可以固定上下游关系。长按鼠标左键，可以移动画布。

![6](https://user-images.githubusercontent.com/6293752/185735432-0ef385fd-b1b8-4269-ae47-e339e2b78bf5.gif)

## setting

设置当前[graph 接口](#graph)接口的参数，来获得不同的分析结果：

| 参数                        | 值                                                                                                                       |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| showRelationType            | 如果 direct dataflow = true，为 fdd；<br />如果 direct dataflow = true 且 indirect dataflow=true ，为 fdd,fddi,fdr,frd； |
| dataflowOfAggregateFunction | direct 或者 indirect，取决于 dataflowOfAggregateFunction                                                                 |
| ignoreRecordSet             | false 或者 true，取决于 show intermediate recordset                                                                      |
| ignoreFunction              | false 或者 true，取决于 show function                                                                                    |
| showConstantTable           | false 或者 true，取决于 show constant                                                                                    |
| showTransform               | false 或者 true，取决于 show transform                                                                                   |

切换不同的选项，观察网络请求，可以看到接口参数的变化：

![7](https://user-images.githubusercontent.com/6293752/185736267-6eefb036-f047-4a72-a95f-391847e5f145.gif)

### show function

![8](https://user-images.githubusercontent.com/6293752/185736347-1ce8fbf9-b66e-45e8-af75-137b746bc31d.gif)

### show transform

![10](https://user-images.githubusercontent.com/6293752/185736610-6fba47eb-9dba-42cc-9f00-5af3ad22563f.gif)

## job list

![image](https://user-images.githubusercontent.com/6293752/185734108-5dc282df-0b49-4061-af2d-c9fa21ab885a.png)

### create a job

![12](https://user-images.githubusercontent.com/6293752/185737736-814ae584-ab72-4be6-a4f6-6393607d385f.gif)

### backwards in code

![14](https://user-images.githubusercontent.com/6293752/185738467-b8485e3c-cbc4-4ceb-ab20-5e869908551b.gif)

## schema

![image](https://user-images.githubusercontent.com/6293752/185734174-6d507fb8-2cb3-4a75-a5b7-4ab70ba8addd.png)

显示 sql 的 schema 结构。在 schema、database、table 上点击鼠标右键，可以 visualize。

![13](https://user-images.githubusercontent.com/6293752/185738098-7ebe1e25-816e-4178-8f60-220d02c17b00.gif)

global、summay、ignore record 表示的是[graph 接口](#graph)返回的的三个模式（json 中的 mode 字段），分别用三种不同的颜色表示。

![image](https://user-images.githubusercontent.com/6293752/185738177-a7b66a2f-9532-4669-87b8-d6284d4bf03b.png)

ANALYTICS、ENTITY 前的图标为绿色，表示 mode 为 global；DATAMART 前为黑色，表示 mode 为 summary；其他节点前为灰色，表示当前节点还没有被 visualize。

### view DDL

![15](https://user-images.githubusercontent.com/6293752/185738579-962c06d1-80c0-4b61-8251-f5541d0564d3.gif)

## export

导出处理结果为 json 或者 png:
![1660980656500](https://user-images.githubusercontent.com/6293752/185734305-70c24757-c59c-40b4-b235-a79a214b7472.png)

## 接口

参考：[SQLFlow api 文档](https://github.com/sqlparser/sqlflow_public/blob/master/api/sqlflow_api.md)

<span id="graph">graph 接口：</span> post /sqlflow/generation/sqlflow/graph
