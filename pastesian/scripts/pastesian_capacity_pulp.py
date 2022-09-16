import pulp

# Define the model
mdl = pulp.LpProblem('Pastesian', sense=pulp.LpMinimize)

# Add variables
x = pulp.LpVariable.dicts(indices=[1, 2, 3, 4], cat=pulp.LpContinuous, lowBound=0, upBound=400, name='x')
y = pulp.LpVariable.dicts(indices=[1, 2, 3, 4], cat=pulp.LpContinuous, lowBound=0, upBound=100, name='y')
s = pulp.LpVariable.dicts(indices=[1, 2, 3], cat=pulp.LpContinuous, lowBound=0, upBound=200, name='s')

# Add Constraints
mdl.addConstraint(50 + x[1] == 200 + s[1], name='c1')
mdl.addConstraint(s[1] + x[2] == 350 + s[2], name='c2')
mdl.addConstraint(s[2] + x[3] == 150 + s[3], name='c3')
mdl.addConstraint(s[3] + x[4] == 250, name='c4')

mdl.addConstraint(x[1] - 300 <= y[1], name='c5')
mdl.addConstraint(x[2] - 300 <= y[2], name='c6')
mdl.addConstraint(x[3] - 300 <= y[3], name='c7')
mdl.addConstraint(x[4] - 300 <= y[4], name='c8')

# Set the objective function
mdl.setObjective(5.50*x[1] + 7.20*x[2] + 8.80*x[3] + 10.90*x[4] + 1.30*s[1] + 1.95*s[2] + 2.20*s[3]
                 + 0.35*(y[1] + y[2] + y[3] + y[4]))

# Optimize
mdl.solve()

# Retrieve the solution
x_sol = {t: x[t].value() for t in [1, 2, 3, 4]}
s_sol = {t: s[t].value() for t in [1, 2, 3]}
print(f'Amount to produce = {x_sol}')
print(f'Amount to store = {s_sol}')
