import csv
import matplotlib.pyplot as plt
from datetime import datetime


print('Enter "regions" for graph of the different regions')
print('Enter "UTLAs" for graph of the top 10 most affected UTLAs')
print('Or just enter the names for specific UTLAs/Regions separated by a comma e.g. "Sheffield, Derby"')
print('Type "Quit" to exit the program')

base_on_population = "true"  # "false" or "true"
userInput = input(": ").replace(" ", "").title().split(",")

while userInput != ["Quit"]:

    regions = []
    data = {}

    with open(r"coronavirus-cases_latest.csv", "r") as csv_file:  # Converts the useful data from the CSV file into arrays
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            if line[2] == "Region" or line[2] == "Upper tier local authority":
                if line[0] in data.keys():
                    data[line[0]][0].append(line[4])
                    data[line[0]][0].append(line[3])
                else:
                    data[line[0]] = [[]]

                if line[2] == "Region" and line[0] not in regions:  # fill regions array with regions
                    regions.append(line[0])

    with open(r"populations.csv", "r") as csv_file:  # appends the population of utlas to array stored data
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            if line[0] in data:
                data[line[0]].append(line[1])

    for key, val in data.items():  # Reverse the order of data
        val[0].reverse()

    no_population_data = []
    def plot_area(location):  # Function that draws line of graph for current location
        x = []
        y = []
        for i in range(0, len(data[location][0])):  # split dates and cases to 2 arrays
            if i % 2 == 1:
                if base_on_population == "false":
                    plt.title("Daily Corona Virus Cases")
                    y.append(float(data[location][0][i]))
                elif len(data[location]) == 2:
                    plt.title("Daily Corona Virus Cases per 100,000 people")
                    num = int(data[location][1]) / 100000
                    y.append(round(int(data[location][0][i]) / num, 1))
            else:
                x.append(datetime.strptime(data[location][0][i], '%Y-%m-%d'))

        if base_on_population == "false":
            plt.plot(x, y)  # plots the line for x (dates) and y
        elif len(data[location]) == 2:
            plt.plot(x, y)  # plots the line for x (dates) and y
        else:
            no_population_data.append(location)


    if userInput == ["Regions"]:
        userInput = regions
    elif userInput == ["Utlas"]:  # shows the top 10 most affected UTLAs
        totalArr = []
        for key, val in data.items():
            location = key
            arr = val[0]
            total = 0
            for i in range(0, len(arr)):
                if i % 2 == 1:
                    if arr[i] != "":
                        total += int(arr[i])

            if key not in regions:
                if len(totalArr) < 10:
                    totalArr.append([key, total])
                else:
                    for i in range(len(totalArr)):
                        if total > totalArr[i][1] and [key, total] not in totalArr:
                            totalArr[i] = [key, total]
        userInput = []
        for i in range(len(totalArr)):
            userInput.append(totalArr[i][0])

    dates = []
    for item in userInput:  # produce array of every date going to be used
        if len(data[item]) == 2:
            for i in range(0, len(data[item][0])):
                if i % 2 == 0 and datetime.strptime(data[item][0][i], '%Y-%m-%d') not in dates:
                    dates.append(datetime.strptime(data[item][0][i], '%Y-%m-%d'))
    dates.sort()

    for item in userInput:  # plot line for each location in array+
        plot_area(item)

    tick = []
    for i in range(0, len(dates)):  # only label x axis every 5 dates
        if i % 5 == 0:
            tick.append(dates[i])

    if len(no_population_data) > 0:
        print("No population data for " + ", ".join(no_population_data))

    plt.xticks(tick)
    plt.xlabel("Date")
    plt.ylabel("Daily Cases")
    plt.gcf().autofmt_xdate()
    plt.legend(userInput)
    plt.show()



    userInput = input(": ").replace(" ", "").title().split(",")

"""
def daily_cases(area_code, specimen_date):
    daily_lab_confirmed_cases = 0
    for item in data:
        if item[1] == area_code and item[2] == specimen_date:
            daily_lab_confirmed_cases = item[3]
    return daily_lab_confirmed_cases


print(daily_cases("E12000009", "2020-05-03"))

"""
