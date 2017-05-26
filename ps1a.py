
annual_salary = int(input('Enter your annual salary:' ))
portion_saved = float(input('Enter the percent of your salary to save, as a decimal:'))
total_cost = int(input('Enter the cost of your dream home:'))

def monthCalc(annual, portion, total) :
    current_savings = 0
    monthly_portion = (annual/12)*portion
    portion_down_payment = total*0.25
    number_of_months = 0
    
    while current_savings < portion_down_payment:
        savings_return = (current_savings*0.04)/12
        this_month = savings_return + monthly_portion
        current_savings += int(this_month)
        number_of_months += 1
        
    return number_of_months
    

total_months = monthCalc(annual_salary, portion_saved, total_cost)

print('Number of months: ' + str(total_months))