class firm:
    def __init__(self, mc, Fc):
        self.mc=mc
        self.Fc=Fc

    def get_mc(self):
        #returns marginal cost
        return self.mc
    def get_Fc(self):
        #returns fixed cost
        return self.Fc
    def get_profit(self,p,q):
        return (p - self.mc)*q - self.Fc

class market:
    def __init__(self, a, n):
        self.a=a
        self.n=n
    
    def get_a(self):
        #returns intercept
        return self.a
    
    def get_n(self):
        #returns number of firms
        return self.n
    
    def get_function_inverseDemand(self,q:int)->int:
        #returns price
        return self.a - q
    
class cournot:
    def __init__(self, market_obj: market, firms):
        self.market_obj = market_obj
        self.firms = firms

    def add_firm(self,firm_obj):
        self.firms.append(firm_obj)

    #def get_bestresponse(self,a,q1,q2,c1,c2):
        #returns q1,q2
    #    return (a-q2-c1)/2, (a-q1-c2)/2,
    
    def get_quantity(self):
        #returns list with q
        Q = []
        for i, f in enumerate(self.firms):
            mc_otherfirms = sum(k.get_mc() for j, k in enumerate(self.firms) if j != i)
            firm_quantity = (self.market_obj.get_a() - 2*f.get_mc() + mc_otherfirms) / (self.market_obj.get_n() + 1)
            Q.append(firm_quantity)
        return Q
    
    def get_price(self):
        #returns market price
        Q = self.get_quantity()
        return self.market_obj.get_function_inverseDemand(sum(Q))
        
    def get_monopoly(self):
        #returns monopoly profit, quantity and price
        #we assume each firm produces half of the total monopoly quantities.
        firm_quantity = self.market_obj.get_a()
        for f in self.firms:
            firm_quantity=firm_quantity-((f.get_mc()/self.market_obj.get_n()))
        M_Q = firm_quantity / 2
        M_P = self.market_obj.get_function_inverseDemand(M_Q)
        costs=0
        for f in self.firms:
            costs+=f.get_mc()*(M_Q/self.market_obj.get_n()) + f.get_Fc()
        M_Z = (M_P*M_Q) - costs
        return M_Z, M_Q, M_P
    
    def get_deviation_profit(self):
        #returns deviation profit
        #we assume firm 1(firms[0]) deviates from collusion
        Z,collusion_Q,collussion_P=self.get_monopoly()
        m_costs=0
        for f in self.firms:
            m_costs+=f.get_mc()
        q1=((self.market_obj.get_n() + 1) * self.market_obj.get_a() + (self.market_obj.get_n() - 1)
             * (m_costs/self.market_obj.get_n()) - 2 * self.market_obj.get_n() * self.firms[0].get_mc()) / (4 * self.market_obj.get_n())
        q = q1 + ((self.market_obj.get_n()-1)*collusion_Q/self.market_obj.get_n())
        p=self.market_obj.get_function_inverseDemand(q)
        return p*q1 - self.firms[0].get_mc() * q1 - self.firms[0].get_Fc()
    
    def get_discountFactor(self,c_Z, m_Z, d_Z):
        return (d_Z - (m_Z / self.market_obj.get_n() ) ) / (d_Z - c_Z)
    
    def summary(self):
        Q=self.get_quantity()
        p=self.get_price()
        m_Z, m_q, m_p=self.get_monopoly()
        d_Z=self.get_deviation_profit()
        delta=self.get_discountFactor(self.firms[0].get_profit(p,Q[0]), m_Z, d_Z)
        print('--Results cournot--')
        for i,f in enumerate(self.firms):
            print(f'firm {i} marginal cost: {f.get_mc()}')
            print(f'firm {i} Q: {Q[i]}')
            print(f'firm {i} profit: {f.get_profit(p,Q[i])}')
        print(f'market price: {p}')
        t_p=0
        for i,f in enumerate(self.firms):
            t_p+=f.get_profit(p,Q[i])
        print(f'Total profits: {t_p}')
        print('--Results collusion--')
        print(f'collusion total profits: {m_Z}')
        print(f'collusion Q: {m_q}')
        print(f'collusion price: {m_p}')
        print(f'delta needed for collusion: {delta}')

class model:
    def __init__(self):
        self.var = {}   
        self.par = {}   
        self.profits = {}  

    def add_firm(self, name):
        self.var[name] = {"value": 1}

    def add_profit(self, name, profit_function):
        self.profits[name] = profit_function

    def optimize(self, name, iterations=100):
        #approximates a partial derivative to maximize f
        for i in range(iterations):
            x = self.var[name]["value"]
            q = {name: v["value"] for name, v in self.var.items()}
            f = self.profits[name]
            #central difference estimate using this definition
            #(∂f/∂x ≈ (f(x+h) - f(x-h)) / (2h))
            h = 0.000001
            q[name] = x + h
            f_1 = f(**q, **self.par)
            q[name] = x - h
            f_2 = f(**q, **self.par)
            grad = (f_1 - f_2) / (2 * h)
            x_new = x + 0.01 * grad
            if x_new<0: x_new=0
            self.var[name]["value"] = x_new

    def get_output(self):
        i = 0
        while i < 1000:
            for firm in self.var:
                self.optimize(firm, 1)
            i+=1
        return {name: info["value"] for name, info in self.var.items()}
          
def demand(q1,q2):
    return 100 - (q1 + q2)

def profit_1(q1, q2):
    P = demand(q1,q2)
    return q1 * P - 25*q1*q1

def profit_2(q1, q2):
    P = demand(q1,q2)
    return q2 * P - 25*q2*q2

def main():
    firm_1= firm(25,0)
    firm_2= firm(50,0)
    firm_3= firm(30,0)
    market_1=market(200,3)
    model_cournot=cournot(market_1,[firm_1,firm_2,firm_3])
    model_cournot.summary()
    
    model_1 = model()
    model_1.add_firm("q1")
    model_1.add_firm("q2")
    model_1.add_profit("q1", profit_1)
    model_1.add_profit("q2", profit_2)
    print('--model 1--')
    print(model_1.get_output())

if __name__ == "__main__":
    main()