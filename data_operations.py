import csv
import os


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
        sold_reader = csv.DictReader(sold_file, delimiter=';')

        # Initialize an empty list to store the data
        sold_data = []

        # Loop over each row in the 'sold.csv' file
        for sold_row in sold_reader:
            # Append the row to the list of data
            sold_data.append(sold_row)

    return sold_data


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
        writer.writerow(["ID", "PRODUCT_NAME", "BUY_PRICE", "EXPIRATION_DATE", "BUY_DATE"])
        for row in bought_data:
            writer.writerow(row.values())


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
        sold_writer = csv.DictWriter(sold_file, fieldnames=sold_data[0].keys(), delimiter=';')
        # Write the headers to the 'sold.csv' file
        sold_writer.writeheader()
        # Write the data roles to the 'sold.csv' file
        sold_writer.writerows(sold_data)


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
        if sold_row['ID'] == args.id:
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
