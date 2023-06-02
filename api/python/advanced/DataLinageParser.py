/**
*  解析SQLFLow exportLineageAsJson接口返回的JSON格式的血缘关系中的关系链路
*
*  例如demo中的血缘数据，解析成以下链路：
*  达成的目标是，List中两个元素：
*    SCOTT.DEPT -> SCOTT.EMP->VSAL
*    SCOTT.EMP->VSAL
*/

import json

class Node:
    def __init__(self, value, node_id):
        self.value = value
        self.id = node_id
        self.next = None

    def key(self):
        node = self.next
        key = self.id
        while node:
            key += node.id
            node = node.next
        return key

def main():
    input_data = '{"jobId":"d9550e491c024d0cbe6e1034604aca17","code":200,"data":{"mode":"global","sqlflow":{"relationship":[{"sources":[{"parentName":"ORDERS","column":"TABLE","coordinates":[],"id":"10000106","parentId":"86"}],"id":"1000012311","type":"fdd","target":{"parentName":"SPECIAL_ORDERS","column":"TABLE","coordinates":[],"id":"10000102","parentId":"82"}},{"sources":[{"parentName":"CUSTOMERS","column":"TABLE","coordinates":[],"id":"10000103","parentId":"94"}],"id":"1000012312","type":"fdd","target":{"parentName":"SPECIAL_ORDERS","column":"TABLE","coordinates":[],"id":"10000102","parentId":"82"}}]}},"sessionId":"8bb7d3da4b687bb7badf01608a739fbebd61309cd5a643cecf079d122095738a_1685604216451"}'
    try:
        data = json.loads(input_data)
        relationship_node = data["data"]["sqlflow"]["relationships"]
        data_list = relationship_node

        value = []
        node_map = {}
        for data_item in data_list:
            sources = data_item["sources"]
            target_node = data_item["target"]
            target = Node(target_node["parentName"], target_node["parentId"])
            if sources:
                for source in sources:
                    parent_id = source["parentId"]
                    parent_name = source["parentName"]
                    source_node = Node(parent_name, parent_id)
                    source_node.next = target
                    value.append(source_node)
                    node_map[parent_id] = source_node
            else:
                value.append(target)
                node_map[target_node["parentId"]] = target

        for node in value:
            next_node = node.next
            if next_node:
                next_id = next_node.id
                next_node = node_map.get(next_id)
                if next_node:
                    node.next = next_node

        key_set = set()
        value_iter = iter(value)
        while True:
            try:
                node = next(value_iter)
                k = node.key()
                if k in key_set:
                    value_iter.remove()
                key_set.add(k)
            except StopIteration:
                break

        chains = []
        print(chains)
    except json.JSONDecodeError as e:
        print(e)

if __name__ == "__main__":
    main()
