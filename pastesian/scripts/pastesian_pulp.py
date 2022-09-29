import pulp

# Define the model
mdl = pulp.LpProblem('Pastesian', sense=pulp.LpMinimize)

# Add variables
x = pulp.LpVariable.dicts(indices=[1, 2, 3, 4], cat=pulp.LpContinuous, lowBound=0, name='x')
s = pulp.LpVariable.dicts(indices=[1, 2, 3], cat=pulp.LpContinuous, lowBound=0, name='s')

# Add Constraints
mdl.addConstraint(50 + x[1] == 200 + s[1], name='c1')
mdl.addConstraint(s[1] + x[2] == 350 + s[2], name='c2')
mdl.addConstraint(s[2] + x[3] == 150 + s[3], name='c3')
mdl.addConstraint(s[3] + x[4] == 250, name='c4')

# Set the objective function
mdl.setObjective(5.50*x[1] + 7.20*x[2] + 8.80*x[3] + 10.90*x[4] + 1.30*s[1] + 1.95*s[2] + 2.20*s[3])

# Optimize
status_code = mdl.solve()

# Retrieve the solution
status = pulp.LpStatus[status_code]
if status == 'Optimal':
    print(f'Optimal solution found!')
    x_sol = {t: x[t].value() for t in [1, 2, 3, 4]}
    s_sol = {t: s[t].value() for t in [1, 2, 3]}
    print(f'Amount to produce = {x_sol}')
    print(f'Amount to store = {s_sol}')
else:
    print(f'Model is not optimal. Status: {status}')
