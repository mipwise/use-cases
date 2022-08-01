# MarketUp - Scripts
This directory contains implementation of optimization 
models that solve the use case.

- [marketup_pulp.py](marketup_pulp.py)
- [marketup_grb.py](marketup_grb.py)
- [marketup_cplex.py](marketup_cplex.py)

The appending to the name of each file indicates the optimization solver
used for the implementation of the mathematical formulation
provided in the [docs](../docs/README.md) directory.

- `cplex`: [CPLEX](https://www.ibm.com/analytics/cplex-optimizer)
- `grb`: [Gurobi](https://www.gurobi.com/)
- `mip`: [Python Mip](https://www.python-mip.com/)
- `pulp`: [PuLP-CBC](https://coin-or.github.io/pulp/)
- `scip`: [SCIP](https://www.scipopt.org/)