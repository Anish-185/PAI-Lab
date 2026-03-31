import heapq
#Case Study: Smart Modular Furniture Layout Optimizer
#Problem Scenario

#Modern offices frequently reconfigure layouts for:

#Team expansion
#Meetings
#Hybrid work setups

#Manually rearranging furniture is:*/

#Time-consuming Inefficient Costly

GOAL_STATE = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]  # 0 represents empty space
]

# Heuristic: Manhattan Distance
def heuristic(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                goal_x = (value - 1) // 3
                goal_y = (value - 1) % 3
                distance += abs(i - goal_x) + abs(j - goal_y)
    return distance


def get_neighbors(state):
    neighbors = []
    # Find empty tile
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                x, y = i, j

    moves = [(-1,0),(1,0),(0,-1),(0,1)]

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)

    return neighbors


def state_to_tuple(state):
    return tuple(tuple(row) for row in state)


def a_star(start):
    open_list = []
    heapq.heappush(open_list, (0, start, []))
    visited = set()

    while open_list:
        cost, state, path = heapq.heappop(open_list)

        if state == GOAL_STATE:
            return path + [state]

        if state_to_tuple(state) in visited:
            continue

        visited.add(state_to_tuple(state))

        for neighbor in get_neighbors(state):
            g = len(path) + 1
            h = heuristic(neighbor)
            f = g + h
            heapq.heappush(open_list, (f, neighbor, path + [state]))

    return None


# Example: Furniture layout (0 = empty space)
start_state = [
    [1, 2, 3],
    [4, 0, 6],
    [7, 5, 8]
]

solution = a_star(start_state)

# Print steps
for step in solution:
    for row in step:
        print(row)
    print("-----")
