Simulation for collusion in an asymetric costs cournot competition game with n firms.

### notes
- The model is able to handle non linear demand and cost functions
- Firms can have asymmetric marginal and fixed costs.
- It is assumed that if firms have asymetric cost functions, they'll allocate production based on the inverse of their marginal costs, so the most efficient one will produce more than the least efficient ones.
- The firm which deviates can be set by changing firm_deviates_id inside the cournot class.

### structure

``class firm``: object which contains the firm's parameters, cost function and profit function to optimize.

``class market``: object which contains market parameters and defines inverse demand function.

``class model``: object which handles function optimization, used specifically to maximize profit and returning output

``class cournot``: the model

### how to use
No external libraries are required. To run the model, you need to define the market and firm objects, use them as arguments to the Cournot model instance, and finally call summary() to print the results. See the sample code:
```
    #define the market
    market_1 = market(100,2)

    #define the firms
    firm1 = firm('q1',5,0,market_1)
    firm2 = firm('q2',10,0,market_1)

    #define the cournot model
    model_cournot = cournot(market_1,[firm1,firm2])

    #run themodel and print results.
    model_cournot.summary()
```