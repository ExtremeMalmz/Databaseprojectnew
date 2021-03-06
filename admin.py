#Eric Malmström - Informationsarkitektsprogrammet Malmö Universitet - Databasteknik VT2022-DA297A

from main import printAllProducts

from psycopg2 import errors

UniqueViolation = errors.lookup('23505')

def admin_menu_printer(message):
    '''prints 20 equal signs, does a new line, prints the inputted message, and new lines and prints 20 more equal signs'''

    print("="*20 + '\n' + message + '\n' + "="*20)

def add_a_supplier(connection):
    '''adds a supplier to the supplier table'''

    admin_menu_printer("Add a Supplier")

    supplierName = str(input("Enter the name of supplier: "))
    telephoneNmr = int(input("Enter the telephone number of supplier (ONLY NUMBERS): "))
    streetNmr = str(input("Enter the street and number of the supplier: "))
    zipcode = int(input("Enter the zip code of the supplier: "))
    city = str(input("Enter the city of the supplier: "))
    country = str(input("Enter the country of the supplier: "))
   

    cursor = connection.cursor()
    cursor.execute("INSERT INTO suppliers (suppliername,telephonenmr,streetnmr,zipcode,city,country) VALUES (%s,%s,%s,%s,%s,%s)", (supplierName,telephoneNmr,streetNmr,zipcode,city,country))
    connection.commit()
    
    cursor.close()

def add_a_product(connection):
    '''adds a product to the product table'''    

    admin_menu_printer("Add a Product")

    productName = str(input("Enter the product name: "))
    price = int(input("Enter the price (NUMBERS ONLY): "))
    supplier = str(input("Enter a supplier: "))
    quantity = int(input("Enter initial quantity of product (NUMBERS ONLY): "))

    cursor = connection.cursor()  
    cursor.execute("INSERT INTO products (productName,baseprice,supplier,quantity,discountprice) VALUES (%s,%s,%s,%s,%s)",(productName,price,supplier,quantity,price))
    connection.commit()

    cursor.close()

def add_a_discount(connection):
    '''adds a discount to discount table'''

    admin_menu_printer("Add a Discount")

    discountName = str(input("Enter the name of the discount: "))
    discountPercentage = int(input("Enter the percentage of the discount: "))
    startdate = str(input("Enter the date when the discount starts (YYYYMMDD): "))
    enddate = str(input("Enter the date when the discount ends (YYYYMMDD): "))

    cursor = connection.cursor()
    cursor.execute("INSERT INTO discounts (discountname,discountpercentage,startdate,enddate) VALUES (%s,%s,%s,%s)",(discountName,discountPercentage,startdate,enddate))
    connection.commit()

    cursor.close()

def add_a_discount_to_product(connection):
    '''adds a discount to a product in the table discountsandproducts'''

    admin_menu_printer("Add Discount to Product")

    productID = int(input("Enter product ID (NUMBERS ONLY): "))
    productName = str(input("Enter the product name: "))
    discountID = int(input("Enter discount ID (NUMBERS ONLY): "))
    discountName = str(input("Enter the name of the discount: "))
    
    cursor = connection.cursor()
    cursor.execute("INSERT INTO discountsAndProducts (productID,productname,discountid,discountname) VALUES (%s,%s,%s,%s)",(productID,productName,discountID,discountName))
    connection.commit()

    cursor.close()

def edit_quantity_of_products(connection):
    '''prints the quantity of products and then asks for the new amount'''

    admin_menu_printer("Edit the amount of products")

    productID = int(input("Enter the productID to display amount: "))

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE productID = %s AND productID = %s",(productID,productID))
    records = cursor.fetchall()
    for row in records:
        print("Product amount/quantity: ", row[4])

    productAmount = int(input("Enter the amount to change the amount of products to: "))

    cursor.execute("UPDATE products SET quantity = %s WHERE productID = %s",(productAmount,productID))
    connection.commit()

    cursor.close()
    
def delete_a_product(connection):
    '''deletes a product from product table'''

    admin_menu_printer("Delete a Product")

    productID = int(input("Enter the productID to delete it: "))

    cursor = connection.cursor()
    cursor.execute("DELETE FROM products WHERE productID = %s AND productID = %s",(productID,productID))
    connection.commit()

    cursor.close()

def list_all_products_admin(connection):
    '''lists all products'''

    admin_menu_printer("Print all Products")

    printAllProducts(connection)

def search_products_by_name(connection):
    '''able to search for products based on product name'''

    productName = str(input("What is the name of the product you are searching for: "))

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE productname = %s AND productname = %s",(productName,productName))
    records = cursor.fetchall()
    for row in records:
        print("Product ID: ", row[0]),
        print("Product name: ", row[1]),
        print("Base price: ", row[2]),
        print("Supplier: ", row[3]),
        print("Quantity in stock: ", row[4]),

    cursor.close()

