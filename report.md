# SuperPy: Technical Report

In this report, we will discuss three notable technical elements of the SuperPy implementation, the problems they solve, and the rationale behind their implementation.

**1. Argument Parsing with argparse**

SuperPy utilizes the argparse library to handle command-line arguments, simplifying input processing and enabling the easy creation of subcommands for various tasks.

```
parser = argparse.ArgumentParser(description='SuperPy')
subparsers = parser.add_subparsers(help='Available commands', dest='command')
```

Argparse allows us to define subparsers for each command, such as buy, sell, list and delete. Each subparser has its arguments defined, making it easy for users to understand what input is required. This approach eliminates the need for manual input parsing and validation, resulting in cleaner and more maintainable code.

**2. File I/O for Data Persistence**

SuperPy stores data in CSV files to maintain state and persist information between sessions. Functions like read_bought, write_bought, read_sold, and write_sold handle file I/O operations.

```
def read_bought():
    with open('bought.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]
```

By using the csv module, we can easily read and write data from/to CSV files, ensuring data persistence even after the program has been terminated. This implementation simplifies data handling and enables the program to scale efficiently as the data grows.

**3. Date Filtering with datetime**

The SuperPy program allows users to filter and display data based on date ranges. To achieve this functionality, the datetime module is used to parse and compare dates.

```
def filter_data_by_date(data, start_date, end_date):
    return [row for row in data if start_date <= datetime.datetime.strptime(row['date_field'], '%Y-%m-%d').date() <= end_date]
```

By leveraging the datetime module, we can parse, compare, and manipulate dates with ease. This approach provides a reliable and efficient method for handling date filtering tasks in the SuperPy program.

In conclusion, the SuperPy program employs argparse for streamlined input processing, uses file I/O for data persistence, and takes advantage of the datetime module for date filtering. These technical elements contribute to a more efficient, user-friendly, and maintainable solution for inventory management.
