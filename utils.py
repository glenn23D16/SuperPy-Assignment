import datetime
import datetime as dt
from prettytable import PrettyTable
import os


def get_current_date():
    """
    Gets the current date as a datetime.date object.

    If a current date is set in the `current_date.txt` file, return that date.
    Otherwise, return today's date.

    Returns:
    -------
    datetime.date
        The current date.
    """
    # Check if 'current_date.txt' file exists
    if os.path.exists('current_date.txt'):
        # Open the 'current_date.txt' file in read mode
        with open('current_date.txt', 'r') as file:
            # Read the date string from the file
            date_str = file.read().strip()
            # If the file is not empty, convert the date string to a date object using strptime
            # and return it
            return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        # If 'current_date.txt' file does not exist or is empty, return today's date
        return datetime.date.today()


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
