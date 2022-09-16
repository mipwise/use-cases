import pulp
import pandas as pd

dataset = {1: 'woodler_data_5_sites', 2: 'woodler_data_10_sites', 3: 'woodler_data_30_sites'}[2]
sub_tour_elimination_MTZ = False
sub_tour_elimination_DFJ = False
time_limit = 60
mip_gap = 0.05

dataset_path = f"../data/{dataset}.xlsx"
sites = pd.read_excel(dataset_path, sheet_name='sites')
trucks = pd.read_excel(dataset_path, sheet_name='trucks')
transit_matrix = pd.read_excel(dataset_path, sheet_name='transit_matrix')

I = set(sites['Site ID'])
td = dict(zip(zip(transit_matrix['Origin Site ID'], transit_matrix['Dest. Site ID']), transit_matrix['Distance (KM)']))
vc = trucks['Variable Cost (dollar/KM)'].iloc[0]  # variable cost of the first truck
depot_id = sites[sites['Site Name'] == 'DC']['Site ID'].iloc[0]

# keys of decision variables
x_keys = [(i, j) for i in I for j in I if i != j]

# Define the model
mdl = pulp.LpProblem('woodler', sense=pulp.LpMinimize)

# Add variables
x = pulp.LpVariable.dicts(indices=x_keys, cat=pulp.LpBinary, name='x')

# Add Constraints
# Flow balance
for h in I:
    mdl.addConstraint(sum(x.get((i, h), 0) for i in I) == sum(x.get((h, j), 0) for j in I), name=f'c4_{h}')

# Must visit every site
for j in I:
    mdl.addConstraint(sum(x.get((i, j), 0) for i in I) == 1, name=f'c5_{j}')

# Miller–Tucker–Zemlin (MTZ) sub-tour elimination constraints
if sub_tour_elimination_MTZ:
    u = pulp.LpVariable.dicts(indices=I, cat=pulp.LpInteger, lowBound=0, upBound=len(I)-1, name='u')
    for i, j in x_keys:
        if j != depot_id:
            mdl.addConstraint(u[i] - u[j] + 1 <= len(I) * (1 - x[i, j]), name=f'mtz_{i}_{j}')
else:
    u = None

# Dantzig–Fulkerson–Johnson (DFJ) sub-tour elimination constraints
if sub_tour_elimination_DFJ:
    # two-sites sub-tours
    for i, j in x_keys:
        mdl.addConstraint(x[i, j] + x.get((j, i), 0) <= 1, name=f'dfj_{i}_{j}')

# Set the objective function
variable_cost = sum(vc * td[i, j] * x[i, j] for i, j in x_keys)
mdl.setObjective(variable_cost)

# Optimize
status = mdl.solve(pulp.PULP_CBC_CMD(timeLimit=time_limit, gapRel=mip_gap))
if pulp.LpStatus[status] == 'Optimal':
    # Retrieve the solution
    x_sol = [key for key in x_keys if x[key].value() > 0.5]
    print(f'Total Cost: {round(variable_cost.value(), 2)}')
    print(f'x_sol: {x_sol}')
    if u:
        u_sol = [(u[i].value(), i) for i in I]
        u_sol = sorted(u_sol, key=lambda t: t[0])
        path = [i for _, i in u_sol]
        print(f'Path: {path}')
else:
    print(f'Optimization status: {pulp.LpStatus[status]}')
