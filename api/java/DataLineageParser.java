package java;
/**
*  解析SQLFLow exportLineageAsJson接口返回的JSON格式的血缘关系中的关系链路
*
*  例如demo中的血缘数据，解析成以下链路：
*  达成的目标是，List中两个元素：
*    SCOTT.DEPT -> SCOTT.EMP->VSAL
*    SCOTT.EMP->VSAL
*/

public class DataLineageParser {
    static class Node {
        String value;
        String id;
        Node next;

        public Node(String value, String id) {
            this.value = value;
            this.id = id;
        }

        public String key() {
            Node node = this.next;
            StringBuilder key = new StringBuilder(id);
            while (node != null) {
                key.append(node.id);
                node = node.next;
            }
            return key.toString();
        }
    }

    public static void main(String[] args) {
        String input = "{"jobId":"d9550e491c024d0cbe6e1034604aca17","code":200,"data":{"mode":"global","sqlflow":{"relationship":[{"sources":[{"parentName":"ORDERS","column":"TABLE","coordinates":[],"id":"10000106","parentId":"86"}],"id":"1000012311","type":"fdd","target":{"parentName":"SPECIAL_ORDERS","column":"TABLE","coordinates":[],"id":"10000102","parentId":"82"}},{"sources":[{"parentName":"CUSTOMERS","column":"TABLE","coordinates":[],"id":"10000103","parentId":"94"}],"id":"1000012312","type":"fdd","target":{"parentName":"SPECIAL_ORDERS","column":"TABLE","coordinates":[],"id":"10000102","parentId":"82"}}]}},"sessionId":"8bb7d3da4b687bb7badf01608a739fbebd61309cd5a643cecf079d122095738a_1685604216451"}";
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            JsonNode jsonNode = objectMapper.readTree(input);
            JsonNode relationshipNode = jsonNode.path("data").path("sqlflow").path("relationships");
            List<Map<String, Object>> dataList = objectMapper.readValue(relationshipNode.toString(), new TypeReference<List<Map<String, Object>>>() {
            });

            ArrayList<Node> value = new ArrayList<>();
            Map<String, Node> nodeMap = new HashMap<>();
            for (Map<String, Object> data : dataList) {
                List<Map<String, Object>> sources = (List<Map<String, Object>>) data.get("sources");
                Map<String, Object> targetNode = (Map<String, Object>) data.get("target");
                Node target = new Node((String) targetNode.get("parentName"), (String) targetNode.get("parentId"));
                if (!sources.isEmpty()) {
                    for (Map<String, Object> source : sources) {
                        String parentId = (String) source.get("parentId");
                        String parentName = (String) source.get("parentName");
                        Node sourceNode = new Node(parentName, parentId);
                        sourceNode.next = target;
                        value.add(sourceNode);
                        nodeMap.put(parentId, sourceNode);
                    }
                } else {
                    value.add(target);
                    nodeMap.put((String) targetNode.get("parentId"), target);
                }
            }

            for (Node node : value) {
                Node next = node.next;
                if (next != null) {
                    String id = next.id;
                    next = nodeMap.get(id);
                    if (next != null) {
                        node.next = next;
                    }
                }
            }

            HashSet<String> key = new HashSet<>();
            Iterator<Node> iterator = value.iterator();
            while (iterator.hasNext()) {
                Node node = iterator.next();
                String k = node.key();
                if (key.contains(k)) {
                    iterator.remove();
                }
                key.add(k);
            }

            // value
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }
    }
}
