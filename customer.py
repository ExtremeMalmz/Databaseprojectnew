#Eric Malmström - Informationsarkitektsprogrammet Malmö Universitet - Databasteknik VT2022-DA297A

from datetime import date
todaysDate = date.today()

def customer_menu_printer(message):
    '''prints 20 equal signs, does a new line, prints the inputted message, and new lines and prints 20 more equal signs'''

    print("="*20 + '\n' + message + '\n' + "="*20)

def print_All_Products(connection):
    '''lists the products in the products table'''
    customer_menu_printer("Listing all products")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    records = cursor.fetchall()
    for row in records:
        print("---")
        print("Product ID: ", row[0]),
        print("Product Name:", row[1]),
        print("Baseprice : ", row[2]),
        print("Supplier : ", row[3]),
        print("Quantity : ", row[4])

    cursor.close()

def search_by_ID(connection,date):
    '''search via the product ID in product table'''
    productID = str(input("Enter the ID of the product you wish to find\n"))

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Products WHERE productID = %s AND productID = %s", (productID,productID))
    records = cursor.fetchall()

    if records == []:
        print("Product not found!")
    else:   
        for row in records:
            basePrice = row[2] 
            print("Product ID: ", row[0]),
            print("Product Name:", row[1]),
            print("Baseprice : ", row[2]),
            print("Supplier : ", row[3]),
            print("Quantity : ", row[4])

    cursor.execute("SELECT * FROM discountsAndProducts INNER JOIN discounts ON (discountsAndProducts.discountID = discounts.discountID AND discounts.startdate<=%s AND discounts.endDate >= %s AND productID = %s)",(date, date,productID))
    records = cursor.fetchall()

    if records == []:
        print("No discount for this product")
    else:
        for row in records:
            discountPercentOriginal = row[6]
            discountPercent = float(discountPercentOriginal)/100
            totalPrice = int(discountPercent*basePrice)
        print(f"Discount amount: {discountPercentOriginal}%")
        print(f"Total price is {totalPrice}")
        
    cursor.close()

def search_by_name(connection,date):
    '''search by the product name in product table'''

    productName = str(input("Enter the name of the product you wish to find\n"))

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Products WHERE productName = %s AND productName = %s", (productName,productName))
    records = cursor.fetchall()

    if records == []:
        print("Product not found!")
    else:   
        for row in records:
            basePrice = row[2] 
            print("Product ID: ", row[0]),
            print("Product Name:", row[1]),
            print("Baseprice : ", row[2]),
            print("Supplier : ", row[3]),
            print("Quantity : ", row[4])

    cursor.execute("SELECT * FROM discountsAndProducts INNER JOIN discounts ON (discountsAndProducts.discountID = discounts.discountID AND discounts.startdate<=%s AND discounts.endDate >= %s AND productName = %s)",(date, date,productName))
    records = cursor.fetchall()

    if records == []:
        print("No discount for this product")
    else:
        for row in records:
            discountPercentOriginal = row[6]
            discountPercent = float(discountPercentOriginal)/100
            totalPrice = int(discountPercent*basePrice)
        print(f"Discount amount: {discountPercentOriginal}%")
        print(f"Total price is {totalPrice}")

def search_Discounts(connection,date):
    '''lists discounts available on the date which was inputted at the log in'''

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM discountsAndProducts INNER JOIN discounts ON (discountsAndProducts.discountID = discounts.discountID AND discounts.startdate<=%s AND discounts.endDate >= %s)",(date, date))
    records = cursor.fetchall()
 
    if records == []:
        print("No discounted product found")
    else:
        for row in records:
            print("---\nDISCOUNTED PRODUCT\n---")
            print("product ID: ", row[0]),
            print("product Name: ", row[1]),
            print("Discount ID: ", row[2]),
            print("Discount reason: ", row[3]),
            print("Discount percentage: ", row[6], "%"),
            print("Start date: ", row[7]),
            print("End date: ", row[8])
            
    cursor.close()

def search_Products(connection,date):
    '''the main for searching products'''

    customer_menu_printer("Search for a product")
    print("1-Search by ID \n2-Search by Product Name \n3-See all ongoing discounts \n4-Search by price \n")
    userInput = str(input("Your choice: "))
    
    match userInput:
        case '1':
            search_by_ID(connection,date)
        case '2':
            search_by_name(connection,date)
        case '3':
            search_Discounts(connection,date)


