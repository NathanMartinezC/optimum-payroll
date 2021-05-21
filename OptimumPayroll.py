class PayrollItem:
    lowerIsr = 0
    upperIsr = 0
    lowerSubsidy = 0
    upperSubsidy = 0
    fixedTax = 0
    additionalFactor = 0
    isr = 0
    J = 0
    sbc = 0
    christmasBonus = 15
    vacations = 6
    quotedDays = 365
    vacationFactor = 0.25
    integrationFactor = 0
    dailySalary = 0
    subsidy = 0
    upperSubsidy = 7382.34
    uma = 86.88
    minimumSalary = 123.22*30
    companyFactor = 0
    salaryCompany = 0
    phi = 0

    imss = 0
    totalTaxes = 0
    payrollPay = 0

    def __init__(self, salary, companyFactor, payrollDaysFactor):
        self.salary = salary
        self.payrollDaysFactor = payrollDaysFactor
        self.companyFactor = companyFactor
        self.salaryCompany = salary*companyFactor
        
        #Initialization
        self.getIsrFactors()
        self.getIsr()
        self.getSbc()
        self.getSubsidy()
        self.imss = ImssTax(self.sbc,self.uma,self.payrollDaysFactor,self.salaryCompany)
        self.totalTaxes = self.imss.totalTax + self.isr - self.subsidy
        self.payrollPay = self.salary + self.imss.totalEmployerTax + self.isr - self.subsidy
        self.CHM()
        self.OF()


    
    def getIsrFactors(self):
        lowerLimitsIsr = [0.01, 578.53, 4910.19, 8629.21, 10031.08, 12009.95, 24222.32, 38177.70, 72887.51, 97183.34, 291550.01]
        upperLimitsIsr = [578.52, 4910.18, 8629.20, 10031.07, 12009.94, 24222.31, 38177.69, 72887.50, 97183.33, 291550.00, 999999.00]
        fixedTaxesIsr = [0.00, 11.11, 288.33, 692.96, 917.26, 1271.87, 3880.44, 7162.74, 17575.69, 25350.35, 91435.02]
        factorsIsr = [1.92, 6.40, 10.88, 16.00, 17.92, 21.36, 23.52, 30.00, 32.00, 34.00, 35.00]

        for i, lower in enumerate(lowerLimitsIsr):
            upper = upperLimitsIsr[i]
            if self.salaryCompany >= lower and self.salaryCompany <= upper:
                self.lowerIsr = lowerLimitsIsr[i]
                self.upperIsr = upperLimitsIsr[i]
                self.fixedTax = fixedTaxesIsr[i]
                self.additionalFactor = factorsIsr[i]/100
                break
            else:
                pass
        

    def getIsr(self):
        self.isr = (self.salaryCompany - self.lowerIsr) * self.additionalFactor + self.fixedTax

    def getSbc(self):
        self.integrationFactor = (1/self.quotedDays) * (self.vacations * self.vacationFactor + self.quotedDays + self.christmasBonus)
        self.dailySalary = self.salaryCompany/self.payrollDaysFactor
        self.sbc = self.dailySalary * self.integrationFactor

    def getSubsidy(self):
        lowerLimitSubsidy = [0.01, 1768.97, 2653.39, 3472.85, 3537.88, 4446.16, 4717.19, 5335.43, 6224.68, 7113.91, 7382.34]
        upperLimitSubsidy = [1768.96, 2653.38, 3472.84, 3537.87, 4446.15, 4717.18, 5335.42, 6224.67, 7113.90, 7382.33, 999999]
        subsidyValue = [407.02, 406.83, 406.62, 392.77, 382.46, 354.23, 324.87, 294.63, 253.54, 217.61, 0]

        for i, lower in enumerate(lowerLimitSubsidy):
            upper = upperLimitSubsidy[i]
            if self.salaryCompany >= lower and self.salaryCompany <= upper:
                self.lowerSubsidy = lowerLimitSubsidy[i]
                self.upperSubsidy = upperLimitSubsidy[i]
                self.subsidy = subsidyValue[i]
                break
            else:
                pass

    def CHM(self):
        g1 = self.salaryCompany - self.upperSubsidy
        g2 = self.minimumSalary - self.salaryCompany

        if(g1 <= 0):
            pass
        else:
            self.phi += 1
        if(g2 <= 0):
            pass
        else:
            self.phi += 1


    def OF(self):
        self.J = abs(self.isr - self.subsidy) #self.payrollPay  #abs(self.isr - self.subsidy) + self.imss.totalEmployerTax + self.imss.totalEmployeeTax + self.salary


    def printValues(self):
        print(" ")
        print("Salary: ", self.salary)
        print("Salary company: ", self.salaryCompany)
        print("ISR: ", self.isr)
        print("Subsidy: ", self.subsidy)
        print("SBC: ", self.sbc)
        print("IMSS - Employee: ", self.imss.totalEmployeeTax)
        print("IMSS - Employer: ", self.imss.totalEmployerTax)
        print("Total IMSS Tax: ", self.imss.totalTax)
        print('Total Payroll: ', self.payrollPay)
        print("J: ", self.J)
        print('phi: ', self.phi)
        print("Company Factor: ", self.companyFactor)
        print(" ")

