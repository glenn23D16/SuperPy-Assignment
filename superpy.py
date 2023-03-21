# Imports
import argparse
import csv
import datetime
from datetime import datetime as dt
import os
import matplotlib.pyplot as plt
from prettytable import PrettyTable

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.


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


def write_bought(bought_data, filename):
    """
    Writes the given list of dictionaries to a CSV file with the given filename.

    Parameters:
    ----------
    bought_data : list of dict
        A list of dictionaries representing the data to be written to the file.
    filename : str
        The name of the file to which the data should be written.

    Returns:
    -------
    None
    """
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["id", "product_name", "buy_price", "expiration_date", "buy_date"])
        for row in bought_data:
            writer.writerow(row.values())


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
    Reads the 'sold.csv' file and returns its contents as a PrettyTable object.

    Returns:
    -------
    list
        A list with the rows from the 'sold.csv' file.
    """
    table = PrettyTable()
    with open('sold.csv', 'r', newline='') as file:
        reader = csv.DictReader(file, delimiter=';')
        headers = reader.fieldnames
        table.field_names = headers
        rows = []
        for row in reader:
            rows.append(row.values())
    return rows


def write_sold(sold_data):
    """
    Writes the given data to the 'sold.csv' file.

    Parameters:
    ----------
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
        # Write the data roles to the 'sold.csc' file
        sold_writer.writerows(sold_data)


def initialize_data_files(args):
    """
    Initializes the data files if they do not exist.

    Parameters:
    ----------
    args : argparse.Namespace
        The parsed command line arguments. Not used in this function.

    Returns:
    -------
    None
    """
    if not os.path.exists("bought_data.csv"):
        with open("bought_data.csv", "w") as file:
            file.write("id;product_name;buy_price;expiration_date;buy_date\n")

    if not os.path.exists("sold_data.csv"):
        with open("sold_data.csv", "w") as file:
            file.write("id;bought_id;product_name;sell_price;sold_date\n")

    if not os.path.exists("current_date.txt"):
        with open("current_date.txt", "w") as file:
            file.write("2023-03-18")


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
    for row in data:
        sell_date = dt.strptime(row['SELL_DATE'], '%Y-%m-%d').date()
        if start_date <= str(sell_date) <= end_date:
            filtered_data.append(row)
    return filtered_data


def get_revenue(args):
    """
    Retrieves the revenue data for a specified date range.

    Parameters:
    ----------
    args : argparse.Namespace
        The parsed command line arguments containing 'start_date' and 'end_date'.

    Returns:
    -------
    dict
        A dictionary with date keys and corresponding revenue values.
    """
    start_date = args.start_date
    end_date = args.end_date

    # Read the sold data
    sold_data = read_sold()

    # Filter the sold data by the given date range
    filtered_sold_data = [
        row for row in sold_data if start_date <= row["sell_date"] <= end_date
    ]

    # Calculate daily revenue
    revenue_data = {}
    for row in filtered_sold_data:
        date = row["sell_date"]
        revenue = float(row["sell_price"])
        if date in revenue_data:
            revenue_data[date] += revenue
        else:
            revenue_data[date] = revenue

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
    float
        The total revenue as a float.

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
    # Calculate the total revenue from the sold_data
    revenue = 0.0
    for row in sold_data:
        # Check if each row contains a 'sell_price' value
        if 'sell_price' not in row:
            raise ValueError("Missing sell_price value in sold_data.")
        revenue += float(row['sell_price'])

    # Create a PrettyTable object with the headers and data
    table_data = [{"Total Revenue": f"${revenue:.2f}"}]
    table = create_pretty_table(table_data)
    table.field_names = ["Total Revenue"]  # Add this line to set the field names

    # Return the revenue and table
    return revenue, table