def add_to_shopping_list(connection,email,date):
    '''adds a product to the shopping list'''

    customer_menu_printer("Add to your shopping list")

    newAmount = 0
    productID = int(input("Enter product ID: "))
    productName = str(input("Enter product name: "))
    productAmount = int(input("Enter the amount you'd like to buy: "))

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE productID = %s AND productName = %s",(productID,productName))
    records = cursor.fetchall()
    for row in records:
        originalAmount = row[4]
        newAmount = originalAmount - productAmount
    if newAmount < 0:
        print("Product amount not available")
    else:
        cursor.execute("UPDATE Products SET quantity = %s WHERE productID = %s",(newAmount,productID))
        connection.commit()
        print(f"You have sucessfully ordered {productAmount} of the product {productName}")
        print("Thanks for your purchase and an admin will confirm your order shortly")

    cursor.execute("INSERT INTO orders (useremail,productId,productname,productamount,dateordered,confirmedorder) VALUES (%s,%s,%s,%s,%s,%s)",(email,productID,productName,productAmount,date,'no'))
    connection.commit()

    cursor.close()
    
def view_shopping_list(connection,email):
    '''prints the customers total shopping list'''

    customer_menu_printer("Displaying shopping list")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM orders WHERE userEmail = %s AND userEmail = %s",(email,email))
    records = cursor.fetchall()
    for row in records:
        print("Order id: ", row[0]),
        print("Product id: ", row[2]),
        print("Product name: ", row[3]),
        print("Product amount: ", row[4]),
        print("Date ordered: ", row[5]),
        print("Confirmed order status: ", row[6])
        print("---")
    
    cursor.execute("SELECT * FROM orders INNER JOIN products ON (orders.productID = products.productID AND useremail = %s AND useremail = %s)",(email,email))
    records = cursor.fetchall()

    totalProductPrice = 0
    for row in records:
        
        productAmount = row[4]
        productPrice = row[9]

        totalProductPrice = (productAmount*productPrice)+totalProductPrice
    print(f"Original cost is: {totalProductPrice}")    
        
    cursor.execute("SELECT orders.productAmount,discounts.discountPercentage,products.discountprice FROM orders INNER JOIN discountsandproducts ON(discountsandproducts.productId = orders.productID AND userEmail = %s and userEmail = %s) INNER JOIN discounts ON(discounts.discountID = discountsandproducts.discountID AND startdate <= orders.dateOrdered AND enddate >= orders.dateOrdered) INNER JOIN products ON(products.productID = orders.productId)",(email,email))
    records = cursor.fetchall()

    totalDiscountPrice = 0
    for row in records:
        discountProductAmount = row[0]
        discountPercent = row[1]
        price = row[2]

        discountPercent = float(discountPercent)/100
        totalDiscountPrice = ((discountProductAmount * price)*discountPercent)+totalDiscountPrice  

    print(f"Total discounts are: {totalDiscountPrice}")
    finalPrice = totalProductPrice - totalDiscountPrice
    print(f"Final price is {finalPrice}")

    userInput = str(input("Do you want to pay this price?").upper())
    if userInput == 'YES':
        print("Thanks for paying!")
    else:
        print("Maybe next time")

    cursor.close()

def delete_from_shopping_list(connection,email):
    '''the customer is able to delete an order from the shopping list here'''

    customer_menu_printer("Delete an Order")

    userInput = int(input("Enter the order ID to cancel it. If the order is confirmed you cant delete it: "))
    
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Orders WHERE useremail = %s AND orderID = %s", (email,userInput))
    records = cursor.fetchall()
    for row in records:
        print("Amount of product deleted: ", row[4])

    if records != []:
        cursor.execute("SELECT * FROM orders INNER JOIN products ON (orders.productID = products.productID AND useremail = %s AND orderID = %s)",(email,userInput))
        records = cursor.fetchall()
        for row in records:
            productID = row[2]
            orderProductAmount = row[4]
            totalProductAmount = row[11]
            
        
        totalProductAmount += orderProductAmount

        cursor.execute("UPDATE products SET quantity = %s WHERE productID = %s", (totalProductAmount,productID))
        connection.commit()

        cursor.execute("DELETE FROM orders WHERE orderID = %s AND userEmail = %s AND confirmedOrder = 'no'",(userInput,email))
        connection.commit()
        print("Order successfully deleted")
    else:
        print("Unable to delete order")
        
    cursor.close()

def customerMain(connection,email):
    '''the main for the logged in customer'''
    
    print(f"Before you continue please enter the date (Todays date is: {todaysDate})\n OBSERVE: Write the date in numbers only")
    date = str(input("Type here: "))
    print(f"Date: {date}")

    while(True):
        customer_menu_printer("Welcome to the main Customer page")
        print("1- See products \n2- Search products \n3- See discounted products \n4- Add a product to your shopping list \n5- View shopping list\n6- Delete order from shopping list")
        
        userInput = str(input("Your input: "))
        match userInput:
            case '1':
                print_All_Products(connection)
            case '2':
                search_Products(connection,date)
            case '3':
                search_Discounts(connection,date)
            case '4':
                add_to_shopping_list(connection,email,date)
            case '5':
                view_shopping_list(connection,email)
            case '6':
                delete_from_shopping_list(connection,email)
            case _:
                print("I didnt understand that...")