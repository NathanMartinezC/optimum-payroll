class PayrollItem:
    lowerIsr = 0
    upperIsr = 0
    lowerSubsidy = 0
    upperSubsidy = 0
    fixedTax = 0
    additionalFactor = 0
    isr = 0
    J = 0
    phi = 0
    sbc = 0
    christmasBonus = 15
    vacations = 6
    quotedDays = 365
    vacationFactor = 0.25
    integrationFactor = 0
    dailySalary = 0
    subsidy = 0
    uma = 86.88

    def __init__(self, salary, payrollDaysFactor):
        self.salary = salary
        self.payrollDaysFactor = payrollDaysFactor
        
        #Initialization
        self.getIsrFactors()
        self.getIsr()
        self.getSbc()
        self.getSubsidy()

    
    def getIsrFactors(self):
        lowerLimitsIsr = [0.01, 578.53, 4910.19, 8629.21, 10031.08, 12009.95, 24222.32, 38177.70, 72887.51, 97183.34, 291550.01]
        upperLimitsIsr = [578.52, 4910.18, 8629.20, 10031.07, 12009.94, 24222.31, 38177.69, 72887.50, 97183.33, 291550.00, 999999.00]
        fixedTaxesIsr = [0.00, 11.11, 288.33, 692.96, 917.26, 1271.87, 3880.44, 7162.74, 17575.69, 25350.35, 91435.02]
        factorsIsr = [1.92, 6.40, 10.88, 16.00, 17.92, 21.36, 23.52, 30.00, 32.00, 34.00, 35.00]

        for i, lower in enumerate(lowerLimitsIsr):
            upper = upperLimitsIsr[i]
            if self.salary >= lower and self.salary <= upper:
                self.lowerIsr = lowerLimitsIsr[i]
                self.upperIsr = upperLimitsIsr[i]
                self.fixedTax = fixedTaxesIsr[i]
                self.additionalFactor = factorsIsr[i]/100
                break
            else:
                pass
        

    def getIsr(self):
        self.isr = (self.salary - self.lowerIsr) * self.additionalFactor + self.fixedTax

    def getSbc(self):
        self.integrationFactor = (1/self.quotedDays) * (self.vacations * self.vacationFactor + self.quotedDays + self.christmasBonus)
        self.dailySalary = self.salary/self.payrollDaysFactor
        self.sbc = self.dailySalary * self.integrationFactor

    def getSubsidy(self):
        lowerLimitSubsidy = [0.01, 1768.97, 2653.39, 3472.85, 3537.88, 4446.16, 4717.19, 5335.43, 6224.68, 7113.91, 7382.34]
        upperLimitSubsidy = [1768.96, 2653.38, 3472.84, 3537.87, 4446.15, 4717.18, 5335.42, 6224.67, 7113.90, 7382.33, 999999]
        subsidyValue = [407.02, 406.83, 406.62, 392.77, 382.46, 354.23, 324.87, 294.63, 253.54, 217.61, 0]

        for i, lower in enumerate(lowerLimitSubsidy):
            upper = upperLimitSubsidy[i]
            if self.salary >= lower and self.salary <= upper:
                self.lowerSubsidy = lowerLimitSubsidy[i]
                self.upperSubsidy = upperLimitSubsidy[i]
                self.subsidy = subsidyValue[i]
                break
            else:
                pass

    def OF(self):
        self.J = abs(self.isr - self.subsidy) + (self.sbc - 3*self.uma) * self.additionalFactor

    # def CMH(self):
    #     g1 = 0
    #     g2 = 0

    def printValues(self):
        print("Salary: ", self.salary)
        print("ISR: ", self.isr)
        print("ISR - Lower Limit: ", self.lowerIsr)
        print("ISR - Upper Limit: ", self.upperIsr)
        print("")
        print("Subsidy: ", self.subsidy)
        print("Subsidy - Lower Limit: ", self.lowerSubsidy)
        print("Subsidy - Upper Limit: ", self.upperSubsidy)
        print("")
        print("SBC: ", self.sbc)
        print("J: ", self.J)
        print("Constraints: ", self.phi)

import numpy as np

a = np.arange(15)


    





p = PayrollItem(5000, 30.42)
p.printValues()
# print(p.isr())