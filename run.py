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
    data_str = input("Enter your data here: ")
    # to remove commas from the strings
    sales_data = data_str.split(",")
    if validate_data(sales_data):
        print('valid Data')
        break

def validate_data(values):
    # to raise valueError and conver all strings into integers if there aren't 5 values
    try:
        [int(value) for value in values]
        if len(values) != 4:
            raise ValueError(
                f" Please check your input, only 4 value required, you have entered {len(values)}"
            )
    except ValueError as e:
        print(f"Invald input: {e}, please try again.\n")
        #checking for error, if error then return false, otherwise return True
        return False
        
    return True

data = get_sales_data()