# Case Study: Smart Meeting Room Scheduler
# Problem Scenario

#A company has:

#Multiple meeting rooms
#Several teams
#Limited time slots

#Conflicts arise when:

#Two teams want the same room at the same time
#Certain rooms lack required facilities (projector, capacity, etc.) 

# Variables
meetings = ["M1", "M2", "M3"]

# Domains: (Room, Time)
domains = {
    "M1": [("R1", "T1"), ("R1", "T2")],  # Needs projector
    "M2": [("R1", "T1"), ("R1", "T2"), ("R2", "T1"), ("R2", "T2")],
    "M3": [("R1", "T1"), ("R1", "T2"), ("R2", "T1"), ("R2", "T2")]
}

# Constraint checking
def is_valid(assignment, meeting, value):
    room, time = value

    for m, (r, t) in assignment.items():
        # Constraint 1: No same room at same time
        if r == room and t == time:
            return False

        # Constraint 2: M2 and M3 cannot be same time
        if (m == "M2" and meeting == "M3") or (m == "M3" and meeting == "M2"):
            if t == time:
                return False

    return True


def backtrack(assignment):
    # If all meetings assigned
    if len(assignment) == len(meetings):
        return assignment

    # Select unassigned variable
    unassigned = [m for m in meetings if m not in assignment][0]

    for value in domains[unassigned]:
        if is_valid(assignment, unassigned, value):
            assignment[unassigned] = value

            result = backtrack(assignment)
            if result:
                return result

            del assignment[unassigned]  # Backtrack

    return None


solution = backtrack({})

print("Final Schedule:")
for meeting, slot in solution.items():
    print(meeting, "→", slot)
