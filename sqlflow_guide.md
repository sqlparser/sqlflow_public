# SQLFlow frontend guide

## 原理

SQLFlow frontend 最主要依赖的接口是 [**/sqlflow/generation/sqlflow/graph**](https://github.com/sqlparser/sqlflow_public/blob/master/api/sqlflow_api.md)。从这个接口获得数据后，分析其中的graph和sqlflow字段，绘制对应的图形，并进行相关的交互。在 SQLFlow frontend 中点击不同的按钮，或者在setting区域做不同的设置，实质上是给这个接口传递了不同的参数，从而获得了对应的图形结果。

参考：[SQLFlow api 文档](https://github.com/sqlparser/sqlflow_public/blob/master/api/sqlflow_api.md)

![1](https://user-images.githubusercontent.com/6293752/95873864-e2734400-0da2-11eb-85a9-e46ea43ff5c3.png)

## editor

在代码编辑框输入sql代码，点击dbvendor菜单选择数据库，点击visualize按钮或者visualize join按钮，可以绘制对应的图像。

点击visualize按钮实际上是请求了graph接口，并传入了下面的参数：

| 参数             | 值                                        |
| ---------------- | ----------------------------------------- |
| sqltext          | 代码编辑框中的代码，例如 select * from a; |
| dbvendor         | dbvendor菜单选择的数据库，例如 dbvoracle  |
| showRelationType | fdd                                       |
| ignoreFunction   | true                                      |

点击visualize join按钮实际上是请求了graph接口，并传入了下面的参数：

| 参数             | 值                                        |
| ---------------- | ----------------------------------------- |
| sqltext          | 代码编辑框中的代码，例如 select * from a; |
| dbvendor         | dbvendor菜单选择的数据库，例如 dbvoracle  |
| showRelationType | join                                      |
| ignoreFunction   | true                                      |

### sample sql

点击dbvendor菜单选择数据库后，点击 sample sql 可以在代码编辑框中获得这个 dbvendor对应的示例sql。

### upload

上传一个文件，在后台创建一个job，当job处理成功后可以获得对应的结果。

### login

登录按钮。登录后可以上传文件，保存图像结果。目前登录功能仅支持 https://gudusoft.com/sqlflow/ 。

## schema

显示sql的schema结构。在schema、database、table上点击鼠标右键，可以visualize。[超链文字](#graph)

![3](https://user-images.githubusercontent.com/6293752/95968181-b8bc2a80-0e3f-11eb-8fc4-1501778fdc74.gif)

global、summay、ignore record表示的是graph接口返回的的三个模式（json 中的 mode 字段），分别用三种不同的颜色表示。

![image](https://user-images.githubusercontent.com/6293752/95972556-2a4aa780-0e45-11eb-8b61-2126ae9f3e0d.png)

DATAMART、DBO前的图标为橙色，表示mode为ignore record set；LOAN前为绿色，表示mode为global；其他节点前为灰色，表示当前节点还没有被visualize。

## setting

![image](https://user-images.githubusercontent.com/6293752/95977385-6da81480-0e4b-11eb-8ec0-cc0de5466701.png)

设置当前graph接口的参数：

| 参数             | 值                                                           |
| ---------------- | ------------------------------------------------------------ |
| hideColumn       | false 或者 true，取决于hide all columns                      |
| showRelationType | 如果 dataflow=true  impact=false，为fdd；<br />如果 dataflow=true  impact=true ，为fdd,ddi,fdr,frd；<br />如果 dataflow=false impact=true ，为fddi,fdr,frd； |
| ignoreRecordSet  | false 或者 true，取决于show intermediate recordset           |
| ignoreFunction   | false 或者 true，取决于show function                         |

## job

![image](https://user-images.githubusercontent.com/6293752/95977128-0b4f1400-0e4b-11eb-8c68-62657380e853.png)

点击upload按钮，可以上传文件，创建一个job。当job处理完成后，可以点击view lineage，打开处理结果。

## download

导出处理结果为json或者png。

## sqlflow

鼠标左键点击某一列可以固定关联关系，点击cancel可以取消。

![3](https://user-images.githubusercontent.com/6293752/95986233-3ee46b00-0e58-11eb-8ee4-85a7ca5ee0f4.gif)

鼠标右键点击 table lineage、column lineage可以显示表或列的关联关系，点击cancel可以取消。[内容][graph接口]

![3](https://user-images.githubusercontent.com/6293752/95986541-c336ee00-0e58-11eb-8a45-ad2d904d89ca.gif)

## 接口

参考：[SQLFlow api 文档](https://github.com/sqlparser/sqlflow_public/blob/master/api/sqlflow_api.md)

<span id="graph">graph接口：</span> post /sqlflow/generation/sqlflow/graph

