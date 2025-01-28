import sqlite3
from datetime import datetime
import csv
import os
conn = sqlite3.connect("expenses.db")

c = conn.cursor()

# c.execute("""CREATE TABLE EXPENSES (
#             date text,
#             expenseName text,
#             type text,
#             amount real,
#             currency text
#             )""")

# c.execute("INSERT INTO EXPENSES VALUES ('1/18/2025', 'food', 'FOOD', 50, 'MYR')")

# c.execute("SELECT * FROM EXPENSES WHERE date = '1/18/2025'")

# c.execute("DELETE from expenses WHERE DATE = '01/20/2025'")
# c.execute("UPDATE expenses SET DATE = '11/28/2024' WHERE DATE = '28-Nov'")
    # print("Added 'currency' column to the table.")

# Fetch all rows with the DATE column
# c.execute("SELECT rowid, DATE FROM expenses")
c.execute("""
UPDATE expenses
SET TYPE = 'UTILITIES'
WHERE TYPE = 'UTILITY';
""")
# rows = c.fetchall()

# for row in rows:
#     rowid = row[0]  # Unique identifier for the row
#     old_date = row[1]  # Original date string

#     try:
#         # Split the date into day, month, and year
#         parts = old_date.split("/")

#         # Add leading zeros to single-digit day/month values
#         if len(parts) == 3:
#             day = parts[0].zfill(2)  # Add leading zero to day if needed
#             month = parts[1].zfill(2)  # Add leading zero to month if needed
#             year = parts[2]
#             new_date = f"{day}/{month}/{year}"  # Reformat to DD/MM/YYYY
#         else:
#             raise ValueError(f"Invalid date format: {old_date}")
    
#     except ValueError:
#         print(f"Skipping invalid date: {old_date}")
#         continue

#     # Update the row with the new formatted date
#     c.execute("UPDATE expenses SET DATE = ? WHERE rowid = ?", (new_date, rowid))

#getMonthlyCatergories(2024,"Aug")

conn.commit()

conn.close()

        #To BE HANDLED

        # #just overwrites csv with the year  q
        # data = {}
        # csvPath = "MonthlyTotals.csv" 
            
        # headers = ["Month"]
        
        # if year not in headers:
        #     headers.append(year)
        
        # with open(csvPath ,"w", newline="") as file:
        #     writer = csv.writer(file)
        #     writer.writerow(headers)
        #     for monthIndex, Amount in monthlyTotal.items():
        #         writer.writerow([monthIndex,Amount])
                