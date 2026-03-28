from queue import PriorityQueue

# Grid size
ROWS = 10
COLS = 10

# Grid:
# 0 = normal
# 1 = obstacle
# 2 = traffic (higher cost)
grid = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,1,1,0,2,2,0,1,0,0],
    [0,0,0,0,0,2,0,1,0,0],
    [0,2,2,2,0,0,0,0,0,0],
    [0,0,0,2,0,1,1,1,0,0],
    [0,1,0,0,0,0,0,1,0,0],
    [0,1,0,1,1,1,0,0,0,0],
    [0,0,0,0,0,1,0,2,2,0],
    [0,1,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,2,2,0,0,0]
]

# Directions: up, down, left, right
directions = [(-1,0),(1,0),(0,-1),(0,1)]

# Heuristic (Manhattan distance)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Cost function
def get_cost(cell):
    if cell == 2:
        return 5  # traffic cost
    return 1      # normal cost

# A* Algorithm
def a_star(start, end):
    pq = PriorityQueue()
    pq.put((0, start))

    came_from = {}
    cost_so_far = {start: 0}

    while not pq.empty():
        _, current = pq.get()

        if current == end:
            break

        for d in directions:
            nx = current[0] + d[0]
            ny = current[1] + d[1]

            if 0 <= nx < ROWS and 0 <= ny < COLS:
                if grid[nx][ny] == 1:
                    continue  # obstacle

                new_cost = cost_so_far[current] + get_cost(grid[nx][ny])
                neighbor = (nx, ny)

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(end, neighbor)
                    pq.put((priority, neighbor))
                    came_from[neighbor] = current

    return reconstruct_path(came_from, start, end)

# Path reconstruction
def reconstruct_path(came_from, start, end):
    if start == end:
        return [start]

    if end not in came_from:
        return []

    current = end
    path = []

    while current != start:
        path.append(current)
        current = came_from[current]

    path.append(start)
    path.reverse()
    return path

# Calculate actual cost (including traffic)
def calculate_cost(path):
    cost = 0
    for (x, y) in path[1:]:
        cost += get_cost(grid[x][y])
    return cost

# Main function
def main():
    start = (0, 0)
    end = (9, 9)

    path = a_star(start, end)

    if not path:
        print("NO PATH")
    else:
        total_cost = calculate_cost(path)

        print("RESULT")
        print("------")
        print("START:", start)
        print("END:", end)
        print("PATH:", path)
        print("STEPS:", len(path))
        print("TOTAL COST:", total_cost)

# Entry point
if __name__ == "__main__":
    main()