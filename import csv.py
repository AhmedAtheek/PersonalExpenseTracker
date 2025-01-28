import csv
import json
from datetime import datetime

# Input and output file paths
input_file = "C:/Users/User/Desktop/Python projects/ExpenseTracker/DATA.csv"
output_file = "C:/Users/User/Desktop/Python projects/ExpenseTracker/output.json"

# Initialize the dictionary
expenses_data = {}

# Read the CSV file
with open(input_file, mode='r') as file:
    csv_reader = csv.DictReader(file)
    
    for row in csv_reader:
        # Extract and parse the date
        date = row['DATE']
        try:
            # Parse the date into a standard format (YYYY-MM-DD)
            parsed_date = datetime.strptime(date, '%m/%d/%Y')  # Adjust for MM/DD/YYYY format
            year = str(parsed_date.year)
            month = str(parsed_date.month).zfill(2)
            day = str(parsed_date.day).zfill(2)
        except ValueError as e:
            print(f"Skipping invalid date entry: {date} -> {e}")
            continue
        
        # Extract other fields
        expense_name = row['EXPENSES']
        amount = float(row['AMOUNT'])
        expense_type = row['TYPE']

        # Build the nested structure
        if year not in expenses_data:
            expenses_data[year] = {}
        if month not in expenses_data[year]:
            expenses_data[year][month] = {}
        if day not in expenses_data[year][month]:
            expenses_data[year][month][day] = {"EXPENSES": []}
        
        # Append the expense
        expenses_data[year][month][day]["EXPENSES"].append({
            "NAME": expense_name,
            "AMOUNT": amount,
            "TYPE": expense_type
        })

# Write the data to a JSON file
with open(output_file, mode='w') as file:
    json.dump(expenses_data, file, indent=4)

print(f"JSON file created successfully at {output_file}")
