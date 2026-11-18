"""
Практическая работа № 2. Алгоритм Дейкстры.
Задание 3 для самостоятельной работы и Задание 1 повышенной трудности:
- Нахождение кратчайшего пути от центрального склада S до ТЦ T.
- Нахождение кратчайших путей от склада S до всех складов логистической компании.
"""
import heapq

def dijkstra(graph, start):
    distances = {v: float('inf') for v in graph}
    distances[start] = 0
    previous = {v: None for v in graph}
    pq = [(0, start)]
    
    while pq:
        curr_dist, u = heapq.heappop(pq)
        if curr_dist > distances[u]:
            continue
            
        for v, weight in graph[u]:
            dist = curr_dist + weight
            if dist < distances[v]:
                distances[v] = dist
                previous[v] = u
                heapq.heappush(pq, (dist, v))
                
    return distances, previous

def reconstruct_path(previous, target):
    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        curr = previous[curr]
    return path[::-1]

def task_self_3():
    print("=" * 60)
    print("Задание 3: Маршрут доставки от склада S до торгового центра T")
    print("=" * 60)
    
    graph = {
        'S': [('A', 5), ('B', 10)],
        'A': [('C', 3), ('T', 12)],
        'B': [('C', 2)],
        'C': [('T', 4)],
        'T': []
    }
    
    dist, prev = dijkstra(graph, 'S')
    path = reconstruct_path(prev, 'T')
    
    print(f"Кратчайшее время доставки: {dist['T']} мин.")
    print(f"Оптимальный маршрут: {' -> '.join(path)}")


def task_advanced_1():
    print("\n" + "=" * 60)
    print("Задание повышенной трудности № 1: ЛогистикПро (до всех складов)")
    print("=" * 60)
    
    graph = {
        'S': [('A', 10), ('B', 15)],
        'A': [('C', 12), ('D', 15)],
        'B': [('E', 10)],
        'C': [('F', 5)],
        'D': [('F', 10), ('G', 20)],
        'E': [('G', 5)],
        'F': [('G', 10)],
        'G': []
    }
    
    dist, prev = dijkstra(graph, 'S')
    
    print("Результаты расчета кратчайших маршрутов от склада S:")
    for node in sorted(graph.keys()):
        path = reconstruct_path(prev, node)
        print(f"Склад {node:2s} | Кратчайшее время: {dist[node]:2d} мин. | Маршрут: {' -> '.join(path)}")

if __name__ == "__main__":
    task_self_3()
    task_advanced_1()
