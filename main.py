import cournot_sim as cs

def model_1():
    #define the market
    market_1 = cs.market(100,2)

    #define the firms
    firm1 = cs.firm('q1',5,0,market_1)
    firm2 = cs.firm('q2',10,0,market_1)

    #define the cournot model
    model_cournot = cs.cournot(market_1,[firm1,firm2])

    #run themodel and print results.
    model_cournot.summary()

    #add firms
    model_cournot.add_firm(cs.firm('q3',4,0,market_1))
    model_cournot.summary()

def main():
    model_1()

if __name__ == "__main__":
    main()