## Get SQL Information By SQLFLow Coordinate

### SQLInfo
When the sqlflow analyzing sql has been finished, it recorded some sql information, we can use it to locate database object position.

```java
public class SqlInfo {
    private String fileName;
    private String sql;
    private int originIndex;
    private int index;
    private String group;
    private int originLineStart;
    private int originLineEnd;
    private int lineStart;
    private int lineEnd;
    private String hash;
}
```

Each sql file matches a SqlInfo object, and the map key is "hash" property.

Sqlflow provides a tool class gudusoft.gsqlparser.dlineage.util.SqlInfoHelper, which can transform dataflow coordinate to `DbObjectPosition`.

### SqlInfoHelper

1. First step, call api `SqlInfoHelper.getSqlInfoJson` to fetch the sqlinfo map from the DataFlowAnalyzer object, and persist it.
```java
    public static String getSqlInfoJson(DataFlowAnalyzer analyzer);
```

2. Second step, initialize the SqlInfoHelper with the sqlinfo json string.
```java
    //Constructor
    public SqlInfoHelper(String sqlInfoJson);
```

3. Third step, transform sqlflow position string to `dataflow.model.json.Coordinate` array.
  * If you use the `dataflow.model.json.DataFlow` model, you can get the Coordinate object directly, doesn't need any transform.
  * If you use the `dataflow.model.xml.dataflow` model, you can call api `SqlInfoHelper.parseCoordinateString`
  ```java
    public static Coordinate[][] parseCoordinateString(String coordinate);
  ```
  * Method parseCoordinateString support both of xml output coordinate string and json output coordinate string, like these:
  ```json
      //xml output coordinate string
      [56,36,64e5c5241fd1311e41b2182e40f77f1e],[56,62,64e5c5241fd1311e41b2182e40f77f1e]

      //json output coordinate string
      [{"x":31,"y":36,"hashCode":"64e5c5241fd1311e41b2182e40f77f1e"},{"x":31,"y":38,"hashCode":"64e5c5241fd1311e41b2182e40f77f1e"}]     
  ``` 

4. Fourth step, get the DbObjectPosition by api getSelectedDbObjectInfo
```java
    public DbObjectPosition[] getSelectedDbObjectInfo(Coordinate start, Coordinate end)
```
  * Each position has two coordinates, start coordinate and end coordinate. If the result of DBObject.getCoordinates() has 10 items, it match 5 positions. 
  
### How to use DbObjectPosition
```java
public class DbObjectPosition {
    private String file;
    private String sql;
    private int index;
    private List<Pair<Integer, Integer>> positions = new ArrayList<Pair<Integer, Integer>>();
}
```
* file field matches the sql file name.
* sql field matches the sql content.
* index: 
   * If the sql file is from `grabit`, it's a json file, and it has an json array named "query", the value of index field is the query item index.  
   * Other case, the value of index field is 0.
* positions, locations of database object, they are matched the sql field. Position x and y **base 1** but not 0.    

### Example
```java
  String sql = "Select\n a\nfrom\n b;";
  DataFlowAnalyzer dataflow = new DataFlowAnalyzer(sql, EDbVendor.dbvmssql, false);
  dataflow.generateDataFlow(new StringBuffer());
  dataflow flow = dataflow.getDataFlow();
  String coordinate = flow.getTables().get(0).getCoordinate();
  Coordinate[][] coordinates = SqlInfoHelper.parseCoordinateString(coordinate);
  SqlInfoHelper helper = new SqlInfoHelper(SqlInfoHelper.getSqlInfoJson(dataflow));
  DbObjectPosition[] postion = helper.getSelectedDbObjectInfo(coordinates[0][0], coordinates[0][1]);
  System.out.println(postion[0].getSql());
  System.out.println("table " + flow.getTables().get(0).getName() + " position is " + Arrays.toString(postion[0].getPositions().toArray()));
``` 

Return:
```java
Select
 a
from
 b;

table b position is [[4,2], [4,3]]
```


