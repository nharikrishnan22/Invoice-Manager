"""This program can create, check for invoices that have not been paid and change whether invoices have been paid or not
"""

success = 0 # login success (0 for failure)


# Main screen
def main():
    try:
        ctypes.windll.kernel32.SetConsoleTitleA(b" Invoice program")
        choice = int(input("""1. Create a new invoice
2. Check invoices
3. Create new table of invoices
4. Edit invoice
5. Delete invoice
6. Help
7. Exit
Choice: """
                           ))
        if choice == 1:
            os.system('cls')
            new_invoice()
        if choice == 2:
            os.system('cls')
            check_invoice()
        if choice == 3:
            os.system('cls')
            new_table()
        if choice == 4:
            os.system('cls')
            edit_invoice()
        if choice == 5:
            os.system('cls')
            delete_invoice()
        if choice == 6:
            os.system('cls')
            help_invoice()
        if choice == 7:
            mydb.close() # close MySQL database connection
            quit()
        elif choice>7 or choice<1:
            print('Invalid input.')
            input('Press enter to continue.')
            os.system('cls')
            main()
    except ValueError: # if the input is a string or another data type other than an integer. This error appears in other functions e.g. check_invoices
        print('Invalid input.')
        input('Press enter to continue.')
        os.system('cls')
        main()

# Create a new invoice
def new_invoice():
    try:
        invoice_number = int(input("Type in the invoice number: "))
        status_invoice = str(input('Type in the status of the invoice (not paid/paid): '))
        if status_invoice != "not paid" and status_invoice!= "paid":
            input('Your invoice status is not valid. Press enter to try again.')
            os.system('cls')
            new_invoice()
        value_invoice = int(input('Type in the value of the invoice (without pound sign): '))
        day_invoice = int(input('Type in the day of the invoice: '))
        month_invoice = int(input('Type in the month of the invoice: '))
        if month_invoice>12 or month_invoice<1:
            input('The month you have typed in is an invalid entry. Press enter to try again.')
            os.system('cls')
            new_invoice()
        year_invoice = int(input('Type in the year of the invoice: '))
        mycursor = mydb.cursor() # create an instance of the "cursor" class which is used to execute SQL statements in Python
        sql = "INSERT INTO invoices (id, status, value, day, month, year) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (invoice_number, status_invoice, value_invoice, day_invoice, month_invoice, year_invoice)
        mycursor.execute(sql, val)
        mydb.commit()
        print('Record added to database')
        input('Press enter to continue.')
        mycursor.close() # close cursor object
        os.system('cls')
        main()
    except Error as e:
       print("Error", e)
       input("Press try again")
       os.system('cls')
       new_invoice()

# Check for invoices that have not been paid and view other details such as their values and the number of days that the money has not been paid.
def check_invoice():
    print("Retrieves invoices in range. For one invoice, type highest invoice number = lowest invoice number")
    print("Result displayed as (invoice number, status , value, day, month, year)")
    lowest_invoice = int(input("Lowest invoice number: "))
    highest_invoice = int(input("Highest invoice number: "))
    mycursor = mydb.cursor()
    current_invoice = lowest_invoice
    if lowest_invoice <= highest_invoice:
        while(current_invoice!=highest_invoice+1):
            sql = "SELECT * FROM invoices WHERE id = %s" # %s escapes query values preventing SQL injection
            id = (current_invoice,)
            mycursor.execute(sql, id)
            myresult = mycursor.fetchone()
            if myresult == None:
                print("Invoice", current_invoice,"not found.")
            else:
                print(myresult)
            current_invoice += 1
    else:
        input("You typed the numbers in the wrong order, press enter to try again.")
        os.system('cls')
        check_invoice()
    input("Press enter to continue.")
    mycursor.close() # close cursor object
    os.system('cls')
    main()

def new_table():
    try:
        mycursor = mydb.cursor()
        mycursor.execute("CREATE TABLE invoices (id INT PRIMARY KEY, status VARCHAR(255), value VARCHAR(255), day VARCHAR(255), month VARCHAR(255), year VARCHAR(255))")
        print("New invoice table created")
        input("Press enter to go back to the main menu")
        mycursor.close() # close cursor object
        os.system('cls')
        main()
    except Error as e:
        print("Error", e)
        input("Press enter to go back to the main menu")
        mycursor.close() # close cursor object
        os.system('cls')
        main()