def search_products_by_supplier(connection):
    '''able to search for products based on supplier name'''

    productSupplier = str(input("What is the name of the supplier you are searching for: "))

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE supplier = %s AND supplier = %s",(productSupplier,productSupplier))
    records = cursor.fetchall()
    for row in records:
        print("Product ID: ", row[0]),
        print("Product name: ", row[1]),
        print("Base price: ", row[2]),
        print("Supplier: ", row[3]),
        print("Quantity in stock: ", row[4]),

    cursor.close()
    

def search_products_admin(connection):
    '''admin main for searching for products'''
    admin_menu_printer("Search Products")

    adminInput = str(input("1-Search by product name \n2-Search by supplier \n"))
    match adminInput:
        case '1':
            search_products_by_name(connection)
        case '2':
            search_products_by_supplier(connection)

def see_discount_history(connection):
    '''prints all discounts and the dates they are active'''

    admin_menu_printer("See Discount history")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM discounts")
    records = cursor.fetchall()
    for row in records:
        print("===")
        print("Discount ID: ", row[0]),
        print("Discount name: ", row[1]),
        print("Discount percent: ", row[2]),
        print("Discount start date: ", row[3]),
        print("Discount end date: ", row[4])

    cursor.close()

def add_confirmed_order_to_maximum_orders(connection,adminInput,cursor):
    '''adds the data from a confirmed order to the maximum order table'''
    
    cursor.execute("SELECT * FROM orders WHERE confirmedOrder = 'yes' AND orderID = %s AND orderID = %s",(adminInput,adminInput))
    records = cursor.fetchall()
    for row in records:
        productID = int(row[2])
        orderAmount = int(row[4])
        orderDate = str(row[5])
    
    print(f"Order amount: {orderAmount} \nOrder date: {orderDate}")
    orderYear = orderDate[0]+orderDate[1]+orderDate[2]+orderDate[3]
    orderMonth = orderDate[5]+orderDate[6]
    print(f"Product ID: {productID} \nOrder year: {orderYear} \nOrder month: {orderMonth}")

    cursor.execute("SELECT * FROM maximumorders WHERE orderYear = %s AND productID = %s",(orderYear,productID))
    records = cursor.fetchall()
    if records == []:
        cursor.execute("INSERT INTO maximumorders (orderYear,orderMonth,productID,amountSold) VALUES (%s,%s,%s,%s)",(orderYear,orderMonth,productID,orderAmount))
    else:
        for row in records:
            originalSales = int(row[3])

        print(f"{originalSales} + {orderAmount}")
        totalSales = originalSales + orderAmount
        print(totalSales)
        print(productID)
        
        cursor.execute("UPDATE maximumorders SET amountsold = %s WHERE productID = %s",(totalSales,productID))
    connection.commit()

    cursor.close()

def confirm_orders(connection):
    '''prints a list of unconfirmed orders and if the order ID is inputted its status may change from unconfirmed to confirmed'''

    admin_menu_printer("Confirm customer Orders")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM orders WHERE confirmedOrder = 'no'")
    records = cursor.fetchall()
    print("LIST OF UNCONFIRMED ORDERS")
    for row in records:
        print("Order ID: ", row[0])

    adminInput = int(input("Enter the orderID to confirm the order: "))
    cursor.execute("UPDATE orders SET confirmedOrder = 'yes' WHERE orderID = %s AND orderID = %s",(adminInput,adminInput))
    connection.commit()

    add_confirmed_order_to_maximum_orders(connection,adminInput,cursor)
    
def see_maximum_orders(connection):
    '''lists the products sold by id, month, year, and amount sold'''

    admin_menu_printer("Maximum Orders sorted by amount sold")
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM maximumorders ORDER BY amountsold DESC")
    records = cursor.fetchall()
    for ele,row in enumerate(records):
        print(f"Place #{ele+1}")

        print("Order year: ", row[0]),
        print("Order month: ", row[1]),
        print("Product ID: ", row[2]),
        print("Amount sold: ", row[3]),
        print("---")

def adminMain(connection):
    '''main for admin accounts'''

    while(True):
        admin_menu_printer("Welcome administrator")
        print("1- Add a supplier\n2- Add a product \n3- Add a discount \n4- Add discounts to products \n5- Edit quantity of available product \n6- Delete a product \n7- See a list of products \n8- Search products \n9- See discount history \n10- Confirm orders \n11- See maximum orders")
        userInput = str(input("Your choice: "))

        match userInput:
            case '1':
                add_a_supplier(connection)
            case '2':
                add_a_product(connection)
            case '3':
                add_a_discount(connection)
            case '4':
                add_a_discount_to_product(connection)
            case '5':
                edit_quantity_of_products(connection)
            case '6':
                delete_a_product(connection)
            case '7':
                list_all_products_admin(connection)
            case '8':
                search_products_admin(connection)
            case '9':
                see_discount_history(connection)
            case '10':
                confirm_orders(connection)
            case '11':
                see_maximum_orders(connection)