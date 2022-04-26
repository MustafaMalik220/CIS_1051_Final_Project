from matplotlib import pyplot as plt

# reads sallie mae files and returns a list of tuples containing loan amounts and interest rates
def sallie_mae_reader(): 
    file = open("loan_report.txt", "r").read().split("\n")
    loans = []
    for index,string in enumerate(file):
        if "Loan #" in string:
            loan = float(string[43:].replace(",",""))
            interest = float(file[index+4].replace("Fixed Interest Rate ","").replace("%",""))
            loans.append((loan,interest))
    return loans
            
loans = sallie_mae_reader()
loans.sort(reverse=True,key=lambda i: i[1]) # sorts loans from highest to lowest interest rate
payment = int(input("Payment amount: "))
payment_freq = int(input("How often do you want to make payments(Days)?: "))
print()
payment_total = 0
payment_start = 0
remaining_money = 0

# returns x and y coordinates for the graph
def loan_graph(loan, interest, payment, payment_freq, payment_start, remaining_money, payment_total):
    loan_x = [0]    # list of days to be used as x coordinates
    loan_y = [loan] # list of loan amounts after payment and interest to be used as y coordinates
    day = 0
    while loan > 0:
        day += 1
        loan_x.append(day)
        # checks if remaining money from the payments on previous loans has to be used
        if day == payment_start: 
            if remaining_money > 0:
                loan -= remaining_money
                payment_total += remaining_money
                print("Day: ",day,"\n","Payment made: ",remaining_money,sep="")
                print("Remaining loan amount:", loan,"\n")
                remaining_money = 0
        # makes payments on loans and adds to payment total
        if day%payment_freq==0 and day>payment_start:
            if loan >= payment:
                loan -= payment
                payment_total += payment
                print("Day: ",day,"\n","Payment made: ",payment,sep="")
                print("Remaining loan amount:", loan,"\n")
            elif loan < payment:
                remaining_money = payment-loan
                payment_total += loan
                print("Day: ",day,"\n","Payment made: ",loan,sep="")
                print("Remaining loan amount:", loan,"\n")
                loan = 0
        loan_interest = loan*((interest/100)/365)
        loan += loan_interest
        loan_y.append(loan)
    return loan_x, loan_y, remaining_money, day, payment_total

# makes plots using lists of days and loan amounts from the loan_graph function
plt.style.use("seaborn")
for loan,interest in loans:
    loan_x,loan_y,remaining_money,payment_start, payment_total = loan_graph(loan,interest,payment,payment_freq,payment_start,remaining_money, payment_total)
    plt.plot(loan_x, loan_y)
    plt.title("Loans")
    plt.xlabel("Time (days)")
    plt.ylabel("Loan Amount ($)")
    plt.show(block=False)
print("Payment total:",payment_total)
    