class ImssTax:
    sbc = 0
    uma = 0
    payrollDays = 0
    salary = 0
    totalEmployeeTax = 0
    totalEmployerTax = 0
    totalTax = 0

    #Employee Tax
    sicknessEmployeeTax = 0
    fixedEmployeeTax = 0
    medicalEmployeeTax = 0
    moneyEmployeeTax = 0
    additionalEmployeeTax = 0
    disabilityEmployeeTax = 0
    retirementEmployeeTax = 0
    ceavEmployeeTax = 0

    #Employee Tax Factors
    #sicknessEmployeeFactor = 0
    fixedEmployeeFactor = 0
    medicalEmployeeFactor = 0.00375
    moneyEmployeeFactor = 0.0025
    additionalEmployeeFactor = 0.004
    disabilityEmployeeFactor = 0.00625
    retirementEmployeeFactor = 0
    ceavEmployeeFactor = 0.01125

    #Employer Tax
    sicknessEmployerTax = 0
    fixedEmployerTax = 0
    medicalEmployerTax = 0
    moneyEmployerTax = 0
    additionalEmployerTax = 0
    disabilityEmployerTax = 0
    retirementEmployerTax = 0
    ceavEmployerTax = 0
    riskEmployerTax = 0
    infonavitTax = 0
    kinderEmployerTax = 0

    #Employer Tax Factors
    #sicknessEmployerFactor = 0
    fixedEmployerFactor = 0.2040
    medicalEmployerFactor = 0.0105
    moneyEmployerFactor = 0.007
    additionalEmployerFactor = 0.0110
    disabilityEmployerFactor = 0.0175
    retirementEmployerFactor = 0.02
    ceavEmployerFactor = 0.03150
    riskEmployerFactor = 0.005
    infonavitFactor = 0.05
    kinderEmployerFactor = 0.01

    def __init__(self,sbc,uma,payrollDays,salary):
        self.sbc = sbc
        self.uma = uma
        self.payrollDays = payrollDays
        self.salary = salary

        self.totalEmployee()
        self.totalEmployer()
        self.totalTax = self.totalEmployeeTax + self.totalEmployerTax

    def totalEmployee(self):
        self.sicknessEmployee()
        self.disabilityEmployee()
        self.retirementEmployee()
        self.ceavEmployee()

        self.totalEmployeeTax = self.sicknessEmployeeTax + self.disabilityEmployeeTax + self.retirementEmployeeTax + self.ceavEmployeeTax

    def totalEmployer(self):
        self.sicknessEmployer()
        self.riskEmployer()
        self.disabilityEmployer()
        self.retirementEmployer()
        self.ceavEmployer()
        self.kinderEmployer()
        self.infonavitEmployer()

        self.totalEmployerTax = self.sicknessEmployerTax + self.riskEmployerTax + self.disabilityEmployerTax + self.retirementEmployerTax + self.ceavEmployerTax + self.kinderEmployerTax + self.infonavitTax

    ###### Methods of Employee Taxes  
    def sicknessEmployee(self):
        self.fixedEmployeeTax = self.uma * self.payrollDays * self.fixedEmployeeFactor
        self.medicalEmployeeTax = self.uma * self.payrollDays * self.medicalEmployeeFactor
        self.moneyEmployeeTax = self.uma * self.payrollDays * self.moneyEmployeeFactor

        if (self.salary >= 3*self.uma*self.payrollDays):
            self.additionalEmployeeTax = ((self.sbc - 3*self.uma)*self.additionalEmployeeFactor) * self.payrollDays
        else:
            self.additionalEmployeeTax = 0

        self.sicknessEmployeeTax = self.fixedEmployeeTax + self.additionalEmployeeTax + self.medicalEmployeeTax + self.moneyEmployeeTax

    def disabilityEmployee(self):
        self.disabilityEmployeeTax = self.sbc * self.payrollDays * self.disabilityEmployeeFactor

    def retirementEmployee(self):
        self.retirementEmployeeTax = self.sbc * self.payrollDays * self.retirementEmployeeFactor
    
    def ceavEmployee(self):
        self.ceavEmployeeTax = self.sbc * self.payrollDays * self.ceavEmployeeFactor
    
    ###### Methods of Employer Taxes
    def sicknessEmployer(self):
        self.fixedEmployerTax = self.uma * self.payrollDays * self.fixedEmployerFactor
        self.medicalEmployerTax = self.uma * self.payrollDays * self.medicalEmployerFactor
        self.moneyEmployerTax = self.uma * self.payrollDays * self.moneyEmployerFactor

        if (self.salary >= 3*self.uma*self.payrollDays):
            self.additionalEmployerTax = ((self.sbc - 3*self.uma)*self.additionalEmployerFactor) * self.payrollDays
        else:
            self.additionalEmployerTax = 0

        self.sicknessEmployerTax = self.fixedEmployerTax + self.additionalEmployerTax + self.medicalEmployerTax + self.moneyEmployerTax

    def riskEmployer(self):
        self.riskEmployerTax = self.sbc * self.payrollDays * self.riskEmployerFactor

    def disabilityEmployer(self):
        self.disabilityEmployerTax = self.sbc * self.payrollDays * self.disabilityEmployerFactor

    def retirementEmployer(self):
        self.retirementEmployerTax = self.sbc * self.payrollDays * self.retirementEmployerFactor
    
    def ceavEmployer(self):
        self.ceavEmployerTax = self.sbc * self.payrollDays * self.ceavEmployerFactor

    def kinderEmployer(self):
        self.kinderEmployerTax = self.sbc * self.payrollDays * self.kinderEmployerFactor

    def infonavitEmployer(self):
        self.infonavitTax = self.sbc * self.payrollDays * self.infonavitFactor

    
