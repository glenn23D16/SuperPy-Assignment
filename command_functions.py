from utils import get_current_date
import os
import data_operations
import csv
import matplotlib.pyplot as plt
import datetime
from data_operations import read_sold, read_bought, write_sold
from prettytable import PrettyTable
from utils import set_current_date


def buy(args):
    """
    Buy a product and add it to the inventory.

    Parameters
    ----------
    args : argparse.Namespace
        Command-line arguments containing product_name, price, and expiration_date.

    Returns
    -------
    None
    """
    product_name = args.product_name
    price = args.price
    expiration_date = args.expiration_date
    buy_date = get_current_date().strftime('%Y-%m-%d')

    bought_file = 'bought.csv'

    # Check if the bought file exists, create it if it doesn't
    if not os.path.exists(bought_file):
        with open(bought_file, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['ID', 'PRODUCT_NAME', 'BUY_PRICE', 'EXPIRATION_DATE', 'BUY_DATE'])

    # Read the existing bought data
    bought_data = data_operations.read_bought(bought_file)

    # Generate a new ID for the product
    new_id = max([int(row['ID']) for row in bought_data]) + 1 if bought_data else 1

    # Add the new product to the bought data
    new_product = {
        'ID': new_id,
        'PRODUCT_NAME': product_name,
        'BUY_PRICE': price,
        'EXPIRATION_DATE': expiration_date,
        'BUY_DATE': buy_date,
    }
    bought_data.append(new_product)

    # Write the updated bought data to the file
    with open(bought_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['ID', 'PRODUCT_NAME', 'BUY_PRICE', 'EXPIRATION_DATE', 'BUY_DATE'], delimiter=';')
        writer.writeheader()
        writer.writerows(bought_data)

    print('OK')


def sell(args):
    """
    Sell a product from the inventory and store the sale information.

    Parameters
    ----------
    args : argparse.Namespace
        Command-line arguments containing product_name and sell_price.

    Returns
    -------
    None
    """
    product_name = args.product_name
    price = args.price
    sold_date = get_current_date().strftime('%Y-%m-%d')

    # Initialize the sold_data file if it does not exist
    sold_data_file = 'sold.csv'
    if not os.path.exists(sold_data_file):
        with open(sold_data_file, 'w') as f:
            f.write('ID;BOUGHT_ID;PRODUCT_NAME;SELL_PRICE;SELL_DATE\n')

    # Read the data of bought products
    bought_data = data_operations.read_bought(args.bought_file)

    # Initialize sold_data
    sold_data = read_sold()

    for row in bought_data:
        if row['PRODUCT_NAME'] == product_name:
            print("Checking product:", row)
            print("Current date:", get_current_date())
            print("Expiration date:", datetime.datetime.strptime(row['EXPIRATION_DATE'], '%Y-%m-%d').date())

    # Find the bought product with the given name
    found = False
    for bought_row in bought_data:
        if (bought_row['PRODUCT_NAME'] == product_name and datetime.datetime.strptime(bought_row['EXPIRATION_DATE'], '%Y-%m-%d').date() > get_current_date()):

            # Generate a unique SOLD_ID for the new sale
            max_id = max([int(sold_row['ID']) for sold_row in sold_data]) if sold_data else 0
            new_id = max_id + 1

            # If a matching product is found, add a row to the sold data
            # with the relevant information
            sold_row = {
                'ID': new_id,
                'BOUGHT_ID': bought_row['ID'],
                'PRODUCT_NAME': product_name,
                'SELL_PRICE': price,
                'SELL_DATE': sold_date,
            }
            # Add the new row to the existing data
            sold_data.append(sold_row)
            # Write the updated data back to the file
            write_sold(sold_data)
            # Print confirmation message
            print('OK')
            found = True
            break

    if not found:
        # If no matching product is found, print error message
        print("Cannot sell the product. It is either not available or expired.")