def plot_revenue(start_date, end_date):
    """
    Plots the revenue over time for a given date range.

    Parameters:
    -----------
    start_date : str
        The start date of the revenue period in format YYYY-MM-DD.
    end_date : str
        The end date of the revenue period in format YYYY-MM-DD.

    Returns:
    --------
    None
    """
    # Get the revenue data for the specified time period
    revenue_data = get_revenue(start_date, end_date)

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
            profit += float(sold_row['SELL_PRICE']) - float(bought_row['BUY_PRICE'])  # Update the profit

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


def advance_time(days):
    """
    Advances the current date by the given number of days.

    Parameters:
    ----------
    days : int
        The number of days to advance the date by.

    Returns:
    -------
    None
    """
    current_date = get_current_date()  # Get the current date from file
    new_date = current_date + datetime.timedelta(days=days)  # Calculate the new date by adding days to current date
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
    buy_parser.add_argument('product_name', type=str,
                            help='the name of the product')
    buy_parser.add_argument('price', type=float,
                            help='the price of the product')
    buy_parser.add_argument('expiration_date', type=str,
                            help='the expiration date of the product in formatYYYY-MM-DD')
    buy_parser.set_defaults(func=buy)

    # Define subparser for the 'sell' command
    sell_parser = subparsers.add_parser('sell', help='sell a product')
    sell_parser.add_argument('product_name', type=str,
                             help='the name of the product')
    sell_parser.add_argument('price', type=float,
                             help='the price at which the product is sold')
    sell_parser.set_defaults(func=sell)

    # Define subparser for the 'list' command
    list_parser = subparsers.add_parser('list',
                                        help='list bought and sold products')
    list_parser.add_argument('--start_date', type=str,
                             help='the start date of the listing period in format YYYY-MM-DD') 
    list_parser.add_argument('--end_date', type=str,
                             help='the end date of the listing period in format YYYY-MM-DD')
    list_parser.set_defaults(func=list_products)

    # Define subparser for the 'revenue' command
    revenue_parser = subparsers.add_parser('revenue',
                                           help='calculate revenue over a period') 
    revenue_parser.add_argument('--start_date', type=str,
                                help='the start date of the revenue period in format YYYY-MM-DD')
    revenue_parser.add_argument('--end_date', type=str,
                                help='the end date of the revenue period')
    revenue_parser.set_defaults(func=revenue)

    # Define subparser for the 'plot' command
    plot_parser = subparsers.add_parser('plot',
                                        help='plot revenue over a period')
    plot_parser.add_argument('--start_date', type=str,
                             help='the start date of the revenue period in format YYYY-MM-DD')
    plot_parser.add_argument('--end_date', type=str,
                             help='the end date of the revenue period')
    plot_parser.set_defaults(func=plot)

    # Define subparser for the 'advance_time' command
    advance_time_parser = subparsers.add_parser('advance_time',
                                                help='advance the current date by a given number of days')
    advance_time_parser.add_argument('days', type=int,
                                     help='the number of days to advance the date by')
    advance_time_parser.set_defaults(func=advance_time)

    # Parse the arguments and execute the appropriate command
    args = parser.parse_args()

    # Initialize the data files if they do not exist
    initialize_data_files()
    
    if hasattr(args, 'func'):
        args.func(args)

    if args.command == 'buy':
        # Extract values from arguments
        product_name = args.product_name
        price = args.price
        expiration_date = args.expiration_date
        # Get current date and format it as string
        buy_date = get_current_date().strftime('%Y-%m-%d')
        # Create a dictionary representing the row to add to bought_data
        row = {'product_name': product_name, 'buy_price':
               price, 'expiration_date': expiration_date, 'buy_date': buy_date}
        # Read current data from bought_data file
        bought_data = read_bought()
        # Add the new row to the existing data
        bought_data.append(row)
        # Write the updated data back to the file
        write_bought(bought_data)
        # Print confirmation message
        print('OK')

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

    # If no valid command was specified, print the help message
    else:
        parser.print_help()

# This line is used to ensure that the main function is only executed
# when the script is run as the main program, and not when it is imported
# as a module into another program


if __name__ == '__main__':
    main()
