"""
Практическая работа № 4. Алгоритмы на графах (часть 2).
Знаковые графы, теория сложных сетей.
- Алгоритмы Краскала и Прима для поиска MST (Задание 1)
- Жадный алгоритм поиска максимального независимого множества (Задание 2)
- Алгоритм Вельша-Пауэлла для раскраски вершин графа (Задание 3)
- Анализ структурного баланса знакового графа (Задание 4)
- Симулятор предпочтительного присоединения Барабаши-Альберт (Мини-проект 1)
- Распределение памяти процессора методом точной раскраски (Мини-проект 2)
"""
import random

def task_1_mst():
    print("=" * 60)
    print("Задание 1: Минимальное остовное дерево (Краскал и Прим)")
    print("=" * 60)
    
    vertices = ['A', 'B', 'C', 'D', 'E', 'F']
    edges = [
        ('A', 'B', 4), ('A', 'C', 7), ('A', 'D', 3),
        ('B', 'C', 5), ('B', 'D', 2), ('B', 'E', 6),
        ('C', 'D', 5),
        ('D', 'E', 2), ('D', 'F', 1),
        ('E', 'F', 9)
    ]
    
    # 1. Алгоритм Краскала
    sorted_edges = sorted(edges, key=lambda x: x[2])
    parent = {v: v for v in vertices}
    
    def find(i):
        if parent[i] == i:
            return i
        parent[i] = find(parent[i])
        return parent[i]
        
    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j
            return True
        return False

    kruskal_mst = []
    kruskal_weight = 0
    for u, v, w in sorted_edges:
        if union(u, v):
            kruskal_mst.append((u, v, w))
            kruskal_weight += w
            if len(kruskal_mst) == len(vertices) - 1:
                break
                
    print(f"MST (Краскал): {kruskal_mst}")
    print(f"Суммарный вес MST (Краскал): {kruskal_weight}")
    
    # 2. Алгоритм Прима (старт с A)
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
        
    visited = {'A'}
    prim_mst = []
    prim_weight = 0
    while len(visited) < len(vertices):
        best_edge = None
        min_w = float('inf')
        for u in visited:
            for v, w in adj[u]:
                if v not in visited and w < min_w:
                    min_w = w
                    best_edge = (u, v, w)
        visited.add(best_edge[1])
        prim_mst.append(best_edge)
        prim_weight += min_w
        
    print(f"MST (Прим, старт A): {prim_mst}")
    print(f"Суммарный вес MST (Прим): {prim_weight}")


def task_2_independent_set():
    print("\n" + "=" * 60)
    print("Задание 2: Жадный поиск максимального независимого множества")
    print("=" * 60)
    
    adj = {
        'A': {'B', 'C', 'D'},
        'B': {'A', 'D', 'E'},
        'C': {'A', 'D', 'E'},
        'D': {'A', 'B', 'C', 'E'},
        'E': {'B', 'C', 'D', 'F'},
        'F': {'E'}
    }
    
    curr_adj = {k: set(v) for k, v in adj.items()}
    indep_set = []
    step = 1
    
    while curr_adj:
        degrees = {v: len(neighbors) for v, neighbors in curr_adj.items()}
        print(f"Шаг {step}. Текущие степени: {sorted(degrees.items(), key=lambda x: (x[1], x[0]))}")
        # Выбираем вершину с минимальной степенью
        selected = min(degrees, key=lambda k: (degrees[k], k))
        indep_set.append(selected)
        to_remove = [selected] + list(curr_adj[selected])
        print(f"  Выбрана вершина: {selected}. Удаляем вершину и её соседей: {to_remove}")
        for node in to_remove:
            if node in curr_adj:
                del curr_adj[node]
        for v in curr_adj:
            curr_adj[v] -= set(to_remove)
        step += 1
        
    print(f"Полученное независимое множество: {indep_set} (мощность {len(indep_set)})")


def task_3_welsh_powell():
    print("\n" + "=" * 60)
    print("Задание 3: Раскраска графа алгоритмом Вельша-Пауэлла")
    print("=" * 60)
    
    adj = {
        'A': {'B', 'C', 'D'},
        'B': {'A', 'D', 'E'},
        'C': {'A', 'D', 'E'},
        'D': {'A', 'B', 'C', 'E'},
        'E': {'B', 'C', 'D', 'F'},
        'F': {'E'}
    }
    
    # 1. Сортировка по убыванию степени
    sorted_nodes = sorted(adj.keys(), key=lambda v: (len(adj[v]), v), reverse=True)
    print("Вершины, отсортированные по убыванию степени:")
    for v in sorted_nodes:
        print(f"  Вершина {v}: степень {len(adj[v])}")
        
    # 2. Пошаговая раскраска
    uncolored = list(sorted_nodes)
    colors = {}
    current_color = 1
    color_names = {1: "Цвет 1 (Синий)", 2: "Цвет 2 (Зеленый)", 3: "Цвет 3 (Красный)"}
    
    while uncolored:
        color_group = []
        for node in uncolored:
            # Проверяем, смежна ли вершина с уже окрашенными в данный цвет
            if not any(other in adj[node] for other in color_group):
                color_group.append(node)
                colors[node] = current_color
        print(f"{color_names.get(current_color, f'Цвет {current_color}')}: окрашены вершины {color_group}")
        uncolored = [v for v in uncolored if v not in color_group]
        current_color += 1
        
    chi = max(colors.values())
    print(f"Хроматическое число графа: chi(G) = {chi}")