def list_products(args):
    """
    Lists all products and their attributes in the given period.

    Parameters
    ----------
    args : argparse.Namespace
        The command line arguments.
    """
    # Set default values for start_date and end_date if they are not provided
    if args.start_date is None:
        args.start_date = datetime.date.min
    if args.end_date is None:
        args.end_date = datetime.date.max

    # Read the bought and sold data using the original read_bought() and read_sold() functions
    bought_data = read_bought("bought.csv")
    sold_data = read_sold()

    # Prepare the output table
    table = PrettyTable()
    table.field_names = [
        "ID",
        "Product",
        "Buy date",
        "Buy price",
        "Expiration date",
        "Days till exp.",
        "Sold",
        "Sold date",
        "Sold price",
    ]

    # Iterate through bought_data and sold_data and add rows to the table
    for row in bought_data:
        # Check if the product is in the given date range
        buy_date = datetime.datetime.strptime(row["BUY_DATE"], "%Y-%m-%d").date()
        if args.start_date <= buy_date <= args.end_date:
            sold = "No"
            sold_date = ""
            sold_price = ""
            for sold_row in sold_data:
                if sold_row["ID"] == row["ID"]:
                    sold = "Yes"
                    sold_date = sold_row["SELL_DATE"]
                    sold_price = sold_row["SELL_PRICE"]
                    break

            days_till_exp = (datetime.datetime.strptime(row["EXPIRATION_DATE"], "%Y-%m-%d") - datetime.datetime.now()).days

            table.add_row([
                row["ID"],
                row["PRODUCT_NAME"],
                row["BUY_DATE"],
                row["BUY_PRICE"],
                row["EXPIRATION_DATE"],
                days_till_exp,
                sold,
                sold_date,
                sold_price,
            ])

    print(table)


def get_revenue(args):
    """
    Retrieves the revenue data for a specified date range.

    Parameters:
    ----------
    args : argparse.Namespace
        The parsed command line arguments containing 'start_date' and 'end_date'.
    """
    print("Getting revenue data...")
    # Set start_date and end_date based on the input arguments or default values
    start_date = args.start_date if args.start_date else "1900-01-01"
    end_date = args.end_date if args.end_date else "9999-12-31"

    # Read the sold data
    sold_data = read_sold()
    print("All sold data:", sold_data)

    # Filter the sold data by the given date range
    filtered_sold_data = [
        row for row in sold_data if start_date <= row["SELL_DATE"] <= end_date
    ]

    print("Filtered sold data:", filtered_sold_data)

    # Calculate daily revenue
    revenue_data = {}
    for row in filtered_sold_data:
        date = row["SELL_DATE"]
        sold_price = float(row["SELL_PRICE"])
        if date in revenue_data:
            revenue_data[date] += sold_price
        else:
            revenue_data[date] = sold_price

    print("Revenue data:", revenue_data)
    return revenue_data


def plot_revenue(args):
    """
    Plots the revenue over time for a given date range.

    Parameters:
    -----------
    args : argparse.Namespace
        The parsed command line arguments containing 'start_date' and 'end_date'.

    Returns:
    --------
    None
    """

    sold_data_file = 'sold.csv'
    if not os.path.exists(sold_data_file):
        with open(sold_data_file, 'w') as f:
            f.write('id,bought_id,product_name,sell_price,sold_date\n')

    # Get the revenue data for the specified time period
    revenue_data = get_revenue(args)

    # Convert the dates to a format that can be plotted
    dates = [datetime.datetime.strptime(date, '%Y-%m-%d').date() for date in
             revenue_data.keys()]

    # Create the plot
    fig, ax = plt.subplots()
    ax.plot(dates, revenue_data.values())

    # Set the labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Revenue')
    ax.set_title('Revenue over time')

    # Show the plot
    plt.show()


def advance_time(args):
    """
    Advances the current date by the given number of days.

    Parameters:
    ----------
    args : argparse.Namespace
        The parsed command line arguments containing 'days'.

    Returns:
    -------
    None
    """
    days = int(args.days)
    current_date = get_current_date()  # Get the current date from file
    new_date = current_date + datetime.timedelta(days=days)  # Calculate the new date by adding the specified number of days to the current date
    set_current_date(new_date)  # Write the new date to the file as the current date
