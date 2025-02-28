def isolated_component_deletion(matrix):
    rows, cols = len(matrix), len(matrix[0]) if matrix else 0
    to_replace = set()

    def is_isolated(r, c):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        count = 0
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                count += 1  # 超出边界视为与0相连
            elif matrix[nr][nc] == 0:
                count += 1
        return count == 3

    # 持续检查和替换
    while True:
        to_replace.clear()
        for r in range(rows):
            for c in range(cols):
                if matrix[r][c] == 1 and is_isolated(r, c):
                    to_replace.add((r, c))

        if not to_replace:
            break

        for r, c in to_replace:
            matrix[r][c] = 0

    return matrix


# 测试示例
matrix = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]
result = isolated_component_deletion(matrix)
for row in result:
    print(row)