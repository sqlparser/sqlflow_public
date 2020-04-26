Embed the SQLFlow UI into your application

# 实现方式

技术上，需要把现有的部分代码抽取出来，打包成一个js文件（sqlflow.js），这个sqlflow.js对外提供一个类（SQLFlow），客户可以实例化这个类，嵌入自己的网页，获取各种数据，进行各种操作。

例如，假如客户有一个html文件：



```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<div class="customer">customer's content</div>
<div id="SQLFlow"></div>
</body>
</html>

```

现在客户想在自己网页中id等于SQLFlow的标签内展示sql graph，那么客户可以：

1. 导入我提供的sqlflow.js
2. 传入参数（参数和与config.json类似,el="#SQLFlow"），实例化SQLFlow
3. 在合适的时机调用SQLFlow.render方法初始化SQLFlow

例如：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>Title</title>

  <!--1. 导入我提供的sqlflow.js，传入参数，实例化SQLFlow-->
  <script src="sqlflow.js"></script>

  <script>

    // 2. 传入参数（参数和与config.json类似,el="#SQLFlow"），实例化SQLFlow
    const sqlflow = new SQLFlow({
      el:"#SQLFlow",
      ApiPrefix:"",
      Authorization:""
    })

    // 3. 在合适的时机调用SQLFlow.render方法初始化SQLFlow
    sqlflow.render();

  </script>
</head>
<body>
<div class="customer">customer's content</div>
<div id="SQLFlow"></div>
</body>
</html>

