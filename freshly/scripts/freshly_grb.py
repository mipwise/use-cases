import gurobipy as gp

# Define the model
mdl = gp.Model('Freshly')

# Add variables
x = mdl.addVars([1, 2], vtype=gp.GRB.CONTINUOUS, name='x')

# Add Constraints
mdl.addConstr(54 * x[1] + 30 * x[2] <= 3*60*60, name='c1')
mdl.addConstr(0.450 * x[1] + 0.520 * x[2] <= 100/2, name='c2')
mdl.addConstr(0.520 * x[2] >= 30/2, name='c3')

# Set the objective function
mdl.setObjective(0.3825 * x[1] + 0.4056 * x[2], sense=gp.GRB.MAXIMIZE)

# Optimize
mdl.optimize()

# Retrieve the solution
print(f'Number of coconuts = {x[1].X}')
print(f'Kilograms of oranges = {x[2].X}')
