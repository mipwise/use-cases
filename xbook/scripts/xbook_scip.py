from pathlib import Path

import pandas as pd
import pyscipopt as scip
from pyscipopt import quicksum as qs


cwd = Path(__file__).parent.resolve()
input_data_dir = cwd / 'input_data'


# Input Data
facilities_df = pd.read_csv(f'{input_data_dir}/facilities.csv')
stores_df = pd.read_csv(f'{input_data_dir}/stores.csv')
lanes_df = pd.read_csv(f'{input_data_dir}/transp_lanes.csv')

I = list(facilities_df['Facility ID'])
J = list(stores_df['Store ID'])

su = dict(zip(facilities_df['Facility ID'], facilities_df['Storage Capacity']))
sc = dict(zip(facilities_df['Facility ID'], facilities_df['Setup Cost']))
d = dict(zip(stores_df['Store ID'], stores_df['Demand']))
tc = dict(zip(
    zip(lanes_df['Origin Site ID'], lanes_df['Dest. Site ID']),
    lanes_df['Distance']
))

# Define the model
mdl = scip.Model('xbook')

# Add variables
x = {}
for i in I:
    for j in J:
        x[i, j] = mdl.addVar(vtype='C', lb=0, name=f'x_{i}_{j}')

y = {}
for i in I:
    y[i] = mdl.addVar(vtype='B', name=f'y_{i}')

# Add Constraints
# C1) Each facility can only deliver if it's operating:
for i in I:
    for j in J:
        mdl.addCons(x[i, j] <= min(su[i], d[j]) * y[i], name=f'C1_{i}_{j}')

# C2) Storage capacity of each facility:
for i in I:
    mdl.addCons(qs(x[i, j] for j in J) <= su[i], name=f'C2_{i}')

# C3) Demand must be satisfied:
for j in J:
    mdl.addCons(qs(x[i, j] for i in I) == d[j], name=f'C3_{j}')

# Set the objective function
transportation_cost = qs(tc[i, j] * x[i, j] for i in I for j in J)
setup_cost = qs(sc[i] * y[i] for i in I)
mdl.setObjective(transportation_cost + setup_cost, sense='minimize')

# Write problem
mdl.writeProblem('xbook.lp')

# Optimize
mdl.optimize()

# Retrieve the solution
x_sol = [(i, j, mdl.getVal(x[i, j])) for i in I for j in J if mdl.getVal(x[i, j]) > 1e-6]
y_sol = [(i, mdl.getVal(y[i])) for i in I]

print("Total Transportation Cost = ", mdl.getVal(transportation_cost))
print("Total Setup Cost = ", mdl.getVal(setup_cost))

# Create output tables
flow_df = pd.DataFrame(data=x_sol, columns=['Facility ID', 'Store ID', 'Flow'])
utilized_facilities_df = pd.DataFrame(data=y_sol, columns=['Facility ID', 'Utilized'])

output_dir = cwd / 'outputs'
flow_df.to_csv(output_dir / 'flow.csv', index=False)
utilized_facilities_df.to_csv(output_dir / 'utilized_facilities.csv', index=False)
