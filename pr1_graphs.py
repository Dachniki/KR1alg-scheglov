"""
Практическая работа № 1. Графы и базовые структуры данных.
Задания повышенной трудности № 2 и 3:
- Построение матрицы смежности, матрицы инцидентности и списков смежности.
- Анализ эйлеровости графа и нахождение эйлерова цикла.
"""

def task_advanced_2():
    print("=" * 60)
    print("Задание повышенной трудности № 2: Матрицы и списки смежности")
    print("=" * 60)
    
    vertices = list(range(1, 10))
    edges = [
        (1, 2), (1, 3), (1, 5), (1, 9),
        (2, 3), (2, 6), (2, 8),
        (3, 4), (3, 9),
        (4, 5), (4, 7), (4, 8),
        (5, 6), (5, 7),
        (6, 8), (6, 9),
        (8, 9)
    ]
    
    n = len(vertices)
    m = len(edges)
    
    # 1. Матрица смежности
    adj_matrix = [[0] * n for _ in range(n)]
    for u, v in edges:
        adj_matrix[u - 1][v - 1] = 1
        adj_matrix[v - 1][u - 1] = 1
        
    print("\nМатрица смежности (9x9):")
    print("   " + " ".join(f"{v:2d}" for v in vertices))
    for i, row in enumerate(adj_matrix, start=1):
        print(f"{i:2d} " + " ".join(f"{val:2d}" for val in row))
        
    # 2. Матрица инцидентности
    inc_matrix = [[0] * m for _ in range(n)]
    for e_idx, (u, v) in enumerate(edges):
        inc_matrix[u - 1][e_idx] = 1
        inc_matrix[v - 1][e_idx] = 1
        
    print(f"\nМатрица инцидентности (9 вершин x {m} рёбер):")
    header = "   " + " ".join(f"e{j+1:02d}" for j in range(m))
    print(header)
    for i, row in enumerate(inc_matrix, start=1):
        print(f"{i:2d} " + "   ".join(f"{val}" for val in row))
        
    # 3. Списки смежности
    adj_list = {v: [] for v in vertices}
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
        
    print("\nСписки смежности:")
    for v in vertices:
        adj_list[v].sort()
        print(f"Вершина {v}: {adj_list[v]}")


def task_advanced_3():
    print("\n" + "=" * 60)
    print("Задание повышенной трудности № 3: Проверка эйлеровости графа")
    print("=" * 60)
    
    vertices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    edges = [
        ('A', 'B'), ('A', 'C'), ('A', 'D'),
        ('B', 'C'), ('B', 'E'),
        ('C', 'D'), ('C', 'F'),
        ('D', 'G'),
        ('E', 'F'), ('E', 'H'),
        ('F', 'G'), ('F', 'H'),
        ('G', 'H')
    ]
    
    degrees = {v: 0 for v in vertices}
    adj = {v: [] for v in vertices}
    for u, v in edges:
        degrees[u] += 1
        degrees[v] += 1
        adj[u].append(v)
        adj[v].append(u)
        
    print("Степени вершин:")
    odd_vertices = []
    for v in vertices:
        print(f"deg({v}) = {degrees[v]}", end="; ")
        if degrees[v] % 2 != 0:
            odd_vertices.append(v)
    print()
    
    print(f"\nВершины с нечётными степенями: {odd_vertices}")
    if odd_vertices:
        print("Граф НЕ является эйлеровым, так как содержит вершины нечётной степени.")
        print(f"Для превращения графа в эйлеров требуется соединить нечётные вершины парами.")
        print(f"Количество нечётных вершин: {len(odd_vertices)}. Минимально нужно добавить {len(odd_vertices) // 2} рёбер.")
    else:
        print("Граф является эйлеровым.")

if __name__ == "__main__":
    task_advanced_2()
    task_advanced_3()
