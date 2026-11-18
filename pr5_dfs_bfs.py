"""
Практическая работа № 5. DFS и BFS: реализация и приложения.
- Задание 1. Обход графа DFS и BFS
- Задание 2. Поиск компонент связности и проверка двудольности
- Задание 3. Топологическая сортировка и поиск кратчайшего пути
"""
from collections import deque

def task_1_traversals():
    print("=" * 60)
    print("Задание 1: Обход графа DFS и BFS")
    print("=" * 60)
    
    graph = {
        1: [2, 3],
        2: [1, 4, 5],
        3: [1, 6, 7],
        4: [2, 8],
        5: [2, 8],
        6: [3, 9],
        7: [3, 9],
        8: [4, 5, 10],
        9: [6, 7, 10],
        10: [8, 9]
    }
    
    def dfs(g, start):
        visited, order = set(), []
        def visit(v):
            visited.add(v)
            order.append(v)
            for u in sorted(g[v]):
                if u not in visited:
                    visit(u)
        visit(start)
        return order
        
    def bfs(g, start):
        visited = {start}
        queue = deque([start])
        order = []
        while queue:
            v = queue.popleft()
            order.append(v)
            for u in sorted(g[v]):
                if u not in visited:
                    visited.add(u)
                    queue.append(u)
        return order

    print("Порядок обхода DFS (в глубину):", dfs(graph, 1))
    print("Порядок обхода BFS (в ширину): ", bfs(graph, 1))


def task_2_components_and_bipartite():
    print("\n" + "=" * 60)
    print("Задание 2: Компоненты связности и проверка двудольности")
    print("=" * 60)
    
    graph = {
        'A': ['B', 'C'], 'B': ['A', 'C'], 'C': ['A', 'B', 'D'],
        'D': ['C'],
        'E': ['F'], 'F': ['E', 'G'], 'G': ['F'],
        'H': [],
        'I': ['J', 'L'], 'J': ['I', 'K'], 'K': ['J', 'L'], 'L': ['I', 'K']
    }
    
    # Поиск компонент связности через DFS
    visited = set()
    components = []
    for node in sorted(graph.keys()):
        if node not in visited:
            comp = set()
            stack = [node]
            visited.add(node)
            while stack:
                curr = stack.pop()
                comp.add(curr)
                for neighbor in graph[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)
            components.append(comp)
            
    print(f"Найдено компонент связности: {len(components)}")
    
    # Проверка двудольности каждой компоненты через BFS-раскраску в 2 цвета
    for idx, comp in enumerate(components, start=1):
        color = {}
        start = next(iter(comp))
        color[start] = 0
        queue = deque([start])
        is_bipartite = True
        
        while queue and is_bipartite:
            curr = queue.popleft()
            for neighbor in graph[curr]:
                if neighbor not in color:
                    color[neighbor] = 1 - color[curr]
                    queue.append(neighbor)
                elif color[neighbor] == color[curr]:
                    is_bipartite = False
                    break
                    
        sorted_comp = sorted(list(comp))
        if is_bipartite:
            part0 = sorted([v for v, c in color.items() if c == 0])
            part1 = sorted([v for v, c in color.items() if c == 1])
            print(f"  Компонента {idx} {sorted_comp}: ДВУДОЛЬНАЯ (Доля 1: {part0}, Доля 2: {part1})")
        else:
            print(f"  Компонента {idx} {sorted_comp}: НЕ ДВУДОЛЬНАЯ (содержит нечётный цикл/треугольник)")


def task_3_topological_and_shortest():
    print("\n" + "=" * 60)
    print("Задание 3: Топологическая сортировка DAG и кратчайший путь")
    print("=" * 60)
    
    dag = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['E', 'F'],
        'D': ['G'],
        'E': ['G', 'H'],
        'F': ['G'],
        'G': ['H'],
        'H': []
    }
    
    # 1. Топологическая сортировка через DFS
    visited = set()
    order = []
    
    def dfs_topo(v):
        visited.add(v)
        for u in dag[v]:
            if u not in visited:
                dfs_topo(u)
        order.append(v)
        
    for node in sorted(dag.keys()):
        if node not in visited:
            dfs_topo(node)
            
    topo_order = order[::-1]
    print("Топологический порядок вершин DAG:", topo_order)
    
    # 2. Кратчайший путь от A до H через BFS
    start, finish = 'A', 'H'
    parent = {start: None}
    queue = deque([start])
    
    while queue:
        curr = queue.popleft()
        if curr == finish:
            break
        for neighbor in dag[curr]:
            if neighbor not in parent:
                parent[neighbor] = curr
                queue.append(neighbor)
                
    # Восстановление пути
    path = []
    curr = finish
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()
    
    print(f"Кратчайший путь от {start} до {finish}: {' -> '.join(path)}")
    print(f"Длина кратчайшего пути (в рёбрах): {len(path) - 1}")

if __name__ == "__main__":
    task_1_traversals()
    task_2_components_and_bipartite()
    task_3_topological_and_shortest()
