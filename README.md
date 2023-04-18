# SuperPy Usage Guide

**Overview**

SuperPy is a command-line application for managing the buying and selling of products. It allows you to keep track of the products you buy, when you bought them, and when you sell them, as well as generate reports on your revenue and profit over time.

**Usage**

To use SuperPy, open a command prompt or terminal and navigate to the directory containing the SuperPy program. From there, you can run the program using the following command:


```
python superpy.py [args]
```

The program accepts the following arguments:

```
-h, --help                Show this help message and exit
-s, --sell                Sell a product
-b, --buy                 Buy a product
-l, --list                List all bought products
-r, --revenue             Show revenue data
-p, --profit              Show profit data
-a, --advance [DAYS]      Advance the current date by DAYS

```

**Examples**

Here are some examples of how to use SuperPy:

product_name (required): The name of the product being sold.
price (required): The price at which the product is being sold.

Example usage:

```
python superpy.py sell apples 2.00
```

**Buy a Product**

To buy a new product, use the --buy flag followed by the product name, the buy price, the expiration date, and the buy date:

```
python superpy.py --buy "Apples" 0.50 "2023-03-25" "2023-03-21"
```

This will add a new product to the list of bought products.

**Sell a Product**

To sell a product, use the --sell flag followed by the product name, the sell price, and the sell date:
```
python superpy.py --sell "Apples" 0.75 "2023-03-22"
```
This will add a new entry to the list of sold products.

**List Bought Products**

To list all bought products, use the --list flag:
```
python superpy.py --list
```
This will print a table of all bought products.

**Show Revenue Data**

To show revenue data for a specified time period, use the --revenue flag followed by the start and end dates:

```
python superpy.py --revenue "2023-03-01" "2023-03-31"
```
This will print a table of the revenue for each day within the specified time period.

**Show Profit Data**

To show profit data, use the --profit flag:

```
python superpy.py --profit
```

**Advance the Current Date**

To advance the current date by a specified number of days, use the --advance flag followed by the number of days to advance:

```
python superpy.py --advance 7
```
# Conclusion

SuperPy is a powerful tool for managing the buying and selling of products. It allows you to keep track of your products and generate reports on your revenue and profit over time. With its user-friendly command-line interface and flexible command-line arguments, SuperPy is a must-have tool for anyone who needs to manage products.