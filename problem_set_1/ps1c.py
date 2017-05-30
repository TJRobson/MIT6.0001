
annual_salary = int(input('Enter your annual salary:' ))
total_cost = 1000000*0.25

def getHigh(sal, tot) :
    hi = (tot/36)/(sal/12)
    return hi

def floatRound(ans) :
    ans = int(ans*10000)
    ans = float(ans)/10000
    return ans

def testRate(ans, sal) :
    savings = 0
    increse = 1.07
    changingSal = sal
    for i in range(36):
        month = (changingSal/12)*ans
        savingsReturn = (savings*0.04)/12
        monthPortion = month + savingsReturn
        savings += monthPortion
        if i >= 6 and i % 6 == 0:
            changingSal *= increse
    return savings

def salPercent(total, salary) :
    steps = 0
    low, high = 0.0, getHigh(salary, total_cost)
    ans = (high + low)/2.0
    current_savings = testRate(ans, salary)
    epsilon = 100
    lowEps, hiEps = total - epsilon, total + epsilon

    while lowEps >= current_savings or current_savings >= hiEps:
        if current_savings < total:
            low = ans
            if ans > 1:
                break
        else:
            high = ans
        ans = floatRound((high + low)/2.0)
        current_savings = testRate(ans, salary)
        steps += 1
    return steps, ans
    
def printFunc(total, salary, func) :
    steps, rate = func(total, salary) 
    if rate > 1:
        print('It is not possible to pay the down payment in three years.')
    else:
        print('Best savings rate: %g \nSteps in bisection search: %d' % (rate, steps) )
    
printFunc(total_cost, annual_salary, salPercent)

#noSteps, bestRate = salPercent(total_cost, annual_salary)
#print('Best savings rate: ' + str(bestRate))
#print('Steps in bisection search: ' + str(noSteps))