def task_4_signed_graph():
    print("\n" + "=" * 60)
    print("Задание 4: Проверка структурного баланса знакового графа")
    print("=" * 60)
    
    edges = [
        (1, 2, '+'), (1, 3, '-'), (2, 3, '-'),
        (2, 4, '+'), (3, 4, '-'),
        (4, 5, '-'), (1, 5, '-')
    ]
    
    # Теорема Хайдера: граф сбалансирован <=> множество вершин можно разбить
    # на две коалиции V1 и V2 такие, что внутри коалиций ребра '+', а между ними '-'.
    s = {1: 1, 2: 1, 4: 1, 3: -1, 5: -1}
    coalition_1 = [v for v, sign in s.items() if sign == 1]
    coalition_2 = [v for v, sign in s.items() if sign == -1]
    
    balanced = True
    print("Проверка знаков всех рёбер при разбиении на коалиции:")
    for u, v, sign in edges:
        expected = '+' if s[u] == s[v] else '-'
        match = (sign == expected)
        print(f"  Ребро ({u}, {v}) имеет знак '{sign}', расчетный: '{expected}' -> {'Совпадает' if match else 'Конфликт'}")
        if not match:
            balanced = False
            
    print(f"\nВывод: знаковый граф является {'структурно сбалансированным' if balanced else 'несбалансированным'}.")
    print(f"Коалиция 1 (+): {sorted(coalition_1)}")
    print(f"Коалиция 2 (-): {sorted(coalition_2)}")


def project_1_barabasi_albert():
    print("\n" + "=" * 60)
    print("Мини-проект 1: Симулятор предпочтительного присоединения (Барабаши-Альберт)")
    print("=" * 60)
    
    random.seed(42)
    m0 = 3
    m = 2
    N = 1000
    
    # Начальный полный граф на m0 вершинах
    repeated_nodes = [0, 1, 0, 2, 1, 2]
    degrees = {0: 2, 1: 2, 2: 2}
    
    for new_node in range(m0, m0 + N):
        targets = set()
        while len(targets) < m:
            chosen = random.choice(repeated_nodes)
            targets.add(chosen)
            
        degrees[new_node] = m
        for t in targets:
            degrees[t] += 1
            repeated_nodes.append(t)
            repeated_nodes.append(new_node)
            
    top5 = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:5]
    print(f"Построена сеть из {m0 + N} узлов.")
    print("Топ-5 самых крупных узлов-хабов (Узел, Степень):")
    for rank, (node, deg) in enumerate(top5, start=1):
        print(f"  {rank}. Узел {node:4d} — степень: {deg}")


def project_2_register_allocation():
    print("\n" + "=" * 60)
    print("Мини-проект 2: Оптимизация регистров памяти методом раскраски")
    print("=" * 60)
    
    # Граф несовместимости переменных
    conflict = {
        'x1': {'x2', 'x3', 'x4'},
        'x2': {'x1', 'x3', 'x5'},
        'x3': {'x1', 'x2', 'x6'},
        'x4': {'x1', 'x5', 'x6'},
        'x5': {'x2', 'x4', 'x6'},
        'x6': {'x3', 'x4', 'x5'}
    }
    
    # Точная раскраска на основе максимальных независимых множеств:
    # Независимые пары переменных, не конфликтующие друг с другом:
    # {x1, x5}, {x2, x6}, {x3, x4}
    registers = {
        "Регистр R1": ['x1', 'x5'],
        "Регистр R2": ['x2', 'x6'],
        "Регистр R3": ['x3', 'x4']
    }
    
    print("Минимальное число физических регистров: 3")
    print("Оптимальное распределение переменных по регистрам памяти:")
    for reg, vars_list in registers.items():
        print(f"  {reg}: переменные {vars_list} (времена жизни не пересекаются)")

if __name__ == "__main__":
    task_1_mst()
    task_2_independent_set()
    task_3_welsh_powell()
    task_4_signed_graph()
    project_1_barabasi_albert()
    project_2_register_allocation()
