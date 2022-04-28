import pulp

# Define the model
mdl = pulp.LpProblem('Freshly', sense=pulp.LpMaximize)

# Add variables
x = pulp.LpVariable.dicts(indexs=[1, 2], cat=pulp.LpContinuous, lowBound=0, name='x')

# Add Constraints
mdl.addConstraint(54 * x[1] + 30 * x[2] <= 3*60*60, name='c1')
mdl.addConstraint(0.450 * x[1] + 0.520 * x[2] <= 100/2, name='c2')
mdl.addConstraint(0.520 * x[2] >= 30/2, name='c3')

# Set the objective function
mdl.setObjective(0.3825 * x[1] + 0.4056 * x[2])

# Optimize
mdl.solve()

# Retrieve the solution
print(f'Number of coconuts = {x[1].value()}')
print(f'Kilograms of oranges = {x[2].value()}')
