import pulp

# Define the model
mdl = pulp.LpProblem('SoyKing', sense=pulp.LpMinimize)

# Add variables
keys = [(1, 1), (2, 1), (3, 1), (1, 2), (2, 2), (3, 2)]
x = pulp.LpVariable.dicts(indexs=keys, cat=pulp.LpContinuous, lowBound=0, name='x')

# Add Constraints
mdl.addConstraint(x[1, 1] + x[1, 2] <= 16, name='s1')
mdl.addConstraint(x[2, 1] + x[2, 2] <= 11, name='s2')
mdl.addConstraint(x[3, 1] + x[3, 2] <= 23, name='s3')
mdl.addConstraint(x[1, 1] + x[2, 1] + x[3, 1] >= 20, name='d1')
mdl.addConstraint(x[1, 2] + x[2, 2] + x[3, 2] >= 25, name='d2')

# Set the objective function
mdl.setObjective(66*x[1, 1] + 51*x[2, 1] + 73*x[3, 1] + 54*x[1, 2] + 82*x[2, 2] + 63*x[3, 2])

# Optimize
mdl.solve()

# Retrieve the solution
x_sol = {key: x[key].value() for key in keys}
print(f'Amount to produce = {x_sol}')
