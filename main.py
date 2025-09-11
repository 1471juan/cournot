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
    
    def get_function_InverseDemand(self,q:int)->int:
        #returns price
        return self.a - q
    
class cournot:
    def __init__(self, market_obj: market, firm_1: firm, firm_2: firm):
        self.firm_1=firm_1
        self.firm_2=firm_2
        self.market_obj = market_obj

    def get_bestresponse(self,a,q1,q2,c1,c2):
        #returns q1,q2
        return (a-q2-c1)/2, (a-q1-c2)/2,

    def get_quantity(self,a,c1,c2):
        #returns q1,q2
        return (a-(2*c1)+c2)/3, (a-(2*c2)+c1)/3
    
    def get_price(self,a,c1,c2):
        #returns market price
        q1, q2 = self.get_quantity(a,c1,c2)
        return self.market_obj.get_function_InverseDemand(q1+q2)
    
    def get_monopoly(self):
        #returns monopoly profit, quantity and price
        #we assume each firm produces half of the total monopoly quantities.
        M_Q = (self.market_obj.get_a()- 0.5*(self.firm_1.get_mc() + self.firm_2.get_mc()))/2
        M_P = self.market_obj.get_function_InverseDemand(M_Q)
        M_Z = (M_P*M_Q)-(self.firm_1.get_mc() + self.firm_2.get_mc())*M_Q - (self.firm_1.get_Fc() + self.firm_2.get_Fc())
        return M_Z, M_Q, M_P
    
    def get_deviation_profit(self):
        #returns deviation profit
        #we assume firm 1 deviates from collusion
        Z,collusion_Q,collussion_P=self.get_monopoly()
        a=self.market_obj.get_a()
        q1=(a-(collusion_Q/2)-(1/2)*(self.firm_1.get_mc() + self.firm_2.get_mc()))/2
        q=q1 + (collusion_Q/2)
        p=self.market_obj.get_function_InverseDemand(q)
        return p*q1 - self.firm_1.get_mc()*q1 - self.firm_1.get_Fc()
    
    def get_discountFactor(self,c_Z, m_Z, d_Z):
        return (d_Z-(m_Z/2))/(d_Z-c_Z)
    
    def summary(self):
        a=self.market_obj.get_a()
        c1=self.firm_1.get_mc()
        c2=self.firm_2.get_mc()
        q1,q2=self.get_quantity(a,c1,c2)
        p=self.get_price(a,c1,c2)

        m_Z, m_q, m_p=self.get_monopoly()
        d_Z=self.get_deviation_profit()
        delta=self.get_discountFactor(self.firm_1.get_profit(p,q1), m_Z, d_Z)
        print(f'firm 1 marginal cost: {c1}')
        print(f'firm 2 marginal cost: {c2}')
        print('--Results cournot--')
        print(f'firm 1 Q: {q1}')
        print(f'firm 2 Q: {q2}')
        print(f'market price: {p}')
        print(f'firm 1 profit: {self.firm_1.get_profit(p,q1)}')
        print(f'firm 2 profit: {self.firm_2.get_profit(p,q2)}')
        print(f'Total profits: {self.firm_1.get_profit(p,q1)+self.firm_2.get_profit(p,q2)}')
        print('--Results collusion--')
        print(f'collusion total profits: {m_Z}')
        print(f'collusion Q: {m_q}')
        print(f'collusion price: {m_p}')
        print(f'delta needed for collusion: {delta}')
        
def main():
    firm_1= firm(25,0)
    firm_2= firm(50,0)
    market_1=market(200,2)
    model=cournot(market_1,firm_1,firm_2)
    print(model.summary())

if __name__ == "__main__":
    main()