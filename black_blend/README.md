# Black Blend
- Statement of the use case: https://mipwise.com/use-cases/black-blend
- Mathematical formulation: [docs](docs/README.md)
- Implementations: [scripts](scripts/README.md)


## Statement
*Black Blend* is a Brazilian company that buys raw coffee grains, roasts them, 
and distribute to wholesalers.

The company buys raw grains from three suppliers, Mineiro, Goiano, and 
Paulista. The price of raw grains from each supplier and the respective weekly 
availability is given in the table below.

| Supplier ID | Supplier | Price ($/Kg) | Availability (Kg/Week) |
|:-----------:|:--------:|:------------:|:----------------------:|
|      1      | Mineiro  |     6.00     |          1000          |
|      2      |  Goiano  |     7.00     |          3000          |
|      3      | Paulista |     5.00     |          2000          |

Black Blend roasts and pack the grains in two facilities, Roast Bold and 
Hot Black. The processing cost and production capacity (maximum amount of 
raw grains that can be roasted per week) of each facility is given in the 
tables below.

| Factory ID |  Factory   | Processing Cost ($/Kg) | Capacity (Kg/Week) |
|:----------:|:----------:|:----------------------:|:------------------:|
|     1      | Roast Bold |         10.00          |        2500        |
|     2      | Hot Black  |         12.00          |        3000        |

Knowing that Black Blend sells roasted coffee for $25/Kg, and that one 
kilogram of raw coffee grains produces 0.8Kg of roasted coffee, how should
they plan production to maximize their profit?
