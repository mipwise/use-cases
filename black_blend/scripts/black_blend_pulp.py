import pulp

# Input data
x_keys = [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1), (3, 2)]

# Build optimization model
mdl = pulp.LpProblem("BlackBland", sense=pulp.LpMaximize)

# Add decision variables
x = pulp.LpVariable.dicts(indices=x_keys, cat=pulp.LpContinuous, lowBound=0.0, name='x')

# Add constraints
# capacity of Supplier 1:
mdl.addConstraint(x[1, 1] + x[1, 2] <= 1000, name=f'cs_1')
# capacity of Supplier 2:
mdl.addConstraint(x[2, 1] + x[2, 2] <= 3000, name=f'cs_2')
# capacity of Supplier 3:
mdl.addConstraint(x[3, 1] + x[3, 2] <= 2000, name=f'cs_3')
# capacity of Facility 1:
mdl.addConstraint(x[1, 1] + x[2, 1] + x[3, 1] <= 2500, name=f'cf_1')
# capacity of Facility 2:
mdl.addConstraint(x[1, 2] + x[2, 2] + x[3, 2] <= 3000, name=f'cf_2')

# Set objective function
revenue = 0.8 * 25 * pulp.lpSum(x[i, j] for i, j in x_keys)
procurement_cost = 6*(x[1, 1] + x[1, 2]) + 7*(x[2, 1] + x[2, 2]) + 5*(x[3, 1] + x[3, 2])
processing_cost = 10*(x[1, 1] + x[2, 1] + x[3, 1]) + 12*(x[1, 2] + x[2, 2] + x[3, 2])
mdl.setObjective(revenue - procurement_cost - processing_cost)
# mdl.setObjective(4*x[1, 1] + 2*x[1, 2] + 3*x[2, 1] + x[2, 2] + 5*x[3, 1] + 3*x[3, 2])

# Optimize and retrieve the solution
mdl.solve()
status = mdl.solve()
status = pulp.LpStatus[status]
if status == 'Optimal':
    x_sol = {(i, j): var.value() for (i, j), var in x.items() if var.value() > 1e-5}
    print(f'Optimal solution found!')
    print(f'Revenue = {revenue.value()}')
    print(f'Procurement Cost = {procurement_cost.value()}')
    print(f'Processing Cost = {processing_cost.value()}')
    print('Flows:\n', x_sol)
else:
    x_sol = None
    print(f'Model is not optimal. Status: {status}')

