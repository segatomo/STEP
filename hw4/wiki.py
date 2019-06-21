# coding: utf-8
import math
import read_txt

def find_name(name):
    """
    探したい単語がpages.txtのなかにあったらそのidを返す関数
    name: 探したい単語(str)
    """
    data = read_txt.read_names('wikipedia_links/pages.txt')
    for d in data:
        if d['name'] == name:
            print('Find %s!' % name, end='')
            print('The id is %d.' % d['id'])
            return d['id']
    return None


def bfs(graph, start, end):
    """
    start: 探す人のid(int)
    end: 探したい人のid(int)
    """
    searched_list = []  # 探索済みリスト
    data = {start: []}  # key: node, value: そのnodeに着くまでに辿ったノードのリスト
    queue = [start]  # 探索候補
    step = 0  # ステップ数
    while queue:
        current = queue.pop(0)  # 現在位置
        if current == end:
            print(start, end='')
            for id in data[current]: # endに着くまでに辿ったノードのリスト
                print('->%d' % id, end='')
            return data[current]  
        if current not in searched_list:
            searched_list.append(current)
            if current in graph.keys():
                queue += graph[current]
            if len(graph[current]) > 0:
                for id in graph[current]:
                    if not id in data.keys():
                        data[id] = data[current] + [current]


def dijkstra(route_map):
    searched_list = []  # 探索済み
    not_searched = list(range(len(route_map)))  # 未探索
    distance = [math.inf] * len(route_map)
    distance[0] = 0
    from_list = [0] * len(route_map)

    while len(searched_list) != len(route_map):
        v = 0
        minimun = math.inf
        for i in not_searched:
            if distance[i] < minimun:  # 最小距離を更新
                v = i
                minimun = distance[i]
        # print(distance)
        searched_list.append(v)
        not_searched.remove(v)
        for i in not_searched:
            d = route_map[v][i]
            if d != 0 and distance[v] + d < distance[i]:
                distance[i] = distance[v] + d
                from_list[i] = v
    current = len(route_map) - 1
    result = [current + 1]

    while current != 0:
        current = from_list[current]
        result.append(current + 1)
    result.reverse()

    return result


if __name__ == "__main__":
    start = find_name('Google')
    end = find_name('渋谷')
    link_data = read_txt.read_links('wikipedia_links/links.txt')
    graph = read_txt.graph(link_data)
    bfs(graph, start, end)

