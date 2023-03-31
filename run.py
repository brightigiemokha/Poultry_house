import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Poultry_house')



def get_sales_data():
    """
    Get sales datas input for the poultry
    """

    
    while True:
        print("Please enter sales data for the day.")
        print("Data should be four numbers, separated by commas.")
        print("Example: 05,35,45,25\n")
        #convert the strings of data from the user into a list of value
        data_str = input("Enter your data here:\n")

        """
        to remove commas from the strings
        """
        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print("Valid Data!!!")
            break

    return sales_data

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


def calculate_extras_data(sales_row):
    """
    compare sales with stock and calculate the Extras for each item type.
    """
    print("Calculating Extras data...\n")
    # to get all balance stock values
    balance = SHEET.worksheet("balance").get_all_values()
    balance_row = balance[-1]
    
    extras_data = []
    for balance, sales in zip(balance_row, sales_row):
        extras = int(balance) - sales
        extras_data.append(extras)
    
    return extras_data


def get_last_5_entries_sales():
    """ 
    collects data in collums from sales worksheet, 5 entries
    """
    sales = SHEET.worksheet("sales")
    
    columns = []
    for ind in range(1, 5):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns

def calculate_balance_data(data):
    """
    calculate the average stock for each item type, adding 10%
    """
    print("Calculate balance data...\n")
    new_balance_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        balance_num = average * 1.1
        new_balance_data.append(balance_num)
    
    return new_balance_data


def main():
    """
     Run all program functions
     """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_extras_data = calculate_extras_data(sales_data)
    update_worksheet(new_extras_data, "extras")
    sales_columns = get_last_5_entries_sales()
    balance_data = calculate_balance_data(sales_columns)
    update_worksheet(balance_data, "balance")


print("Welcome to Poultry House Date Automation")
main()

