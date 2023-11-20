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
    print("5. View Providers")
    print("6. View Employees")
    print("7. Place Order")
    print("8. Add a new product")
    print("0. Exit")
    print("-------------------")

# get all products
def view_products(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Product")
    products = cursor.fetchall()
    cursor.close()
    for product in products:
        print(product)

# get all customers
def view_customers(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customer")
    customers = cursor.fetchall()
    cursor.close()
    for customer in customers:
        print(customer)

# get all orders
def view_orders(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Order")
    orders = cursor.fetchall()
    cursor.close()
    for order in orders:
        print(order)

def view_carts(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cart")
    carts = cursor.fetchall()
    cursor.close()
    for cart in carts:
        print(cart)

def view_providers(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Provider")
    providers = cursor.fetchall()
    cursor.close()
    for provider in providers:
        print(provider)                

# Get all employees
def view_employees(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employee")
    employees = cursor.fetchall()
    cursor.close()
    for employee in employees:
        print(employee)    

#Place order 
def place_order(conn):
    customer_id = input("Enter Customer ID: ")
    product_id = input("Enter Product ID: ")
    quantity = int(input("Enter Quantity: "))

#add new product
def add_product(conn):
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

def main():
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
                view_providers(conn)
            elif choice == "6":
                view_employees(conn)
            elif choice == "7":
                place_order(conn)
            elif choice == "8":  # Adding a new option for adding a product
                add_product(conn)        
            else:
                print("Invalid choice. Please try again.")

        conn.close()
        print("Goodbye!")

if __name__ == "__main__":
    main()