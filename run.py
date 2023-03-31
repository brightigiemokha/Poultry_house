import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Poultry_house')

def validate_data(values):
    """
     to raise valueError and conver all strings
      into integers if there aren't 5 values
      """

    try:
        [int(value) for value in values]
        if len(values) != 4:
            raise ValueError(
                f" Please check your input, only 4 value required, you have entered {len(values)}"
            )
    except ValueError as e:
        print(f"Invald data: {e}, please try again.\n")
        #checking for error, if error then return false, otherwise return True
        return False
        
    return True


def update_worksheet(data, worksheet):
    """ 
    receiving a list of int to be insterted into a worksheet
    to update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_updates = SHEET.worksheet(worksheet)
    worksheet_updates.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")


def input_sales_data():
    """
    Get sales datas input for the poultry
    """

    
    while True:
        print("Please enter sales data for the day.")
        print("Data should be four numbers, separated by commas.")
        print("Example: 05,35,45,25\n")
        #convert the strings of data from the user into a list of value
        data_str = input("Enter your data here: ")

        """
        to remove commas from the strings
        """
        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print(sales_data)
            break

    return sales



def calculate_extras_data(sales_row):
    """
    compare sales with stock and calculate the Extras for each item type.
    """
    print("Calculating Extras data...\n")
    # to get all balance stock values
    balance = SHEET.worksheet("balance").get_all_values()
    balance_row = stock[-1]
    
    extras_data = []
    for stock, sales in zip(balance_row, sales_row):
        extras = int(balance) - sales
        extras_data.append(extras)
    
    return surplus_data


def get_last_5_entries_sales():
    """ 
    collects data in collums from sales worksheet, 5 entries
    """
    sales = SHEET.worksheet("sales")
    
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns

def calculate_stock_data(data):
    """
    calculate the average stock for each item type, adding 10%
    """
    print("Calculate stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(stock_num)
    
    return new_stock_data


def main():
    # Run all program functions
    data = input_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_balance_data = calculate_extras_data(sales_data)
    update_worksheet(new_extra_data, "extras")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")


print("Welcome to Poultry House Date Automation")
main()

