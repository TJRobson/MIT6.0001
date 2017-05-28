
annual_salary = int(input('Enter your annual salary:' ))
total_cost = 1000000*0.25

def getHigh(sal, tot) :
    hi = (tot/36)/(sal/12)
    return hi
    
def testRate(ans, sal) :
    savings = 0 
    increse = 1.07
    for i in range(36):
        changingSal = sal 
        month = (changingSal/12)*ans
        savingsReturn = (savings*0.04)/12
        monthPortion = month + savingsReturn 
        savings += monthPortion
        if i % 6 == 0:
            changingSal = changingSal*increse
            #print(changingSal)
    return savings

def salPercent(total, salary) :
    
    steps = 0
    epsilon = 100
    low = 0.0
    high = getHigh(salary, total_cost)
    ans = (high + low)/2.0
    current_savings = testRate(ans, salary)        
        
    while (current_savings - total) <= epsilon:
        high = high
        ans = ans
        if current_savings < total:
            low = ans 
        else:
            high = ans
        ans = (high + low)/2.0
        current_savings = testRate(ans, salary)
        #print(current_savings)
        #print(ans)
        steps += 1
    return steps, ans
        
noSteps, bestRate = salPercent(total_cost, annual_salary)    

print(bestRate, noSteps)    



