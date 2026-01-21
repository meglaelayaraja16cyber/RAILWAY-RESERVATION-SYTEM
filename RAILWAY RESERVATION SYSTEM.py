# =====================================================
# RAILWAY RESERVATION SYSTEM
# Python + MySQL
# =====================================================

import mysql.connector
import os
import platform

# -----------------------------------------------------
# GLOBAL VARIABLES
# -----------------------------------------------------
pnr = 1024

# -----------------------------------------------------
# DATABASE CONNECTION
# -----------------------------------------------------
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="SQL@123"   # Enter your MySQL password if any
)

mycursor = mydb.cursor()

# -----------------------------------------------------
# FUNCTION : CREATE DATABASE
# -----------------------------------------------------
def create_database():
    mycursor.execute("CREATE DATABASE IF NOT EXISTS Railway_System")
    mycursor.execute("USE Railway_System")
    print("\nDatabase 'Railway_System' is ready.\n")

# -----------------------------------------------------
# FUNCTION : CREATE TABLES
# -----------------------------------------------------
def create_tables():
    mycursor.execute("USE Railway_System")

    # Train Details Table
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS traindetail(
            tname VARCHAR(30),
            tnum INT PRIMARY KEY,
            ac1 INT,
            ac2 INT,
            ac3 INT,
            slp INT
        )
    """)

    # Passenger Table
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS passengers(
            pname VARCHAR(25),
            age INT,
            trainno INT,
            noofpas INT,
            cls VARCHAR(10),
            amt INT,
            status VARCHAR(15),
            pnrno INT PRIMARY KEY
        )
    """)

    print("\nTables created successfully.\n")

# -----------------------------------------------------
# FUNCTION : ADD TRAIN DETAILS
# -----------------------------------------------------
def train_detail():
    mycursor.execute("USE Railway_System")
    ch = 'y'

    while ch.lower() == 'y':
        tname = input("Enter Train Name        : ")
        tnum = int(input("Enter Train Number      : "))
        ac1 = int(input("AC First Class Seats    : "))
        ac2 = int(input("AC Second Class Seats   : "))
        ac3 = int(input("AC Third Class Seats    : "))
        slp = int(input("Sleeper Class Seats     : "))

        sql = """
            INSERT INTO traindetail
            (tname, tnum, ac1, ac2, ac3, slp)
            VALUES (%s,%s,%s,%s,%s,%s)
        """
        data = (tname, tnum, ac1, ac2, ac3, slp)

        mycursor.execute(sql, data)
        mydb.commit()

        print("\nTrain record added successfully.\n")
        ch = input("Add another train? (y/n): ")

# -----------------------------------------------------
# FUNCTION : RESERVATION
# -----------------------------------------------------
def reservation():
    global pnr
    mycursor.execute("USE Railway_System")

    pname = input("Passenger Name        : ")
    age = int(input("Age                   : "))
    trainno = int(input("Train Number          : "))
    noofpas = int(input("Number of Passengers  : "))

    print("\nChoose Class")
    print("1. AC First Class")
    print("2. AC Second Class")
    print("3. AC Third Class")
    print("4. Sleeper Class")

    ch = int(input("Enter choice: "))

    if ch == 1:
        cls = "AC1"
        amt = noofpas * 1000
    elif ch == 2:
        cls = "AC2"
        amt = noofpas * 800
    elif ch == 3:
        cls = "AC3"
        amt = noofpas * 500
    else:
        cls = "SLP"
        amt = noofpas * 350

    pnr += 1
    status = "CONFIRMED"

    sql = """
        INSERT INTO passengers
        (pname, age, trainno, noofpas, cls, amt, status, pnrno)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    data = (pname, age, trainno, noofpas, cls, amt, status, pnr)

    mycursor.execute(sql, data)
    mydb.commit()

    print("\nTicket Booked Successfully!")
    print("PNR Number :", pnr)
    print("Amount Paid:", amt)

# -----------------------------------------------------
# FUNCTION : CANCELLATION
# -----------------------------------------------------
def cancel_ticket():
    mycursor.execute("USE Railway_System")
    p = int(input("Enter PNR Number to Cancel: "))

    sql = "UPDATE passengers SET status='CANCELLED' WHERE pnrno=%s"
    mycursor.execute(sql, (p,))
    mydb.commit()

    print("\nTicket Cancelled Successfully.\n")

# -----------------------------------------------------
# FUNCTION : DISPLAY PNR STATUS
# -----------------------------------------------------
def display_pnr():
    mycursor.execute("USE Railway_System")
    p = int(input("Enter PNR Number: "))

    sql = "SELECT * FROM passengers WHERE pnrno=%s"
    mycursor.execute(sql, (p,))
    res = mycursor.fetchall()

    if res:
        print("\nPassenger Details:")
        print("(Name, Age, TrainNo, Passengers, Class, Amount, Status, PNR)")
        for row in res:
            print(row)
    else:
        print("\nPNR Not Found.\n")

# -----------------------------------------------------
# MAIN MENU
# -----------------------------------------------------
def menu():
    create_database()

    while True:
        print("\n========== RAILWAY RESERVATION SYSTEM ==========")
        print("1. Create Tables")
        print("2. Add Train Details")
        print("3. Reserve Ticket")
        print("4. Cancel Ticket")
        print("5. Display PNR Status")
        print("6. Exit")
        print("==============================================")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            create_tables()
        elif choice == 2:
            train_detail()
        elif choice == 3:
            reservation()
        elif choice == 4:
            cancel_ticket()
        elif choice == 5:
            display_pnr()
        elif choice == 6:
            print("\nThank you for using Railway Reservation System.")
            break
        else:
            print("\nInvalid choice. Try again.\n")

# -----------------------------------------------------
# PROGRAM START
# -----------------------------------------------------
menu()
