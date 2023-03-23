# SuperPy Usage Guide

**Overview**

SuperPy is a command-line program designed to manage an inventory of bought and sold products. The program allows you to buy products, sell products, list bought and sold products, calculate revenue over a period, plot revenue over a period, and advance the current date.

**Commands**

Buy a Product:

To buy a product, use the following command:


```
python your_superpy_file.py buy <product_name> <price> <expiration_date> [--bought_file <bought_file_path>]
```

- <product_name>: The name of the product
- <price>: The price of the product
- <expiration_date>: The expiration date of the product in YYYY-MM-DD format
- <bought_file_path> (optional): Path to the bought file. Default is bought.csv

```
python your_superpy_file.py buy Apples 2.5 2023-04-30
```

**Sell a Product**

To sell a product, use the following command:

```
python your_superpy_file.py sell <product_name> <price> [--sold_file <sold_file_path>]
```
- <product_name>: The name of the product
- <price>: The price at which the product is sold
- <sold_file_path> (optional): Path to the sold file. Default is sold.csv

Example: 

```
python your_superpy_file.py sell Apples 3.0
```

**List Bought and Sold Products**

To list bought and sold products, use the following command:

```
python your_superpy_file.py list [--start_date <start_date>] [--end_date <end_date>]
```

- <start_date> (optional): The start date of the listing period in YYYY-MM-DD format
- <end_date> (optional): The end date of the listing period in YYYY-MM-DD format

Example: 

```
python your_superpy_file.py list --start_date 2023-03-01 --end_date 2023-03-31
```

**Calculate Revenue Over a Period**

To calculate revenue over a period, use the following command:

```
python your_superpy_file.py revenue [--start_date <start_date>] [--end_date <end_date>]
```
- <start_date> (optional): The start date of the revenue period in YYYY-MM-DD format
- <end_date> (optional): The end date of the revenue period in YYYY-MM-DD format

Example:

```
python your_superpy_file.py revenue --start_date 2023-03-01 --end_date 2023-03-31
```

**Plot Revenue Over a Period**

To plot revenue over a period, use the following command:
```
python your_superpy_file.py plot [--start_date <start_date>] [--end_date <end_date>]
```
- <start_date> (optional): The start date of the revenue period in YYYY-MM-DD format
- <end_date> (optional): The end date of the revenue period in YYYY-MM-DD format

Example:

```
python your_superpy_file.py plot --start_date 2023-03-01 --end_date 2023-03-31
```

**Advance Time**

To advance the current date by a given number of days, use the following command:

```
python your_superpy_file.py advance_time <days>
```

- <days>: The number of days to advance the date by

Example:

```
python your_superpy_file.py advance_time 7
```

# Conclusion

It is intended that this usage guide helps you effectively utilize the SuperPy program to manage your inventory of bought and sold products. By using the various commands provided, you can efficiently track product purchases, sales, and revenue over time. Remember to consult this guide if you need assistance with the command syntax or examples. Good luck and happy inventory management!
