class firm:
    def __init__(self,name, mc, Fc, market_obj):
        self.mc=mc
        self.Fc=Fc
        self.name=name
        self.market_obj=market_obj
        self.weigh=None

    def get_name(self):
        #returns name
        return self.name
    
    def get_mc(self):
        #returns marginal cost
        return self.mc
    
    def get_Fc(self):
        #returns fixed cost
        return self.Fc
    
    def set_weigh(self,w):
        #sets weigh
        self.weigh=w
    def get_weigh(self):
        #returns weigh
        return self.weigh
    
    def get_costs(self,q):
        #returns total cost
        return self.mc*q + self.Fc
    
    def get_profit(self,q,p):
        #returns profit
        return p*q - self.get_costs(q)
    
    def profit(self, **params):
        q = params[self.name]
        P = self.market_obj.get_inversedemand(sum(params.values()))
        return q*P - self.get_costs(q)

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
    
    def set_n(self,new_n):
        #set number of firms
        self.n=new_n
    
    def get_inversedemand(self, Q):
        #returns price
        return self.a - Q


class model:
    def __init__(self,r,iter):
        self.var = {}   
        self.par = {}   
        self.profits = {}  
        self.r=r
        self.iter=iter

    def add_firm(self, name):
        #add firm
        self.var[name] = {"value": 1}

    def add_profit(self, name, profit_function):
        #add profit function to a firm
        self.profits[name] = profit_function

    def integration(self, function,a,b,iterations=1000):
        size = (b - a) / iterations
        total = 0
        i=0
        while i < iterations:
            total += function(a + i*size) * size
            i+=1
        return total

    def optimize(self, name, iterations=100):
        #approximates a partial derivative to maximize f
        for i in range(iterations):
            x = self.var[name]["value"]
            q = {name: v["value"] for name, v in self.var.items()}
            f = self.profits[name]
            #central difference estimate using this definition
            #(df/dx = (f(x+h) - f(x-h)) / (2h))
            h = 0.00001
            q[name] = x + h
            f_1 = f(**q, **self.par)
            q[name] = x - h
            f_2 = f(**q, **self.par)
            grad = (f_1 - f_2) / (2 * h)
            x_new = x + self.r * grad
            if x_new<0: x_new=0
            self.var[name]["value"] = x_new

    def get_output(self):
        i = 0
        while i < self.iter:
            for firm in self.var:
                self.optimize(firm, 1)
            i+=1
        return {name: info["value"] for name, info in self.var.items()}
          
