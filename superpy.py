# Imports
import argparse
import datetime
import os
from prettytable import PrettyTable
from data_operations import read_bought, read_sold, write_sold, delete_bought, delete_sold
from command_functions import buy, sell, list_products, get_revenue, plot_revenue, advance_time
from utils import get_current_date, set_current_date, filter_data_by_date, calculate_revenue


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
    delete_sold_parser.add_argument('id', type=int, help='ID of the sold product to delete')
    delete_sold_parser.set_defaults(func=delete_sold)

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
            if bought_row['PRODUCT_NAME'] == product_name:

                # If a matching product is found, add a row to the sold data
                # with the relevant information
                sold_row = {'ID': bought_row['ID'], 'PRODUCT_NAME':
                            product_name, 'SELL_PRICE': price, 'SELL_DATE': sold_date}
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
        bought_table = create_pretty_table(bought_data, ['ID', 'PRODUCT_NAME', 'BUY_PRICE', 'EXPIRATION_DATE', 'BUY_DATE'])

        # Create a PrettyTable for the sold data
        sold_table = create_pretty_table(sold_data, ['ID', 'PRODUCT_NAME', 'SELL_PRICE', 'SELL_DATE'])

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
