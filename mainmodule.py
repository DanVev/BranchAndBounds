import sys
from graph import *
import random
import time
from functions import *

sys.setrecursionlimit(100000)
graphpath = []
raw_matrix = []
best_upper_bound = best_lower_bound = branchcount = iterations = 0


def search(weight_list, path, graph_weight, used_weight, position):
    """
    Реализация метода ветвей и границ
    :param weight_list: список весов
    :param path: список вершин в порядке обхода графа в глубину
    :param graph_weight: Изначально пустой список для хранения весов для вершин
    :param used_weight: Изначально пустой список булевых переменных, отвечающих за уже использованные веса
    :param position: число-парметр итерации яруса дерева решений
    :return: лучшая оценка и соответствующее размещение весов
    """
    res = []
    global branchcount, best_lower_bound, best_upper_bound, graph, iterations, arclist, graphpath
    for order, weight in enumerate(weight_list):
        if used_weight[order]:
            continue
        this_graph_weight = graph_weight.copy()
        this_graph_weight[path[position]] = weight
        this_used = used_weight.copy()
        this_used[order] = True
        this_avail_list = [weight_list[i] for i in range(len(weight_list)) if not used[i]]
        # подсчет верхней и нижней оценки
        this_lower, this_upper = calculate_bounds(this_graph_weight, position, this_avail_list, arclist, graphpath)
        # отсев
        if best_lower_bound >= this_upper:
            continue
        if best_lower_bound < this_lower:
            best_lower_bound = this_lower
        iterations += 1
        if position != len(graph) - 1:
            res.append(search(weight_list, path, this_graph_weight, this_used, position + 1))
        else:
            branchcount += 1
            if this_lower == this_upper:
                return this_upper, this_graph_weight
    return findbest(res)


def fullsearch(weight_list, path, graph_weight, used_weight, position):
    """
    Реализация полного перебора с подсчетом лучшей оценки и размещения весов
    :param weight_list: список весов
    :param path: список вершин в порядке обхода графа в глубину
    :param graph_weight: Изначально пустой список для хранения весов для вершин
    :param used_weight: Изначально пустой список булевых переменных, отвечающих за уже использованные веса
    :param position: число-параметр итерации яруса дерева решений
    :return: лучшая оценка и соответствующее размещение весов
    """
    res = []
    global branchcount, best_lower_bound, best_upper_bound, graph, iterations, arclist, graphpath
    for order, weight in enumerate(weight_list):
        if used_weight[order]:
            continue
        iterations += 1
        this_graph_weight = graph_weight.copy()
        this_graph_weight[path[position]] = weight
        this_used = used_weight.copy()
        this_used[order] = True
        this_avail_list = [weight_list[i] for i in range(len(weight_list)) if not used[i]]
        # подсчет верхней и нижней оценки
        this_lower, this_upper = calculate_bounds(this_graph_weight, position, this_avail_list, arclist, graphpath)
        if position != len(graph) - 1:
            res.append(fullsearch(weight_list, path, this_graph_weight, this_used, position + 1))
        else:
            branchcount += 1
            return this_upper, this_graph_weight
    return findbest(res)

while True:
    ch = input("\nDo you want to input graph and weight list (button I) or generate all data (button G)? ")
    if ord(ch) in [73, 105, 152, 232]:
        graphsize = int(input("Input graph size: "))
        for i in range(graphsize):
            raw_matrix.append(input())
        graph = convertmatrixtoadjlist(converttomatrix(raw_matrix))
        weightlist = [int(x) for x in input("Input a weight list: ").split()]
    elif ord(ch) in [71, 103, 143, 175]:
        graphsize = int(input("Input graph size: "))
        a = generatematrix(graphsize)
        weightlist = [random.randint(1, 10) for i in range(graphsize)]
        weightlist.sort()
        for row in a:
            print(' '.join(list(map(lambda x: str(x), row))))
            graph = convertmatrixtoadjlist(a)
    else:
        continue
    visited = [False] * graphsize
    used = [False] * len(weightlist)
    graphweight = [0] * graphsize
    for i in range(graphsize):
        if not visited[i]:
            dfs(graph, i, graphpath, visited)
    arclist = converttoarclist(graph)
    start_time = time.time()
    result, new_graph_weight = fullsearch(weightlist, graphpath, graphweight, used, 0)
    first_time = time.time()
    print("Full Search", "\n______________________________")
    print("Time needed: %.2f" % (first_time - start_time), 's.', sep='')
    print("Total count of branches/nodes: ", branchcount, iterations)
    print("Found Result:", result)
    print("Order of weights:", new_graph_weight, "\n")
    best_upper_bound = branchcount = iterations = 0
    start_time = time.time()
    result, new_graph_weight = search(weightlist, graphpath, graphweight, used, 0)
    print("Branches and Bounds Method", "\n______________________________")
    print("Time needed: %.2f" % (time.time() - start_time), 's.', sep='')
    print("Total count of branches/nodes: ", branchcount, iterations)
    print("Found Result:", result)
    print("Order of weights:", new_graph_weight)
    break
