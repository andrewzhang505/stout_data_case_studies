import csv
from prettytable import PrettyTable


DATA_FILE = "./casestudy.csv"


def format_cents(cents):
    if cents == 0:
        return "-"
    s = ""
    if cents < 0:
        cents = -cents
        s = "-"
    dollars = cents // 100
    cents = cents % 100
    return s + "$" + f'{dollars:,}' + "." + f'{cents:02d}'

def format_int(num):
    if num == 0:
        return "-"
    return f'{num:,}'


class Case2Data:
    def __init__(self):
        self.years = {}
        self.customers = {}

        with open(DATA_FILE) as f:
            reader = csv.reader(f)
            _ = next(reader)
            for _, email, net_rev, year in reader:
                year = int(year)
                net_rev = int(round(float(net_rev)*100))
                # net_rev = float(net_rev)

                if year not in self.years:
                    self.years[year] = YearData(year)
                if email not in self.customers:
                    self.customers[email] = CustomerData(email)
                
                self.customers[email].add_data(year, net_rev)
                self.years[year].add_data(self.customers[email])
        
        for y in sorted(self.years.keys()):
            year = self.years[y]
            year.calc_stats()
            prev_year = self.years.get(y-1)
            if prev_year is not None:
                year.attrition = prev_year.tot_rev - year.tot_rev
                year.tot_cust_prev = prev_year.tot_cust
                year.lost_cust = prev_year.next_cust_loss        
            
    
    def print_table(self):
        table = PrettyTable()
        table.add_column("Year", ["Total Revenue", "New Customer Revenue", "Existing Customer Growth", 
                "Revenue Attrition", "Existing Customer Revenue", "Prior Existing Customer Revenue", 
                "Total Customers", "Prior Year Total Customers", "New Customers", "Lost Customers"])

        for y in sorted(self.years.keys()):
            table.add_column(str(y), self.years[y].get_stats())

        
        print(table)





class YearData:
    def __init__(self, year):
        self.year = year
        self.customers = []
    
    def add_data(self, customer):
        self.customers.append(customer)
    
    def calc_stats(self):
        self.tot_rev = 0
        self.new_cust_rev = 0
        self.ex_cust_growth = 0
        self.ex_cust_rev_curr = 0
        self.ex_cust_rev_prev = 0
        self.tot_cust = len(self.customers)
        self.new_cust = 0
        self.next_cust_loss = 0

        self.attrition = 0
        self.tot_cust_prev = 0
        self.lost_cust = 0

        for c in self.customers:
            curr_rev = c.get_rev(self.year)
            prev_rev = c.get_rev(self.year - 1)
            
            self.tot_rev += curr_rev
            
            if prev_rev is None:
                self.new_cust_rev += curr_rev
                self.new_cust += 1
            else:
                self.ex_cust_growth += (curr_rev - prev_rev)
                self.ex_cust_rev_curr += curr_rev
                self.ex_cust_rev_prev += prev_rev
            
            if c.get_rev(self.year + 1) is None:
                self.next_cust_loss += 1
    
    def get_stats(self):
        return [format_cents(self.tot_rev), format_cents(self.new_cust_rev), format_cents(self.ex_cust_growth),
            format_cents(self.attrition), format_cents(self.ex_cust_rev_curr), format_cents(self.ex_cust_rev_prev), 
            format_int(self.tot_cust), format_int(self.tot_cust_prev), format_int(self.new_cust), format_int(self.lost_cust)]

                

    

class CustomerData:
    def __init__(self, customer):
        self.customer = customer
        self.years = {}
    
    def add_data(self, year, rev):
        self.years[year] = rev
    
    def get_rev(self, year):
        return self.years.get(year)
    
