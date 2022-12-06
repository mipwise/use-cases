import pulp

# Input Data
# retailers
I = [1, 2, 3, 4, 5, 6, 7]
# price
p = {1: 47, 2: 65, 3: 70, 4: 68, 5: 46, 6: 78, 7: 55}
# demand
d = {1: 230, 2: 150, 3: 270, 4: 90, 5: 190, 6: 55, 7: 120}
# production upper bound
pu = 650
# shipment lower bound
sl = 50
# penalty (num. of units)
pn = 20

# Define the model
mdl = pulp.LpProblem('ukulelor', sense=pulp.LpMaximize)

# Add variables
x = pulp.LpVariable.dicts(indices=I, cat=pulp.LpInteger, name='x', lowBound=0)
z = pulp.LpVariable.dicts(indices=I, cat=pulp.LpBinary, name='z')

# Add Constraints
mdl.addConstraint(pulp.lpSum(x) <= pu, name='max_avty')
for i in I:
    mdl.addConstraint(sl * z[i] <= x[i], name=f'at_least_{i}')
    mdl.addConstraint(x[i] <= d[i] * z[i], name=f'at_most_{i}')

# Set the objective function
revenue = sum(p[i] * x[i] for i in I)
penalty = sum((pn * p[i]) * (1 - z[i]) for i in I)
mdl.setObjective(revenue - penalty)

# Optimize
mdl.solve()

# Retrieve the solution
x_sol = {i: int(x[i].value()) for i in I}
print(f'x = {x_sol}')
print(f'revenue: {revenue.value()}')
print(f'penalty: {penalty.value()}')