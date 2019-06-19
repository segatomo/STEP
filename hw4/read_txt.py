# coding: utf-8

def read_names(filename):
    page_data = [] # 辞書のリスト
    with open(filename, "r") as f:
        for line in f:
            if line.split():
                page_data.append({ "id": int(line.split()[0]), "name": line.split()[1] })
    return page_data


def read_links(filename):
    link_data = [] # 辞書のリスト(にする必要ある??)
    with open(filename, "r") as f:
        for line in f:
            if line.split():
                link_data.append({ "from": int(line.split()[0]), "to": int(line.split()[1]) })
    return link_data


def graph(link_data):
    """
    linkを整理する関数
    """
    graph = {}
    to = [link_data[0]['to']]
    for i in range(1, len(link_data)):
        if link_data[i-1]['from'] == link_data[i]['from']:
            to.append(link_data[i]['to'])
        else:
            to = [link_data[i]['to']]
        graph[link_data[i]['from']] = to
    return graph