def edit_invoice():
    mycursor = mydb.cursor()
    invoice_number = input("Type which invoice you want to change: ")
    sql = "SELECT * FROM invoices WHERE id = %s" # %s escapes query values preventing SQL injection
    id = (invoice_number,)
    mycursor.execute(sql, id)
    myresult = mycursor.fetchone()
    print("Current invoice properties", myresult)
    if myresult != None: # invoice data present
        # status , value, year, month, day
        new_status = str(input("Type new status: "))
        sql = "UPDATE invoices SET status=%s WHERE id = %s"
        val = (new_status, invoice_number)
        mycursor.execute(sql, val)
        mydb.commit()
        new_value = str(input("Type new value: "))
        sql = "UPDATE invoices SET value=%s WHERE id = %s"
        val = (new_value, invoice_number)
        mycursor.execute(sql, val)
        mydb.commit()
        new_day = str(input("Type new day: "))
        sql = "UPDATE invoices SET day=%s WHERE id = %s"
        val = (new_day, invoice_number)
        mycursor.execute(sql, val)
        mydb.commit()
        new_month = str(input("Type new month: "))
        sql = "UPDATE invoices SET month=%s WHERE id = %s"
        val = (new_month, invoice_number)
        mycursor.execute(sql, val)
        mydb.commit()
        new_year = str(input("Type new year: "))
        sql = "UPDATE invoices SET year=%s WHERE id = %s"
        val = (new_year, invoice_number)
        mycursor.execute(sql, val)
        mydb.commit()
        input("Changes saved. Press enter to continue.")
    else:
        input("Invoice does not exist. Press enter to continue.")
    mycursor.close() # close cursor object
    os.system('cls')
    main()

def delete_invoice():
    mycursor = mydb.cursor()
    invoice_number = int(input("Type the invoice number you want to delete: "))
    confirm = input("Are you sure you want to delete the invoice (y/n)? ")
    if confirm == "y":
        sql = "DELETE from invoices WHERE id = %s"
        id = (invoice_number,)
        mycursor.execute(sql, id)
        mydb.commit()
        print("Invoice deleted.")
    else:
        print("Invoice not deleted.")
    input("Press enter to continue.")
    mycursor.close() # close cursor object
    os.system('cls')
    main()



# See help
def help_invoice():
    print('Help for Invoice program (updated 16/08/2019)')
    print("Major Improvement: Invoice program now makes use of MySQL which allows password \n authentication to access databse")
    print("Minor Improvements (1): Errors at login are clearer, password is hidden when typing, invoices in range can be displayed")
    print("Minor Improvements (2): Invoices can be deleted")
    print("Create a new invoice - Day, month and year must be input as a number")
    print('Create a new table of invoices - Use this option when first starting the program \n or if the invoice table is accidentally deleted.')
    print('Delete invoice - Can appear to delete non-existent invoices')
    print('The invoice database must exist when starting the program.')
    input('Press enter to continue.')
    os.system('cls')
    main()


import ctypes
ctypes.windll.kernel32.SetConsoleTitleA(b" Invoice program")
import os
import datetime # used to determine number of days for a given month
import mysql.connector # for database
from mysql.connector import Error # from https://pynative.com/python-mysql-database-connection/
import getpass # to hide password when typing
while success == 0:
    username = input("Enter Database username: ")
    password = getpass.getpass("Enter Database password: ")
    try:
        mydb = mysql.connector.connect(
          host = "localhost",
          port = "3306",
          user = username,
          passwd = password,
          database = "invoices"
        )
        input("Access Granted! Press enter to continue.")
        success = 1
        os.system('cls')
        # go to main menu
        main()
    except Error as e: # from https://pynative.com/python-mysql-database-connection/
        if "2003" in str(e): # str(e): convert e to string, this branch used for connection error
            print("Error", e)
            start_service = input("Type y to open Services and try to start/restart the MySQL80 service to fix the problem: ")
            if start_service == "y":
                os.system("services.msc")
        else: # more likely to be a password error in this case
            print("Error", e)
        input("Press enter to try again.")
        os.system('cls')
