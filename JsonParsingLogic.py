import json
from datetime import datetime

startDate = "01/08/2024"
endDAte = "02/08/2024"

startSplit = startDate.split("/")
endsplit = endDAte.split("/")


startDay = str(startSplit[0])
startMonth = str(startSplit[1])
#print(startMonth)
startYear = str(startSplit[2])

endDay = str(endsplit[0])
endMonth = str(endsplit[1])
endYear = str(endsplit[2])


with open("C:/Users/User/Desktop/Python projects/ExpenseTracker/output.json") as file:
    data = json.load(file)

expenseList = []



start_date = datetime.strptime(startDate, '%d/%m/%Y')
end_date = datetime.strptime(endDAte, '%d/%m/%Y')

for year, months in data.items():
    for month, days in months.items():
        for day, details in days.items():
            datestr = f'{year}-{month}-{day}'
            currentDate = datetime.strptime(datestr,'%Y-%m-%d')
            
            if start_date <= currentDate <= end_date:
                    expenseList.append({
                        "DATE": currentDate.strftime('%d/%m/%Y'),
                        "EXPENSES": details.get("EXPENSES", [])
                    })
print(expenseList)


file.close()