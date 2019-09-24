import mysql.connector # for database
import os
from mysql.connector import Error # from https://pynative.com/python-mysql-database-connection/
import getpass # to hide password when typing
username = input("Enter Database username: ")
password = getpass.getpass("Enter Database password: ")
try:
    mydb = mysql.connector.connect(
      host = "localhost",
      port = "3306",
      user = username,
      passwd = password,
    )
    input("Access Granted! Press enter to continue.")
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE invoices")
    success = 1
    input("invoices database created. Press enter to exit.")
except Error as e: # from https://pynative.com/python-mysql-database-connection/
    if "2003" in str(e): # str(e): convert e to string, this branch used for connection error
        print("Error", e)
        start_service = input("Type y to open Services and try to start/restart the MySQL80 service to fix the problem: ")
        if start_service == "y":
            os.system("services.msc")
    else: # more likely to be a password error in this case
        print("Error", e)
    input("Press enter to exit. Try again later.")
