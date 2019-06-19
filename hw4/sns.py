# coding: utf-8
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
    queue = [start]  # 探索候補スタック
    step = 0  # ステップ数
    while queue:
        current = queue.pop(0)  # 現在位置
        if end in queue:
            searched_list.append(current)
            return step
        if current not in searched_list:
            searched_list.append(current)
            queue += graph[current]
            step += 1
        else:
            step -= 1            
        
    return step


if __name__ == "__main__":
    start_name = input('Enter your account name: ')
    end_name = input('Who is the person you are looking for?: ')

    start = find_name(start_name)
    end = find_name(end_name)

    if start and end:
        print('ok')
    else:
        print('Not found…')
        exit()

    link_data = read_txt.read_links('links.txt')
    graph = read_txt.graph(link_data)
    step = bfs(graph, start, end)
    
    if step == 1:
        print('%s need to follow the link to reach out to %s %d step.' % (start_name, end_name, step))
    else:
        print('%s need to follow the link to reach out to %s %d steps.' % (start_name, end_name, step))

        