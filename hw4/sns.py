import read_txt

def find_name(name):
    """
    探したい人の名前がnicknames.txtのなかにあったらそのidを返す関数
    name: 探したい人の名前(str)
    """
    data = read_txt.read_names('nicknames.txt')
    for d in data:
        if d['name'] == name:
            return d['id']
    return None


def bfs(graph, start, end):
    """
    start: 探す人のid(int)
    end: 探したい人のid(int)
    """
    searched_list = []  # 探索済みリスト
    data = {start: []}
    queue = [start]  # 探索候補
    step = 0  # ステップ数
    while queue:
        current = queue.pop(0)  # 現在位置
        if current == end:
            return len(data[current])
        if current not in searched_list:
            searched_list.append(current)
            queue += graph[current]
            for id in graph[current]:
                if not id in data.keys():
                    data[id] = data[current] + [current]


def main():
    start_name = input('Enter your account name: ')
    end_name = input('Who is the person you are looking for?: ')

    start = find_name(start_name)
    end = find_name(end_name)

    if start is None:
        print('%s was not found…' % start_name)
        exit()
    elif end is None:
        print('%s was not found…' % end_name)
        exit()
    else:
        print('OK.')
        
    link_data = read_txt.read_links('links.txt')
    graph = read_txt.graph(link_data)
    step = bfs(graph, start, end)

    if step == 1:
        print('%s need %d step to reach out to %s.' % (start_name, step, end_name))
    elif step != None:
        print('%s need %d steps to reach out to %s.' % (start_name, step, end_name))
    else: 
        print('%s cannot reach out to %s' % (start_name, end_name))


if __name__ == "__main__":
    main()