import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(host="localhost", dbname="Final Project COP4710", user = "postgres", password="5822",port=5432)


def display_menu():
    print("T6 Electronics - Enterprise Information System")
    print("1. View Products")
    print("2. View Customers")
    print("3. Place an Order")
    print("4. View Employees")
    # Add more options for other functionalities
    print("0. Exit")


def retrieve_products():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()
    cursor.close()
    return products

def retrieve_customers():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer")
    customers = cursor.fetchall()
    cursor.close()
    return customers

def retreive_employees():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee")
    employees = cursor.fetchall()
    cursor.close()
    return employees    

def place_order(customer_id, employee_id, date, total_amount):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Orders (CustomerID, EmployeeID, Date, TotalAmount) VALUES (%s, %s, %s, %s)", (customer_id, employee_id, date, total_amount))
    conn.commit()
    cursor.close()
    return "Order placed successfully."

while True:
    display_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
        products = retrieve_products()
        # Display products
    elif choice == "2":
        customers = retrieve_customers()
        # Display customers
    elif choice == "3":
        # Gather input for placing an order
        customer_id = int(input("Enter Customer ID: "))
        employee_id = int(input("Enter Employee ID: "))
        date = input("Enter Order Date (YYYY-MM-DD): ")
        total_amount = float(input("Enter Total Amount: "))
        result = place_order(customer_id, employee_id, date, total_amount)
        print(result)
    elif choice == "4":
        # Gather input for placing an order
        employees = retreive_employees()    
    # Add more options and queries handling
    elif choice == "0":
        break
    else:
        print("Invalid choice. Please try again.")