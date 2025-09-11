Simulation for collusion between n firms in cournot competition.

### Assumptions:
- The demand is linear with b=1 : p=a-q
- Firms can have asymmetric marginal and fixed costs.
- The marginal cost is constant.
- Firm 1(firms[0]) deviates from collusion

### Structure:

firm class represents a firm; stores marginal/fixed costs and computes profit.

market class stores intercept, number of firms n, and computes indirect demand.

cournot class simulates competition and collusion
get_quantity() returns cournot nash equilibrium outputs as a list
get_price() returns market price
get_monopoly() returns collusion quantity, price and profit
get_deviation_profit() returns profit of a deviating firm
get_discountFactor() returns minimum necessary discount factor for collusion
summary() – prints results
