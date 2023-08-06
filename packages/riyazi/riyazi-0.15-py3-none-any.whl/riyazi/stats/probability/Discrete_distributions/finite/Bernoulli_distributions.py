__all__ = ['bernoulli']

import numpy as np
#created a bernoulli class
 
class bernoulli():
    def pmf(x,p):
        """
        probability mass function        
        """
        f = p**x*(1-p)**(1-x)
        return f
    
    def mean(p):
        """
        expected value of bernoulli random variable
        """
        return p
    
    def var(p):
        """
        variance of bernoulli random variable
        """
        return p*(1-p)
    
    def std(p):
        """
        standart deviation of bernoulli random variable
        """
        return bernoulli.var(p)**(1/2)
    
    def rvs(p,size=1):
        """
        random variates
        """
        rvs = np.array([])
        for i in range(0,size):
            if np.random.rand() <= p:
                a=1
                rvs = np.append(rvs,a)
            else:
                a=0
                rvs = np.append(rvs,a)
        return rvs

    def get_pdf(self, success: bool = True):
        
        """
        This function calculates the probability density function of the distribution for either success or failure
        :param success: Indicate whether the calculation is for success or failure; with 'true' indicating success and
        'false' indicating failure
        :return pdf: probability density function (float)
        """
        if success:
            x = 1
        else:
            x = 0

        pdf = round(self.p ** x * self.q ** (1 - x), 2)
        return pdf