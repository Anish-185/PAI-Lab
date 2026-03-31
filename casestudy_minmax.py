#Case Study: Smart Traffic Signal Control System
#Problem Scenario

#In busy urban areas, traffic congestion is a major issue.
#Traffic signals must decide:

#Which lane gets the green light
#How long to allow traffic flow

#However:

#Competing traffic directions “compete” for green time
#Poor decisions lead to congestion and delays

import math

# Example tree (traffic costs)
tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': 10,
    'E': 12,
    'F': 8,
    'G': 9
}

def minimax(node, depth, is_max, alpha, beta):
    # Leaf node
    if isinstance(tree[node], int):
        return tree[node]

    if is_max:
        max_eval = -math.inf
        for child in tree[node]:
            eval = minimax(child, depth+1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)

            if beta <= alpha:
                break  # Beta cut-off

        return max_eval
    else:
        min_eval = math.inf
        for child in tree[node]:
            eval = minimax(child, depth+1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)

            if beta <= alpha:
                break  # Alpha cut-off

        return min_eval


result = minimax('A', 0, True, -math.inf, math.inf)
print("Optimal Traffic Cost:", result)
