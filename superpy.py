# Imports
import argparse
import csv
import datetime
import os
import matplotlib.pyplot as plt
from prettytable import PrettyTable

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def revenue(args):
    """
    Determines how to calculate and display revenue data based on the provided arguments.

    Parameters:
    ----------
    args : argparse.Namespace
        The parsed command line arguments.

    Returns:
    -------
    None
    """
    # Initialize an empty revenue dictionary
    revenue_data = {}
    # If the user specified the plot flag, plot the revenue data over time
    if args.plot:
        plot_revenue(args.start_date, args.end_date)
    # Otherwise, calculate and print the revenue data
    else:
        # Get the revenue data for the specified date range
        revenue_data = get_revenue(args)
        # If the user specified the calculate total flag, calculate the total revenue and print a summary table
        if args.calculate_total:
            total_revenue, table = calculate_revenue({'sold_data': revenue_data})
            print(table)
        # Otherwise, print a table of the revenue data
        else:
            table = create_pretty_table(revenue_data)
            print(table)

    # Return the revenue data
    return revenue_data


def read_bought(file_name):
    """
    Reads the given file and returns its contents
    as a list of dictionaries.

    Parameters:
    ----------
    file_name : str
        The name of the file to read.

    Returns:
    -------
    List[Dict]
        A list of dictionaries with the data from the file.
    """
    with open(file_name, 'r', newline='') as file:
        reader = csv.DictReader(file, delimiter=';')
        return [row for row in reader]


def write_bought(bought_data, bought_file):
    """
    Writes the given list of dictionaries to a CSV file with the given filename.

    Parameters:
    ----------
    bought_data : list of dict
        A list of dictionaries representing the data to be written to the file.
    bought_file : str
        The name of the file to which the data should be written.

    Returns:
    -------
    None
    """
    with open(bought_file, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["SOLD_ID", "PRODUCT_NAME", "BUY_PRICE", "EXPIRATION_DATE", "BUY_DATE"])
        for row in bought_data:
            writer.writerow(row.values())


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
    bought_data = read_bought(bought_file)

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