import numpy as np

NP = 10
GMAX = 60
p_min = 0.6
p_max = 1.0
salary = 8000
payrollDaysFactor = 30.42


P = []
V = []
p = []
v = []

#Inicializacion de la poblacion
for i in range(NP):
    companyFactor = p_min + np.random.rand() * (p_max - p_min)
    p.append(PayrollItem(salary, companyFactor, payrollDaysFactor))
    v.append(PayrollItem(0, 0, payrollDaysFactor))

for i in range(GMAX):
    F = np.random.rand()
    CR = np.random.rand()
    
    while (((F < 0.3) or (F > 0.9)) and ((CR < 0.8) or (CR >= 1))):
        F = np.random.rand()
        CR = np.random.rand()

    for k in range(NP):
        flag = True

        while flag == True:
            r1 = np.random.randint(0,NP)
            r2 = np.random.randint(0,NP)
            r3 = np.random.randint(0,NP)
            if (r1 != k and r2 != k and r3 != k) and ( r1 != r2 and r2 != r3 and r1 !=r3):
                flag = False
        
        flag = True
        
        if np.random.rand() < CR:
            u = PayrollItem(salary, p[r1].companyFactor + F*(p[r2].companyFactor - p[r3].companyFactor),payrollDaysFactor)
            if u.companyFactor < p_min or u.companyFactor > p_max:
                u.companyFactor = p_min + np.random.rand() * (p_max - p_min)
            v[k] = PayrollItem(salary,u.companyFactor,payrollDaysFactor)
        else:
            v[k] = PayrollItem(salary,p[k].companyFactor,payrollDaysFactor)

    for k in range(NP):

        if (p[k].phi == 0) and (v[k].phi == 0):
            if (p[k].J < v[k].J):
                p[k] = PayrollItem(salary,p[k].companyFactor,payrollDaysFactor)
            elif(p[k].J > v[k].J):
                p[k] = PayrollItem(salary,v[k].companyFactor,payrollDaysFactor)
        
        elif(p[k].phi != 0) and (v[k].phi == 0):
            p[k] = PayrollItem(salary,v[k].companyFactor,payrollDaysFactor)
        elif(p[k].phi == 0) and (v[k].phi != 0):
            p[k] = PayrollItem(salary,p[k].companyFactor,payrollDaysFactor)
        else:
            if(np.random.rand() < 0.5):
                p[k] = PayrollItem(salary,v[k].companyFactor,payrollDaysFactor)
            else:
                p[k] = PayrollItem(salary,p[k].companyFactor,payrollDaysFactor)

for i in p:
    i.printValues()

Z = PayrollItem(8000, 0.6, payrollDaysFactor)
Z.printValues()

#for p in population:
#    p.printValues()