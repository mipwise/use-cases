"""
This is the most basic implementation of MarketUp formulation.

This version uses Gurobi as a solver.

Created by Rohit Karvekar (Aug, 22) for Mip Wise.
"""

import gurobipy as gp

# Input Data
# marketing channels
mc = {1: 'Print', 2: 'TV', 3: 'SEO', 4: 'Social Media'}
I = list(mc)
# expected ROI
r = {1: 1.16, 2: 1.09, 3: 1.06, 4: 1.14}
# expected market penetration
p = {1: 2.1, 2: 2.5, 3: 3.0, 4: 0.9}
# total budget
tb = 1_000_000
# print budget
pb = 100_000
# viewer target
vt = 1_500_000
# minimum conventional channel allocation
ca = 0.4

# Define the model
mdl = gp.Model('market_up')

# Add variables
x = mdl.addVars(I, vtype=gp.GRB.CONTINUOUS, name='x')

# Add Constraints
# C1) Can't exceed the total budget
mdl.addConstr(x.sum() <= tb, name='C1')
# C2) Minimum allocation to conventional channels
mdl.addConstr(sum(x[i] for i in [1, 2]) >= ca * tb, name='C2')
# C3) Can't exceed the print budget
mdl.addConstr(x[1] <= pb, name='C3')
# C4) Social Media investment must be at most three times SEO investment
mdl.addConstr(x[4] <= 3 * x[3], name='C4')
# C5) Reach minimum viewers target
mdl.addConstr(sum(p[i] * x[i] for i in I) >= vt, name='C5')

# Set the objective function
total_roi = sum(r[i] * x[i] for i in I)
mdl.setObjective(total_roi, sense=gp.GRB.MAXIMIZE)

# Optimize
mdl.optimize()

# Retrieve the solution
x_sol = {mc[i]: int(x[i].X) for i in I}
print(f'Total ROI: {total_roi.getValue()}')
print(f'Optimal budget allocation: {x_sol}')