```

操作完成后就可以得到目前的图形展示效果。

此外，为满足客户嵌入自己网页，编程操纵的需求，sqlflow.js还可以对外提供更多的方法（api）。这些方法一般分为三类：

1. 操作设置
2. 获取数据
3. 事件监听

例如：

## 操作设置

### SQLFlow.render()

挂载sqlflow到html，只能初始化的时候调用一次。

### SQLFlow.setSQLText(sqltext:string)

设置当前的sql文本

### SQLFlow.setSQLFlie(sqlfile: FileList | Blob)

设置当前的sql文件

### SQLFlow.setDbvendor(dbvendor:string)

设置dbvendor

### SQLFlow.visualize()

效果和目前点击visualize按钮一致

### SQLFlow.highlightColumnById(columnId:string)

高亮graph中的某个column，columnId来源于SQLFlow.getColumnList()中的graph column

### SQLFlow.highlightColumnAndRelationById(columnId:string)

高亮graph中的某个column和与它相关的relation，columnId来源于SQLFlow.getColumnList()中的graph column

### SQLFlow.lineColumnById(columnId:string)

效果等同于目前的column lineage，columnId来源于SQLFlow.getColumnList()中的graph column

## 获取数据

注意：这里获取到的数据结构和dbojs不一样

### SQLFlow.getTableList()

获取dbojs中的table，部分返回结果如下：

```json
{
	"1": {
		"id": "1",
		"name": "RESULT_OF_a",
		"type": "select_list",
		"database": "unknown",
		"schema": "DEFAULT",
		"coordinates": [{"x": 11,"y": 29}, {"x": 11,"y": 30}],
		"columns": {
			"logicIds": ["7", "8", "9"],
			"graphIds": ["33", "34", "35"]
		},
		"graphId": "n8"
	},
	"10": {
		"id": "10",
		"name": "RESULT_OF_b",
		"type": "select_list",
		"database": "unknown",
		"schema": "DEFAULT",
		"coordinates": [{"x": 15,"y": 32}, {"x": 15,"y": 33}],
		"columns": {"logicIds": ["14", "15"],"graphIds": ["36", "37"]},
		"graphId": "n9"
	}
}
```

columns.graphIds表示是graph columnId，使用这个columnId到SQLFlow.getColumnList()结果中的graph中查表，可以获得这个column的graph信息。

columns.logicIds表示是logic columnId，使用这个columnId到SQLFlow.getColumnList()结果中的logic中查表，可以获得这个column的logic信息。

### SQLFlow.getColumnList()

获取dbojs中的column，column分为logic和graph类型，部分返回结果如下：

```json
{

	"graph": {
		"33": {
			"id": "33",
			"uuid": "V0Am-IR7zCUYzQ4398Lxi",
			"tableId": "1",
			"name": "deptno",
			"coordinates": [[{"x": 6,"y": 18}, {"x": 6,"y": 24}]],
			"sources": {"relationIds": ["1"]},"targets": {"relationIds": ["4"]},
			"logicIds": ["7"],
			"midY": 50,
			"highlight": false,
			"mouseover": false
		}
	},
	"logic": {
		"7": {
			"id": "7",
			"tableId": "1",
			"name": "deptno",
			"coordinates": [[{"x": 6,"y": 18}, {"x": 6,"y": 24}]],
			"sources": [{"relationId": "1","logicId": "3","tableId": "63"}],
			"targets": [{"relationId": "4","logicId": "17","tableId": "16"}],
			"graphId": "33"
		}
	}
}
```



### SQLFlow.getRelationList()

获取dbojs中的relation，部分返回结果如下：

```json
{
	"1": {
		"id": "1",
		"oringinalId": "1",
		"type": "fdd",
		"source": {"column": {"logicId": "3","graphId": "26","tableId": "63"}},
		"target": {"column": {"logicId": "7","graphId": "33","tableId": "1"}
		},
		"show": true,
		"lineage": false,
		"highlight": false,
		"svg": {
			"text": {"x": "","y": "","value": "","title": ""},
			"path": "M 197 76.492 C 232 76.492 232 50 257 50",
			"arrow": "267,50 257,46.5 257,53.5",
			"isDash": false,
			"isJoin": false,
			"isSelfJoin": false
		}
	},
	"4": {
		"id": "4",
		"oringinalId": "16",
		"type": "fdd",
		"source": {"column": {"logicId": "7","graphId": "33","tableId": "1"}},
		"target": {"column": {"logicId": "17","graphId": "38","tableId": "16"}},
		"show": true,
		"lineage": false,
		"highlight": false,
		"svg": {
			"text": {"x": "","y": "","value": "","title": ""},
			"path": "M 429 50 C 504 50 504 74.656 569 74.656",
			"arrow": "579,74.656 569,71.156 569,78.156",
			"isDash": false,
			"isJoin": false,
			"isSelfJoin": false
		}
	}
}
```

使用tableId到SQLFlow.getTableList()的结果中查表，可以获得这个table的信息。

使用graphId到SQLFlow.getColumnList()结果中的graph中查表，可以获得这个column的graph信息。

使用logicId到SQLFlow.getColumnList()结果中的logic中查表，可以获得这个column的logic信息。

### SQLFlow.getSchemaList()

获取schema，部分返回结果如下：

```json
{
	"table": {
		"unknown": {
			"DEFAULT": {
				"24": ["1", "2", "3", "4"],
				"29": ["5", "6", "7", "8"],
				"34": ["9", "10", "11", "12"],
				"39": ["13", "14", "15", "16", "17", "18"],
				"40": ["19", "20", "22", "23"],
				"46": ["24", "25"]
			},
			"scott": {
				"63": ["26", "28"]
			}
		}
	},
	"view": {
		"unknown": {
			"DEFAULT": {
				"20": ["30", "31", "32"]
			}
		}
	},
	"procedure": {
		"unknown": {
			"DEFAULT": {}
		}
	},
	"function": {
		"unknown": {
			"DEFAULT": {}
		}
	},
	"trigger": {
		"unknown": {
			"DEFAULT": {}
		}
	},
	"synonym": {
		"unknown": {
			"DEFAULT": {}
		}
	},
	"select_list": {
		"unknown": {
			"DEFAULT": {
				"1": ["33", "34", "35"],
				"10": ["36", "37"],
				"16": ["38", "39", "40"]
			}
		}
	},
	"temp_result": {
		"unknown": {
			"DEFAULT": {
				"50": ["41", "42", "43", "44", "45", "46"]
			}
		}
	}
}
```

table.unknown.DEFAULT表示数据库名称为unknown，schema为DEFAULT，DEFAULT下的"24"、"29"、"34"表示tableId，使用这个tableId到SQLFlow.getTableList()的结果中查表，可以获得这个table的信息。"24"下的"1", "2", "3", "4"表示是graph columnId，使用这个columnId到SQLFlow.getColumnList()结果中的graph中查表，可以获得这个column的graph信息。

## 事件监听

### SQLFlow.addEventListener(name:string,handler:function)

增加一个事件监听器，当sqlflow的graph中发生这个事件时，会触发客户提供的函数handler。

例如，name可以为

1. onMouseoverColumn ：当客户鼠标滑过某一个column时触发
2. onLineColumn： 当客户点击column lineage时触发
3. 其他事件

### SQLFlow.removeEventListener(name:string,handler:function)

移除一个事件监听器。

# 应用

综合运用以上api，可以实现流程图中的需求：

1. 客户自建一个sql列表，
2. 客户引入sqlflow.js，初始化SQLFlow，将SQLFlow程序嵌入自己的网页
3. 点击sql列表上的某个sql
4. 从点击事件中获得这个sql,调用SQLFlow.setSQLText(sql)
5. 调用SQLFlow.visualize获取图形结果

还可以根据需要实现更多复杂的编程控制。