import pyscipopt as scip
from pyscipopt import quicksum as qs


# Input Data
# products
I = ['freezip', 'sprinter']
# periods
T = [1, 2, 3]
# demand, units
d = {
    ('freezip', 1): 15300, ('freezip', 2): 11200, ('freezip', 3): 13000,
    ('sprinter', 1): 14000, ('sprinter', 2): 12500, ('sprinter', 3): 15800
}
# opening inventory, units
oi = {'freezip': 3000, 'sprinter': 2500}
# production rate, units/hour
pr = {'freezip': 1.2 * 60, 'sprinter': 1.4 * 60}
# holding cost, dollars
hc = {1: 0.12, 2: 0.13, 3: 0.10}
# production capacity (upper bound), hours
pu = {1: 465, 2: 320, 3: 315}
# production costs, dollars/unit
pc = {'freezip': 3, 'sprinter': 2.8}

# Define the model
mdl = scip.Model('frisbee_square')

# Add variables
x, y = {}, {}
for i in I:
    for t in T:
        x[i, t] = mdl.addVar(vtype='I', lb=0, name=f'x_{i}_{t}')
        y[i, t] = mdl.addVar(vtype='I', lb=0, name=f'y_{i}_{t}')

# Add Constraints
# C1) Flow balance
for i in I:
    mdl.addCons(
        y[i, 1] == oi[i] + x[i, 1] - d[i, 1],
        name=f'C1_{i}_{1}'
    )
    for t in T[1:]:
        mdl.addCons(
            y[i, t] == y[i, t-1] + x[i, t] - d[i, t],
            name=f'C1_{i}_{t}'
        )

# C2) Production capacity
for t in T:
    mdl.addCons(
        qs(round(1 / pr[i], 4) * x[i, t] for i in I) <= pu[t],  # round 1/pr to avoid numerical issues
        name=f'C2_{t}'
    )

# Set the objective function
production_cost = qs(pc[i] * x[i, t] for i in I for t in T)
holding_cost = qs(hc[t] * y[i, t] for i in I for t in T)
mdl.setObjective(production_cost + holding_cost, sense='minimize')

# Write problem
mdl.writeProblem('frisbee_square.lp')

# Optimize
mdl.optimize()

# Retrieve the solution
x_sol = [(i, t, mdl.getVal(var)) for (i, t), var in x.items()]
y_sol = [(i, t, mdl.getVal(var)) for (i, t), var in y.items()]
print()
print(f"Production cost: {mdl.getVal(production_cost):.2f}")
print(f"Holding cost: {mdl.getVal(holding_cost):.2f}")
print(f"Total cost: {mdl.getObjVal():.2f}")
print(f"x_sol:\n{x_sol}")
print(f"y_sol:\n{y_sol}")
