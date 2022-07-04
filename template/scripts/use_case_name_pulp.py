import pulp

# Input data
I = ['P1', 'P2', 'P3']
J = ['L1', 'L2']
T = [1, 2, 3]
c = {('L1', 1): 1.0, ('L1', 2): 2.0, ('L1', 3): 1.0,
     ('L2', 1): 2.0, ('L2', 2): 1.0, ('L2', 3): 2.0}
d = {('P1', 1): 1, ('P1', 2): 2, ('P1', 3): 3,
     ('P2', 1): 1, ('P2', 2): 2, ('P2', 3): 3,
     ('P3', 1): 1, ('P3', 2): 2, ('P3', 3): 3}
x_keys = [(i, j, t) for i in I for j in J for t in T]
z_keys = list(c.keys())
M = max(sum(d[i, t] for i in I) for t in T)

# Define the model
mdl = pulp.LpProblem('UseCaseName', sense=pulp.LpMinimize)

# Add variables
x = pulp.LpVariable.dicts(indexs=x_keys, cat=pulp.LpContinuous, lowBound=0, name='x')
z = pulp.LpVariable.dicts(indexs=z_keys, cat=pulp.LpBinary, name='z')

# Add Constraints
# Demand for Product i must be met:
for i in I:
    for t in T:
        mdl.addConstraint(pulp.lpSum(x[i, j, t] for j in J) >= d[i, t], name=f'c1_{i}_{t}')
# There is production in Location j in Period t if and only if Location j is operational in Period t:
for j, t in z_keys:
    mdl.addConstraint(pulp.lpSum(x[i, j, t] for i in I) <= M * z[j, t], name=f'c2_{j}_{t}')

# Set the objective function
mdl.setObjective(pulp.lpSum(c[key] * z[key] for key in z_keys))

# Optimize
mdl.solve()

# Retrieve the solution
x_sol = {key: x[key].value() for key in x_keys}
z_sol = [key for key in z_keys if z[key].value() > 0.5]
print(f'Production: {x_sol}')
print(f'Open locations: {z_sol}')
