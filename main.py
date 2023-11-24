import psycopg2
from datetime import datetime

# Connect to the PostgreSQL database
def connect_to_database():
    try:
        conn = psycopg2.connect(
            host="localhost",dbname="Final Project COP4710",user = "postgres",password="5822",port=5432
            )
        
        return conn
    
    except Exception as e:
        print("Error:", e)
        return None

# interface menu options
def display_menu():
    print("\n------ T6 Electronics ------")
    print("1. View Products")
    print("2. View Customers")
    print("3. View Orders")
    print("4. View Carts")
    print("5. Add Employee")
    print("6. View Employees")
    print("7. Place Order")
    print("8. Add a new product")
    print("9. Update a product")
    print("10. Add a customer")
    print("11. Delete product")
    print("0. Exit")
    print("-------------------")

# get all products
def view_products(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Product WHERE deleted=false")
    products = cursor.fetchall()
    cursor.close()
    print("Here are the products:")
    for product in products:
        print(product)

# get all customers
def view_customers(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customer")
    customers = cursor.fetchall()
    cursor.close()
    print("Here are the customers:")
    for customer in customers:
        print(customer)

# get all orders
def view_orders(conn):
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT o.orderid, o.employeeid, o.customerid, c.productid, p.name
                   FROM orders o
                   JOIN cart c ON o.orderid = c.orderid
                   JOIN product p ON c.productid = p.productid
                   """)
    orders = cursor.fetchall()
    cursor.close()
    print("Here are the orders:")
    for order in orders:
        print("orderid: " + str(order[0]) + 
              " employeeid: " + str(order[1]) +
              " customerid: " + str(order[2])  + 
              " productid: " + str(order[3]) +
              " product name: " + order[4])

def view_carts(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cart")
    carts = cursor.fetchall()
    cursor.close()
    for cart in carts:
        print(cart)

def add_employee(conn): #Add a new employee
    try:
       cursor = conn.cursor()

       firstname = input("Enter first name: ")
       lastname = input("Enter last name: ")
       phone = input("Enter Phone: ")
       email = input("Enter Email: ")
       address = input("Enter Address: ")
       salary = float(input("Enter Salary: "))
       position = input("Enter Position: ")
       datehired = input("Enter the product received date (YYYY-MM-DD): ")

        # Convert the input date string to a datetime object
       datehired = datetime.strptime(datehired, "%Y-%m-%d").date()

       cursor.execute("""
            INSERT INTO employee (firstname, lastname, phone, email, address, salary,position,datehired)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (firstname, lastname, phone, email, address, salary,position,datehired))
        
       conn.commit()

       print(f"Employee '{firstname}' '{lastname}' added successfully!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cursor.close()            


def view_employees(conn): # Display all employees
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employee")
    employees = cursor.fetchall()
    cursor.close()
    for employee in employees:
        print(employee)    


def place_order(conn): #Place a new order
    customer_id = int(input("Enter customer id: "))
    employee_id = int(input("Enter employee id: ")) # store employee id in order

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (customerid, employeeid, order_status)
        VALUES (%s, %s, TRUE)
        RETURNING orderid
    """, (customer_id, employee_id))

    order_id = cursor.fetchone()[0]

    conn.commit()
    print("order placed")

    # create an order using the above with order_status set to 0
    # get order id of this newly created order
    
    view_products(conn) #display all products
    while True:
        choice = input("Enter product id (0 to exit): ")
        if choice == "0":
                break
        else:
            cursor.execute("""
                INSERT INTO cart (productid, orderid)
                VALUES (%s, %s)
            """, (choice, order_id))

            conn.commit()

            

def add_product(conn): #add a new product
    try:
       cursor = conn.cursor()

       name = input("Enter the product name: ")
       description = input("Enter the product description: ")
       price = float(input("Enter the product price: "))
       quantity = int(input("Enter the product quantity: "))
       brand = input("Enter the product brand: ")
       type = input("Enter the product type: ")
       date_received = input("Enter the product received date (YYYY-MM-DD): ")

        # Convert the input date string to a datetime object
       datereceived = datetime.strptime(date_received, "%Y-%m-%d").date()

       cursor.execute("""
            INSERT INTO Product (name, description, price, quantity, brand, type, datereceived)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, description, price, quantity, brand, type, datereceived))
        
       conn.commit()

       print(f"Product '{name}' added successfully!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cursor.close()

#update an existing product
def update_product(conn): #Update an existing Product
    try:
       cursor = conn.cursor()

       update_id = input("Enter product id: ")

       name = input("Enter new product name: ")
       description = input("Enter new product description: ")
       price = float(input("Enter new product price: "))
       quantity = int(input("Enter new product quantity: "))
       brand = input("Enter new product brand: ")
       type = input("Enter new product type: ")
       date_received = input("Enter new product received date (YYYY-MM-DD): ")

        # Convert the input date string to a datetime object
       datereceived = datetime.strptime(date_received, "%Y-%m-%d").date()

       cursor.execute("""
            UPDATE Product
            SET name=%s, description=%s, price=%s, quantity=%s, brand=%s, type=%s, datereceived=%s
            WHERE productid=%s
        """, (name, description, price, quantity, brand, type, datereceived, update_id))
        
       conn.commit()

       print(f"Product '{name}' updated successfully!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cursor.close()

#add new customer
def add_customer(conn): #add a new customer
    try:
       cursor = conn.cursor()

       firstname = input("Enter first name: ")
       lastname = input("Enter last name: ")
       phone = input("Enter phone: ")
       email = input("Enter email: ")
       address = input("Enter address: ")
       creditcard = int(input("Enter credit card: "))

       cursor.execute("""
            INSERT INTO Customer (firstname, lastname, phone, email, address, paymentinfo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (firstname, lastname, phone, email, address, creditcard))
        
       conn.commit()

       print(f"Customer '{firstname}' '{lastname}' added successfully!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cursor.close()

def delete_product(conn): #Delete a Product
    view_products(conn)

    product_id = input("Enter product id to delete: ")
    
    cursor = conn.cursor()
    cursor.execute("""
                   DELETE from product WHERE productid=%s
                   """, (product_id))
    
    conn.commit()

    print("Product successfully deleted")
    cursor.close()



def main(): #shows user the menu and  runs queries based on the input
    conn = connect_to_database()

    if conn:
        while True:
            display_menu()
            choice = input("Enter your choice (0 to exit): ")

            if choice == "0":
                break
            elif choice == "1":
                view_products(conn)
            elif choice == "2":
                view_customers(conn)
            elif choice == "3":
                view_orders(conn)
            elif choice == "4":
                view_carts(conn)
            elif choice == "5":
                add_employee(conn)
            elif choice == "6":
                view_employees(conn)
            elif choice == "7":
                place_order(conn)
            elif choice == "8":
                add_product(conn)
            elif choice == "9": 
                update_product(conn)
            elif choice == "10": 
                add_customer(conn)
            elif choice == "11": 
                delete_product(conn)   
            else:
                print("Invalid choice. Please try again.")

        conn.close()
        print("Goodbye!")

if __name__ == "__main__":
    main()