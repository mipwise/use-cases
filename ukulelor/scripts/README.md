# Ukulelor - Scripts
This directory contains implementation of optimization 
models that solve the use case.

- [ukulelor_pulp.py](ukulelor_pulp.py)

The appending to the name of each file indicates the optimization solver
used for the implementation of the mathematical formulation
provided in the [docs](../docs/README.md) directory.

- `cplex`: [CPLEX](https://www.ibm.com/analytics/cplex-optimizer)
- `grb`: [Gurobi](https://www.gurobi.com/)
- `mip`: [Python Mip](https://www.python-mip.com/)
- `pulp`: [PuLP-CBC](https://coin-or.github.io/pulp/)
- `scip`: [SCIP](https://www.scipopt.org/)