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
    print("Please enter sales data for the day.")
    print("Data should be four numbers, separated by commas.")
    print("Example: 05,35,45,25\n")

    data_str = input("Enter your data here: ")
    # to remove commas from the strings
    sales_data = data_str.split(",")
    print(sales_data)

def validate_data(values):
    # to raise valueError and conver all strings into integers if there aren't 5 values
    try:
        if lent(values) != 4:
            raise ValueError(
                f" Please check your input, only 4 value required, you have ended {len(values)}"
            )
    except ValueError as e:
        print(f"Invald input: {e}, please try again.\n")

get_sales_data()