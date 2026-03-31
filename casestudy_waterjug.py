from collections import deque

#Case Study: Measuring Exact Water for a Medical Lab
Scenario

A small medical laboratory needs exactly 5 liters of distilled water to prepare a chemical solution.

However, they only have:

One 7-liter jug
One 3-liter jug
Unlimited water supply

There are no measurement markings on the jugs.

def water_jug(cap1, cap2, target):
    visited = set()
    queue = deque([(0, 0, [])])

    while queue:
        x, y, path = queue.popleft()

        if (x, y) in visited:
            continue

        visited.add((x, y))
        path = path + [(x, y)]

        if x == target or y == target:
            return path

        next_states = [
            (cap1, y),  # Fill Jug1
            (x, cap2),  # Fill Jug2
            (0, y),     # Empty Jug1
            (x, 0),     # Empty Jug2

            # Pour Jug1 → Jug2
            (x - min(x, cap2 - y), y + min(x, cap2 - y)),

            # Pour Jug2 → Jug1
            (x + min(y, cap1 - x), y - min(y, cap1 - x))
        ]

        for state in next_states:
            if state not in visited:
                queue.append((state[0], state[1], path))

    return None


# Case study: 7L and 3L jugs to get 5L
solution = water_jug(7, 3, 5)

print("Steps:")
for step in solution:
    print(step)
