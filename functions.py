def dfs(graph, vertex, path, visited):
    """ выполняет обход в глубину
    graph - список смежных вершин
    vertex - номер стартовой вершины
    path - список, в который записывается путь обхода
    visited - массив уже посещенных вершин"""
    visited[vertex] = True
    path.append(vertex)
    for w in graph[vertex]:
        if not visited[w]:  # посещён ли текущий сосед?
            dfs(graph, w, path, visited)


def calculate_bounds(_graph_weight, position, avail_list, arclist, graphpath):
    """
    Подсчитывает верхнию и нижнюю оценку
    :param _graph_weight: список из уже присвоенных весов
    :param position: число, параметр итерации дерева решений
    :param avail_list: список неиспользованных весов
    :param arclist: список всех ребер графа
    :param graphpath: список из вершин в порядке их обхода в глубину
    :return: кортеж (low,high), состоящий из нижней и верхней оценки соответственно
    """
    low = high = 0
    graphpathpart = graphpath[:position + 1]
    maxdiff = abs(avail_list[0] - avail_list[-1])
    mindiff = min([abs(avail_list[i + 1] - avail_list[i]) for i in range(len(avail_list) - 1)])
    for arc in arclist:
        if arc[0] in graphpathpart:
            if arc[1] in graphpathpart:
                diff = abs(_graph_weight[arc[0]] - _graph_weight[arc[1]])
                high += diff
                low += diff
            else:
                high += max(abs(_graph_weight[arc[0]] - avail_list[0]), abs(_graph_weight[arc[0]] - avail_list[-1]))
                low += min([abs(_graph_weight[arc[0]] - weight) for weight in avail_list])
        else:
            if arc[1] in graphpathpart:
                high += max(abs(_graph_weight[arc[1]] - avail_list[0]), abs(_graph_weight[arc[1]] - avail_list[-1]))
                low += min([abs(_graph_weight[arc[1]] - weight) for weight in avail_list])
            else:
                high += maxdiff
                low += mindiff

    return low, high


def findbest(_list):
    """
    Находит из нескольких вариантов лучший
    :param _list: список промежуточных вариантов, состоящих из оценки и расположения весов
    :return: лучший результат и соответствующее расположение весов
    """
    res = 0
    best_way = []
    for first, second in _list:
        if first > res:
            res = first
            best_way = second
    return res, best_way