class cournot:
    def __init__(self, market_obj: market, firms):
        self.market_obj = market_obj
        self.firms = firms
        self.model_cournot=model(0.01,1000)
        self.model_monopoly=model(0.01,1000)
        self.model_deviation=model(0.01,1000)
        self.firms_mc=[]
        for f in self.firms: self.firms_mc.append(f.get_mc())
        self.flag_same_mc = self.check_mc()
        self.firm_deviates_id=0
        self.firm_deviates = self.firms[self.firm_deviates_id]

    def check_mc(self):
        #returns boolean indicating whether there are asymmetric costs
        for i in self.firms_mc:
            if i != self.firms_mc[0]:
                return False
        return True
    
    def add_firm(self,firm_obj):
        #adds firm to the model
        self.firms.append(firm_obj)
        self.market_obj.set_n(self.market_obj.get_n()+1)
        self.firms_mc.clear()
        for f in self.firms: self.firms_mc.append(f.get_mc())
        self.flag_same_mc = self.check_mc()

    def get_output(self):
        #returns list with q
        for firm in self.firms:
            self.model_cournot.add_firm(firm.get_name())
            self.model_cournot.add_profit(firm.get_name(), firm.profit)
        Q = []
        Q.extend(self.model_cournot.get_output().values())
        return Q

    def get_price(self):
        #returns market price
        Q = self.get_output()
        return self.market_obj.get_inversedemand(sum(Q))
        
    def weigh_firms(self):
        #calculate weigh for each firm based on the inverse of their marginal cost
        for f in self.firms:
            w=((1/f.get_mc()) / sum(1/mc for mc in self.firms_mc))
            f.set_weigh(w)
            #print(w)

    def get_sum_others_weighted(self):
        #returns the sum of the weighted collusion output for the firms that don't deviate.
        sum_others_weighted=0
        for f in self.firms:
            if f != self.firm_deviates:
                sum_others_weighted += self.m_Q * f.get_weigh()
        return sum_others_weighted
    
    def monopoly_profit(self,**params):
        #function to maximize in collusion
        total_q = params['Q']
        P = self.market_obj.get_inversedemand(total_q)
        if self.flag_same_mc:
            total_cost = sum(firm.get_mc() * (total_q / self.market_obj.get_n()) + firm.get_Fc() for firm in self.firms)
        else:
            total_cost=total_q*sum(firm.get_mc()*firm.get_weigh() for firm in self.firms) + sum(firm.get_Fc() for firm in self.firms)
        return P * total_q - total_cost
    
    def get_monopoly(self):
        #returns collusion profit, output and price
        self.weigh_firms() 
        self.model_monopoly.add_firm('Q')
        self.model_monopoly.add_profit('Q', self.monopoly_profit)
        output = self.model_monopoly.get_output() 
        m_Q = output['Q']
        m_P = self.market_obj.get_inversedemand(m_Q)
        if self.flag_same_mc:
            m_Z = m_P * m_Q - sum(firm.get_mc()*(m_Q / self.market_obj.get_n()) - firm.get_Fc() for firm in self.firms)
        else:
            m_Z = m_P * m_Q - (m_Q*sum(firm.get_mc()* firm.get_weigh() for firm in self.firms)) - sum(firm.get_Fc() for firm in self.firms)
        return m_Z,m_Q,m_P
    
    def deviation_profit(self, **params):
        #function to maximize in deviation
        q = params[self.firm_deviates.get_name()]  
        if self.flag_same_mc: 
            P = self.market_obj.get_inversedemand(q + (self.m_Q/self.market_obj.get_n())*(self.market_obj.get_n()-1))
        else:
            P = self.market_obj.get_inversedemand(q + (self.get_sum_others_weighted()))
        return (P-self.firm_deviates.get_mc()) * q - self.firm_deviates.get_Fc()
    
    def get_deviation_profit(self):
        #returns deviation profit
        self.m_Z, self.m_Q, self.m_P = self.get_monopoly() 
        self.model_deviation.add_firm(self.firm_deviates.get_name())
        self.model_deviation.add_profit(self.firm_deviates.get_name(), self.deviation_profit)
        output = self.model_deviation.get_output()
        d_Q = output[self.firm_deviates.get_name()]
        self.d_Q=d_Q
        if self.flag_same_mc:
            q_other = (self.market_obj.get_n()-1) * (self.m_Q / self.market_obj.get_n())
        else:
            q_other=self.get_sum_others_weighted()
        d_P = self.market_obj.get_inversedemand(d_Q+q_other)
        d_Z = (d_P -self.firm_deviates.get_mc()) * d_Q - self.firm_deviates.get_Fc()
        return d_Z

    def get_discountFactor(self,c_Z, d_Z):
        #returns discount factor needed for collusion to take place.
        if d_Z-c_Z!=0:
            if self.flag_same_mc:
                return (d_Z - (self.m_Z / self.market_obj.get_n() ) ) / (d_Z - c_Z)
            else:
                m_Zi=self.firms[0].get_profit(self.m_Q * self.firms[0].get_weigh(),self.m_P)
                return (d_Z - (m_Zi) ) / (d_Z - c_Z)
        else:
            return None
        
    def get_consumerSurplus(self, Q):
        A=self.model_cournot.integration(self.market_obj.get_inversedemand,0,Q,1000)
        B=self.market_obj.get_inversedemand(Q)*Q
        return A-B
    
    def get_elasticity(self, Q):
        P0 = self.market_obj.get_inversedemand(Q)
        P1 = self.market_obj.get_inversedemand(Q + 0.00001)
        return - (P0 / Q) / ((P1 - P0) / 0.00001)
    
    def summary(self):
        #run the model and print results
        Q=self.get_output()
        p=self.get_price()
        d_Z=self.get_deviation_profit()
        c_Zs=[]
        for i,firm in enumerate(self.firms):
            c_Zs.append(firm.get_profit(Q[i],p))
        c_Z=sum(c_Zs)
        delta=self.get_discountFactor(self.firm_deviates.get_profit(Q[self.firm_deviates_id],p), d_Z)
        print()
        print('----Market----')
        print(f'number of firms: {self.market_obj.get_n()}')
        print()
        print('----Results cournot----')
        for i,firm in enumerate(self.firms):
            print(f'firm {i} marginal cost: {firm.get_mc()}')
            print(f'firm {i} Q: {Q[i]}')
            print(f'firm {i} profit: {c_Zs[i]}')
        print(f'market price: {p}')
        t_p=0
        for i,firm in enumerate(self.firms):
            t_p+=c_Zs[i]
        print(f'Total profits: {t_p}')
        print(f'Consumer surplus: {self.get_consumerSurplus(c_Z)}')
        print(f'demand elasticity: {self.get_elasticity(c_Z)}')
        print()
        print('----Results collusion----')
        print(f'collusion total profits: {self.m_Z}')
        if self.flag_same_mc:
            print(f'collusion profits per firm: {self.m_Z/self.market_obj.get_n()}')
        else:
            for f in self.firms:
                m_Zi=f.get_profit(self.m_Q * f.get_weigh(),self.m_P)
                print(f'collusion profits per firm {f.get_name()}: {(m_Zi)}')
        print(f'collusion Q: {self.m_Q}')
        print(f'collusion price: {self.m_P}')
        print(f'Consumer surplus: {self.get_consumerSurplus(self.m_Q)}')
        print(f'demand elasticity: {self.get_elasticity(self.m_Q)}')
        print(f'deviation profit: {d_Z}')
        print(f'delta needed for collusion: {delta}')


def model_1():
    #define the market
    market_1 = market(100,2)

    #define the firms
    firm1 = firm('q1',5,0,market_1)
    firm2 = firm('q2',10,0,market_1)

    #define the cournot model
    model_cournot = cournot(market_1,[firm1,firm2])

    #run themodel and print results.
    model_cournot.summary()

    #add fims
    model_cournot.add_firm(firm('q3',4,0,market_1))
    model_cournot.summary()


def main():
    model_1()

if __name__ == "__main__":
    main()