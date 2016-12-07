import random as rd


def convertmatrixtoadjlist(matrix):
    """
    Конвертирует матрицу смежностей в список смежных вершин
    :param matrix: матрица (двумерный массив)
    :return: список смежных вершин
    """
    adj_list = []
    for row in matrix:
        adj = []
        for col_index, element in enumerate(row):
            if element == 1:
                adj.append(col_index)
        adj_list.append(adj)
    return adj_list


def converttomatrix(strings):
    """
    Конвертирует список строк с ввода в матрицу
    :param strings: список строк
    :return: матрица (двумерный массив)
    """
    matrix = []
    for string in strings:
        perf = [int(x) for x in string.split()]
        matrix.append(perf)
    return matrix


def generatematrix(size):
    """
    Генерирует квадратную матрицу, состоящих из {0,1} порядка size
    :param size: число, размер матрицы
    :return: матрица в виде списка списков (двумерный массив)
    """
    return [[rd.randint(0, 1) for i in range(size)] for j in range(size)]


def converttoarclist(_adj_list):
    """
    Преобразует список смежных вершин в список ребер
    :param _adj_list: список смежностей
    :return: список кортежей вида (a,b)
    """
    arc_list = []
    for index, adj_vertexes in enumerate(_adj_list):
        for vertex in adj_vertexes:
            arc_list.append((index, vertex))
    return arc_list
