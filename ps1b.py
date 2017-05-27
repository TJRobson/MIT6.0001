
annual_salary = int(input('Enter your annual salary:' ))
portion_saved = float(input('Enter the percent of your salary to save, as a decimal:'))
total_cost = int(input('Enter the cost of your dream home:'))
semi_annual_raise = float(input('Enter the semiannual raise, as a decimal:'))

def monthCalc(annual, portion, total, raises) :
    
    current_savings = 0
    portion_down_payment = total*0.25
    number_of_months = 0
    
    changing_annual_salary = annual
    salary_increase = raises + 1.0

    while current_savings < portion_down_payment:
        
        monthly_portion = (changing_annual_salary/12)*portion                     
        savings_return = (current_savings*0.04)/12
        this_month = savings_return + monthly_portion
        current_savings += this_month
        
        if number_of_months >= 6 and number_of_months % 6 == 0:
            changing_annual_salary = changing_annual_salary*salary_increase
        
        #print(changing_annual_salary)
        number_of_months += 1
        
    return number_of_months
    

total_months = monthCalc(annual_salary, portion_saved, total_cost, semi_annual_raise)

print('Number of months: ' + str(total_months))
