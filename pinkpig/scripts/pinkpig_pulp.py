import pulp

# Define the model
mdl = pulp.LpProblem('PinkPig', sense=pulp.LpMinimize)

# Add variables
x = pulp.LpVariable.dicts(indices=[1, 2], cat=pulp.LpContinuous, lowBound=0, name='x')

# Add Constraints
mdl.addConstraint(0.77*x[1] + 0.66*x[2] >= 6.0, name='c1')
mdl.addConstraint(0.08*x[1] + 0.14*x[2] >= 0.9, name='c2')
mdl.addConstraint(0.77*x[1] + 0.66*x[2] <= 7.5, name='c3')
mdl.addConstraint(0.08*x[1] + 0.14*x[2] <= 1.6, name='c4')

# Set the objective function
mdl.setObjective(1.50*x[1] + 2.23*x[2])

# Optimize
mdl.solve()

# Retrieve the solution
print(f'Amount of rice = {x[1].value()}')
print(f'Amount of corn = {x[2].value()}')