def delete_bought(args):
    """
    Delete a bought product from the inventory based on its id.

    Parameters
    ----------
    args : argparse.Namespace
        Command-line arguments containing the id of the bought product to be deleted.

    Returns
    -------
    None
    """
    # Read current data from bought_data file
    bought_data = read_bought(args.bought_file)

    # Find the bought product with the matching id
    for index, bought_row in enumerate(bought_data):
        if int(bought_row['ID']) == args.id:
            # If a matching product is found, delete the corresponding row
            del bought_data[index]
            # Write the updated data back to the file
            write_bought(bought_data, args.bought_file)
            # Print confirmation message
            print(f"Deleted product with id {args.id}")
            break
    else:
        # If no matching product is found, print an error message
        print(f"No product with id {args.id} found in stock.")


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
            f.write('SOLD_ID;BOUGHT_ID;PRODUCT_NAME;SELL_PRICE;SELL_DATE\n')

    # Read the data of bought products
    bought_data = read_bought(args.bought_file)

    # Print debug information
    print("Bought products:")
    for row in bought_data:
        print(row)

    # Find the bought product with the given name
    found = False
    for bought_row in bought_data:
        if bought_row['PRODUCT_NAME'] == product_name and datetime.datetime.strptime(bought_row['EXPIRATION_DATE'], '%Y-%m-%d') > datetime.datetime.utcnow():
            # Read current data from sold_data file
            sold_data = read_sold()

            # Generate a unique SOLD_ID for the new sale
            max_sold_id = max([int(sold_row['SOLD_ID']) for sold_row in sold_data]) if sold_data else 0
            new_sold_id = max_sold_id + 1

            # If a matching product is found, add a row to the sold data
            # with the relevant information
            sold_row = {
                'SOLD_ID': new_sold_id,
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
        # If no matching product is found, add a row to the sold data
        # with the relevant information
        sold_data = read_sold()
        max_sold_id = max([int(sold_row['SOLD_ID']) for sold_row in sold_data]) if sold_data else 0
        new_sold_id = max_sold_id + 1
        sold_row = {
            'SOLD_ID': new_sold_id,
            'BOUGHT_ID': 'N/A',  # Indicate that this product was not bought from the inventory
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


def delete_sold(args):
    """
    Delete a sold product from the inventory based on its id.

    Parameters
    ----------
    args : argparse.Namespace
        Command-line arguments containing the id of the sold product to be deleted.

    Returns
    -------
    None
    """
    # Read current data from sold_data file
    sold_data = read_sold()

    # Find the sold product with the matching id
    for index, sold_row in enumerate(sold_data):
        if sold_row['id'] == args.id:
            # If a matching product is found, delete the corresponding row
            del sold_data[index]
            # Write the updated data back to the file
            write_sold(sold_data)
            # Print confirmation message
            print(f"Deleted product with id {args.id}")
            break
    else:
        # If no matching product is found, print an error message
        print(f"No product with id {args.id} found in sold products.")


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
                if sold_row["SOLD_ID"] == row["ID"]:
                    sold = "Yes"
                    sold_date = sold_row["SELL_DATE"]
                    sold_price = sold_row["SELL_PRICE"]
                    break

            days_till_exp = (datetime.datetime.strptime(row["EXPIRATION_DATE"], "%Y-%m-%d") - datetime.datetime.now()).days

            table.add_row([
                row["SOLD_ID"],
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


def create_pretty_table(data):
    """
    Creates a PrettyTable object from the given data.

    Parameters:
    ----------
    data : list of dict
        The data for the table, where each dictionary
        represents a row in the table.

    Returns:
    -------
    PrettyTable
        A PrettyTable object with the given data.
    """
    # create a PrettyTable object from the data
    table = PrettyTable()
    for row in data:
        table.add_row([row[column_name] for column_name in row])

    # return the PrettyTable object
    return table


def read_sold():
    """
    Reads the data of sold products from the 'sold.csv' file.

    Returns
    -------
    sold_data : list of dict
        The data of sold products as a list of dictionaries,
        where each dictionary represents a row in the file.
    """
    # If the 'sold.csv' file does not exist, return an empty list
    if not os.path.exists('sold.csv'):
        return []

    # Read the data from the 'sold.csv' file
    with open('sold.csv', 'r') as sold_file:
        # Create a CSV reader object
        sold_reader = csv.DictReader(sold_file, delimiter=',')

        # Initialize an empty list to store the data
        sold_data = []

        # Loop over each row in the 'sold.csv' file
        for sold_row in sold_reader:
            # Append the row to the list of data
            sold_data.append(sold_row)

    return sold_data


def write_sold(sold_data):
    """
    Writes the given data to the 'sold.csv' file.

    Parameters:
    -----------
    sold_data : list of dict
        The data to write to the 'sold.csv' file as a list
        of dictionaries, where each dictionary represents
        a row in the file.

    Returns:
    -------
    None
    """
    # Open the 'sold.csv' file with write permission and clear it
    with open('sold.csv', 'w', newline='') as sold_file:
        # Create a DictWriter object that writes to the 'sold.csv' file,
        # using the field names from the first row of the data as the headers
        sold_writer = csv.DictWriter(sold_file, fieldnames=sold_data[0].keys())
        # Write the headers to the 'sold.csv' file
        sold_writer.writeheader()
        # Write the data roles to the 'sold.csv' file
        sold_writer.writerows(sold_data)


def initialize_data_files(args):
    """
    Initializes the data files if they do not already exist.

    Parameters:
    ----------
    args : argparse.Namespace
        The parsed command line arguments.

    Returns:
    -------
    None
    """
    # Create the bought and sold data files if they do not exist
    if not os.path.exists(args.bought_file):
        with open(args.bought_file, 'w') as f:
            f.write('id,product_name,buy_price,expiration_date,buy_date\n')
    if not os.path.exists(args.sold_file):
        with open(args.sold_file, 'w') as f:
            f.write('bought_id,product_name,sell_price,sold_date\n')


def filter_data_by_date(data, start_date, end_date):
    """
    Filter the data between two dates (inclusive).

    Parameters:
    -----------
    data: list
        A list of dictionaries containing sales data.

    start_date: str
        The start date in 'YYYY-MM-DD' format.

    end_date: str
        The end date in 'YYYY-MM-DD' format.

    Returns:
    --------
    list
        A list of dictionaries containing sales data filtered by the date range.
    """
    filtered_data = []
    # Loop through each row of data and compare its date to the date range
    for row in data:
        sell_date = dt.strptime(row['SELL_DATE'], '%Y-%m-%d').date()
        if start_date <= str(sell_date) <= end_date:
            filtered_data.append(row.copy())
    return filtered_data


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


def calculate_revenue(args):
    """
    Calculates the total revenue from the given data.

    Parameters:
    ----------
    args : argparse.Namespace
        The parsed command line arguments containing 'sold_data'.

    Returns:
    -------
    revenue : float
        The total revenue as a float.

    table : prettytable.PrettyTable
        The PrettyTable object containing the revenue data.

    Raises:
    ------
    ValueError:
        If the sold_data is empty or does not contain any
        'sell_price' values.
    """
    sold_data = args.sold_data

    # Check if the sold_data is empty or None
    if not sold_data:
        raise ValueError("No sold_data provided.")

    # Initialize revenue to 0.0
    revenue = 0.0

    # Calculate the total revenue from the sold_data
    for row in sold_data:
        # Check if each row contains a 'sell_price' value
        if 'sell_price' not in row:
            raise ValueError("Missing sell_price value in sold_data.")
        revenue += float(row['sell_price'])

    # Create a PrettyTable object with the headers and data
    table = create_pretty_table([{"Total Revenue": f"${revenue:.2f}"}])
    table.field_names = ["Total Revenue"]

    # Return the revenue and table
    return revenue, table


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


def calculate_profit(bought_data, sold_data):
    """
    Calculates the profit based on bought and sold data.

    Parameters:
    ----------
    bought_data : list of dict
        The data of the bought products as a list of
        dictionaries, where each dictionary represents
        a row in the bought data file.
    sold_data : list of dict
        The data of the sold products as a list of dictionaries,
        where each dictionary represents a row in the sold data file.

    Returns:
    -------
    float, PrettyTable
        The calculated profit based on the bought and sold data, and a
        PrettyTable object displaying the profit.
    """
    profit = 0  # Initialize profit to zero
    for sold_row in sold_data:  # Loop through each row in the sold data
        bought_id = int(sold_row['ID'])  # Get the ID of the bought
        # Find the corresponding bought row
        bought_row = next((b for b in bought_data if int(b['ID']) == bought_id), None)
        if bought_row is not None:  # If the bought row is found
            profit += float(sold_row['SELL_PRICE']) - float(bought_row['BUY_PRICE'])  # Update the profit by subtracting the buy_price from the sell_price

    # Create a pretty table with the profit data
    table = PrettyTable()
    table.field_names = ["Profit"]
    table.add_row([f"${profit:.2f}"])

    return profit, table


def get_current_date():
    """
    Gets the current date as a datetime.date object.

    Returns:
    -------
    datetime.date
        The current date.
    """
    # Open the 'current_date.txt' file in read mode
    with open('current_date.txt', 'r') as file:
        # Read the date string from the file
        date_str = file.read()
        # Convert the date string to a date object using strptime
        # and return it
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()


def set_current_date(new_date):
    """
    Sets the current date to the given date by writing it to a file.

    Parameters:
    ----------
    new_date : datetime.date
        The new date to set as the current date.

    Returns:
    -------
    None
    """
    # Open the 'current_date.txt' file in write mode
    # and write the new date to the file as a string
    # in the format YYYY-MM-DD
    with open('current_date.txt', 'w') as file:
        file.write(new_date.strftime('%Y-%m-%d'))


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


def set_time(new_date):
    """
    Sets the current date to the given date.

    Parameters:
    ----------
    new_date : datetime.date
        The date to set as the new current date.

    Returns:
    -------
    None
    """
    set_current_date(new_date)  # Write the new date to the file as the current date


def main():
    """
Main function of the SuperPy application.

Returns:
-------
None
"""

    # Create the argument parser and add subparsers for each command
    parser = argparse.ArgumentParser(description='SuperPy')
    subparsers = parser.add_subparsers(dest='command')

    # Define subparser for the 'buy' command
    buy_parser = subparsers.add_parser('buy', help='buy a product')
    buy_parser.add_argument('product_name', type=str, help='the name of the product')
    buy_parser.add_argument('price', type=float, help='the price of the product')
    buy_parser.add_argument('expiration_date', type=str, help='the expiration date of the product in format YYYY-MM-DD')
    buy_parser.add_argument("--bought_file", type=str, default="bought.csv", help="Path to the bought file.")
    buy_parser.set_defaults(func=buy)

    # Define subparser for the 'sell' command
    sell_parser = subparsers.add_parser('sell', help='sell a product')
    sell_parser.add_argument('product_name', type=str, help='the name of the product')
    sell_parser.add_argument('price', type=float, help='the price at which the product is sold')
    sell_parser.add_argument('--bought_file', default='bought.csv', help='Path to the bought file')
    sell_parser.add_argument('--sold_file', default='sold.csv', help='Path to the sold file')
    sell_parser.set_defaults(func=sell)

    # Define subparser for the 'list' command
    list_parser = subparsers.add_parser('list', help='list bought and sold products')
    list_parser.add_argument(
        '--start_date',
        type=lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date(),
        help='the start date of the listing period in format YYYY-MM-DD'
    )
    list_parser.add_argument(
        '--end_date',
        type=lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date(),
        help='the end date of the listing period in format YYYY-MM-DD'
    )
    list_parser.add_argument('--bought_file', default='bought.csv', help='Path to the bought file')
    list_parser.add_argument('--sold_file', default='sold.csv', help='Path to the sold file')
    list_parser.set_defaults(func=list_products)

    # Define subparser for the 'revenue' command
    revenue_parser = subparsers.add_parser('revenue', help='calculate revenue over a period')
    revenue_parser.add_argument('--start_date', type=str, help='the start date of the revenue period in format YYYY-MM-DD')
    revenue_parser.add_argument('--end_date', type=str, help='the end date of the revenue period')
    revenue_parser.add_argument('--bought_file', default='bought.csv', help='Path to the bought file')
    revenue_parser.add_argument('--sold_file', default='sold.csv', help='Path to the sold file')
    revenue_parser.set_defaults(func=get_revenue)

    # Define subparser for the 'plot' command
    plot_parser = subparsers.add_parser('plot', help='plot revenue over a period')
    plot_parser.add_argument('--start_date', type=str, help='the start date of the revenue period in format YYYY-MM-DD')
    plot_parser.add_argument('--end_date', type=str, help='the end date of the revenue period')
    plot_parser.add_argument('--bought_file', default='bought.csv', help='Path to the sold file')
    plot_parser.set_defaults(func=plot_revenue)

    # Define subparser for the 'advance_time' command
    advance_time_parser = subparsers.add_parser('advance_time', help='advance the current date by a given number of days')
    advance_time_parser.add_argument('days', type=int, help='the number of days to advance the date by')
    advance_time_parser.set_defaults(func=advance_time)

    # Define subparser for the 'set_time' command
    parser_set_time = subparsers.add_parser('set_time', help='Set the current date to a specific date.')
    parser_set_time.add_argument('new_date', type=str, help='The new date to set (format: YYYY-MM-DD).')
    parser_set_time.set_defaults(command='set_time')

    # Create parser for deleting bought products
    delete_bought_parser = subparsers.add_parser("delete_bought", help="delete a row from the bought.csv file")
    delete_bought_parser.add_argument("id", type=int, help="The id of the bought product to delete.")
    delete_bought_parser.add_argument("--bought_file", default="bought.csv", help="The bought file to delete from.")
    delete_bought_parser.set_defaults(func=delete_bought)

    # Create parser for deleting sold products
    delete_sold_parser = subparsers.add_parser('delete_sold', help='Delete a sold product from the sales record')
    delete_sold_parser.add_argument('sold_id', type=int, help='ID of the sold product to delete')

    # Parse the arguments and execute the appropriate command
    args = parser.parse_args()

    # Call the appropriate function based on the subparser
    if hasattr(args, 'func'):
        args.func(args)
    # Execute the appropriate function based on the user's command

    elif args.command == 'revenue':
        # Get start and end dates from command line arguments
        start_date_str = args.start_date
        end_date_str = args.end_date
        # Read sold data from file
        sold_data = read_sold()
        # Filter sold data by start and end dates, if specified
        if start_date_str and end_date_str:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
            sold_data = filter_data_by_date(sold_data, start_date, end_date)
        # Calculate revenue and PrettyTable from filtered sold data
        revenue, table = calculate_revenue(sold_data)
        # Print revenue and table to the console
        print(f"Revenue: {revenue}")
        print(table)

    elif args.command == 'sell':
        # Extract product name and price from the arguments
        product_name = args.product_name
        price = args.price
        # Get the current date and format it as a string in the format
        # YYYY-MM-DD
        sold_date = get_current_date().strftime('%Y-%m-%d')
        # Read the data of bought products
        bought_data = read_bought()
        # Find the bought product with the matching name
        for bought_row in bought_data:
            if bought_row['product_name'] == product_name:
                # If a matching product is found, add a row to the sold data
                # with the relevant information
                sold_row = {'bought_id': bought_row['id'], 'product_name':
                            product_name, 'sell_price': price, 'sold_date': sold_date}
                sold_data = read_sold()
                sold_data.append(sold_row)
                write_sold(sold_data)
                print('OK')
                break
        else:
            # If no matching product is found, print an error message
            print('ERROR: Product not in stock.')

    elif args.command == 'list':
        # Retrieve the start and end dates from the command line arguments
        start_date_str = args.start_date
        end_date_str = args.end_date
        # Read in the bought and sold data
        bought_data = read_bought()
        sold_data = read_sold()
        # If start and end dates are specified, filter the data based on those
        # dates
        if start_date_str and end_date_str:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
            bought_data = filter_data_by_date(bought_data, start_date, end_date)
            sold_data = filter_data_by_date(sold_data, start_date, end_date)
        # Create a PrettyTable for the bought data
        bought_table = create_pretty_table(bought_data, ['product_name', 'buy_price', 'expiration_date', 'buy_date'])
        # Create a PrettyTable for the sold data
        sold_table = create_pretty_table(sold_data, ['product_name', 'sell_price', 'sold_date'])
        # Print the tables
        print('Bought:')
        print(bought_table)
        print('Sold:')
        print(sold_table)

    elif args.command == 'plot':
        # Get start and end dates from command line arguments
        start_date_str = args.start_date
        end_date_str = args.end_date
        # Call plot_revenue function with start and end dates
        plot_revenue(start_date_str, end_date_str)

    elif args.command == 'advance_time':
        # Extract the number of days to advance from the arguments
        days_to_advance = args.days
        # Get the current date
        current_date = get_current_date()
        # Calculate the new date by adding the number of days to advance to
        # the current date
        new_date = current_date + datetime.timedelta(days=days_to_advance)
        # Set the new date as the current date
        set_current_date(new_date)
        # Print a message to confirm that the date was successfully updated
        print('Current date set to:', new_date)

    elif args.command == 'set_time':
        # Parse the new date from the arguments
        new_date = datetime.datetime.strptime(args.new_date, "%Y-%m-%d").date()
        # Get the current date
        current_date = get_current_date()
        # Set the new date as the current date
        set_time(new_date)
        # Print a message to confirm that the date was successfully updated
        print('Current date set to:', new_date)

        # If no valid command was specified, print the help message
    else:
        parser.print_help()

# This line is used to ensure that the main function is only executed
# when the script is run as the main program, and not when it is imported
# as a module into another program


if __name__ == '__main__':
    main()

