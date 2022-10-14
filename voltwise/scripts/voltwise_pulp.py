import pulp

# Input Data
# tasks
I = [1, 2, 3, 4, 5, 6]
# regular completion time
r = {1: 23, 2: 20, 3: 27, 4: 9, 5: 19, 6: 21}
# regular cost
c = {1: 270, 2: 165, 3: 270, 4: 158, 5: 146, 6: 80}
# extra cost (for expedition)
ce = {1: 340, 2: 225, 3: 370, 4: 170, 5: 195, 6: 150}
# expedition upper bound
eu = {1: 3, 2: 2, 3: 5, 4: 2, 5: 3, 6: 0}
# predecessor-successor list
p = [(1, 3), (2, 3), (3, 4), (4, 5), (4, 6)]
# Maximum time to complete the project
tu = 75

# Define the model
mdl = pulp.LpProblem('voltwise', sense=pulp.LpMinimize)

# Add variables
x = pulp.LpVariable.dicts(indices=I, cat=pulp.LpContinuous, lowBound=0, name='x')
y = pulp.LpVariable.dicts(indices=I, cat=pulp.LpContinuous, lowBound=0, name='y')

# Add Constraints
# C1) Task j can only start after Task i is complete:
for (i, j) in p:
    mdl.addConstraint(x[i] + y[i] <= x[j], name=f'c1_{i}_{j}')
# C2) Maximum time to complete task i:
for i in I:
    mdl.addConstraint(y[i] <= r[i], name=f'c2_{i}')
# C3) Minimum time to complete task i:
for i in I:
    mdl.addConstraint(r[i] - eu[i] <= y[i], name=f'c3_{i}')
# C4) Maximum time to complete the project:
for i in I:
    mdl.addConstraint(x[i] + y[i] <= tu, name=f'c4_{i}')

# Set the objective function
regular_cost = sum(c[i] * y[i] for i in I)
expedition_cost = sum(ce[i]*(r[i]-y[i]) for i in I)
mdl.setObjective(regular_cost + expedition_cost)

# Optimize
mdl.solve()

# Retrieve the solution
print(f'Total Regular Cost = {regular_cost.value()}')
print(f'Total Expedition Cost = {expedition_cost.value()}')
x_sol = {i: x[i].value() for i in I}
y_sol = {i: y[i].value() for i in I}
z_sol = {i: r[i] - y[i].value() for i in I}
print(f'Starting time   = {x_sol}')
print(f'Total time      = {y_sol}')
print(f'Expedition time = {z_sol}')
