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

def get_sales_data():
    """
    Get sales datas input for the poultry
    """

while True:
    print("Please enter sales data for the day.")
    print("Data should be four numbers, separated by commas.")
    print("Example: 05,35,45,25\n")
    #convert the strings of data from the user into a list of value
    data_str = input("Enter your data here: ")
    # to remove commas from the strings
    sales_data = data_str.split(",")
    if validate_data(sales_data):
        print('valid Data')
        break


def validate_data(values):
    # to raise valueError and conver all strings
    #  into integers if there aren't 5 values
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

def update_sales_worksheet(data):
    """
    update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated.\n")


def calculate_extras_data(sales_row):
    """
    compare sales with stock and calculate the Extras for each item type.
    """
    print("Calculating Extras data...\n")
    # to get all balance stock values
    balance = SHEET.worksheet("balance").get_all_values()
    pprint(balance)


def man():
    # Run all program functions
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_extras_data(sales_data)


print("Welcome to Poultry House Date Automation")
main()