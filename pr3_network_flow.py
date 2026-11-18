"""
Практическая работа № 3. Нахождение максимального потока и минимального разреза.
Задание повышенной трудности № 4:
- Реализация алгоритма Эдмондса-Карпа (BFS в остаточной сети).
- Нахождение максимального потока и минимального разреза сети.
"""
from collections import deque

def edmonds_karp(capacity, source, sink, nodes):
    # Инициализация остаточной сети
    flow = {u: {v: 0 for v in nodes} for u in nodes}
    total_flow = 0
    iteration = 1
    
    print("=" * 60)
    print(f"Поиск максимального потока из {source} в {sink} (алгоритм Эдмондса-Карпа)")
    print("=" * 60)
    
    while True:
        # Поиск кратчайшего увеличивающего пути с помощью BFS
        parent = {u: None for u in nodes}
        visited = {source}
        queue = deque([source])
        
        while queue:
            curr = queue.popleft()
            if curr == sink:
                break
            for nxt in nodes:
                residual = capacity[curr][nxt] - flow[curr][nxt]
                if nxt not in visited and residual > 0:
                    visited.add(nxt)
                    parent[nxt] = curr
                    queue.append(nxt)
                    
        # Если путь в сток не найден, поток максимален
        if sink not in visited:
            print("\nУвеличивающих путей в остаточной сети больше нет.")
            break
            
        # Определение бутылочного горлышка (минимальной остаточной пропускной способности)
        path = []
        curr = sink
        bottleneck = float('inf')
        while curr != source:
            p = parent[curr]
            bottleneck = min(bottleneck, capacity[p][curr] - flow[p][curr])
            path.append(curr)
            curr = p
        path.append(source)
        path.reverse()
        
        # Увеличение потока вдоль пути
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            flow[u][v] += bottleneck
            flow[v][u] -= bottleneck
            
        total_flow += bottleneck
        path_str = " -> ".join(path)
        print(f"Итерация {iteration}: путь [{path_str}], пропускная способность = {bottleneck}, накопленный поток = {total_flow}")
        iteration += 1

    # Нахождение минимального разреза (S-компонента и T-компонента)
    # Вершины, достижимые из source в остаточной сети
    visited_cut = {source}
    q = deque([source])
    while q:
        curr = q.popleft()
        for nxt in nodes:
            if nxt not in visited_cut and (capacity[curr][nxt] - flow[curr][nxt]) > 0:
                visited_cut.add(nxt)
                q.append(nxt)
                
    s_cut = visited_cut
    t_cut = set(nodes) - s_cut
    
    # Ребра разреза (из S-части в T-часть)
    cut_edges = []
    cut_capacity = 0
    for u in s_cut:
        for v in t_cut:
            if capacity[u][v] > 0:
                cut_edges.append((u, v, capacity[u][v]))
                cut_capacity += capacity[u][v]
                
    return total_flow, flow, s_cut, t_cut, cut_edges, cut_capacity

def main():
    nodes = ['S', 'A', 'B', 'C', 'D', 'T']
    capacity = {u: {v: 0 for v in nodes} for u in nodes}
    
    # Задание сети согласно условию Задания повышенной трудности № 4
    edges = [
        ('S', 'A', 10),
        ('S', 'B', 5),
        ('A', 'C', 9),
        ('B', 'C', 4),
        ('B', 'D', 8),
        ('C', 'T', 10),
        ('D', 'T', 10)
    ]
    for u, v, c in edges:
        capacity[u][v] = c
        
    max_flow, flow, s_cut, t_cut, cut_edges, cut_cap = edmonds_karp(capacity, 'S', 'T', nodes)
    
    print("\n" + "=" * 60)
    print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
    print("=" * 60)
    print(f"Максимальный поток: {max_flow}")
    print("\nФактическое распределение потока по исходным рёбрам:")
    for u, v, c in edges:
        print(f"  Ребро ({u} -> {v}): поток {flow[u][v]} / вместимость {c}")
        
    print(f"\nМинимальный разрез (теорема Форда-Фалкерсона):")
    print(f"  Множество истока S: {sorted(list(s_cut))}")
    print(f"  Множество стока T: {sorted(list(t_cut))}")
    print(f"  Рёбра, пересекающие разрез:")
    for u, v, c in cut_edges:
        print(f"    ({u} -> {v}) с пропускной способностью {c}")
    print(f"  Пропускная способность разреза: {cut_cap} (равна максимальному потоку {max_flow})")

if __name__ == "__main__":
    main()
