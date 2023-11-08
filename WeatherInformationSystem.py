from tkinter import *
import requests
from bs4 import BeautifulSoup
import os

root = Tk()
root.geometry("700x700")
root.configure(bg="powderblue")
root.title("Weather Information Display Program")

r = requests.get("https://tr.freemeteo.com/")
source = BeautifulSoup(r.content, "lxml")

cities = []
links = []
templinks = []
temperatures = []
winds = []
cityDict = dict()
temperaturesDict = dict()
windsDict = dict()
details = source.find_all("div", attrs={"class": "details"})

for x in details:
    strong = x.find_all_next("strong")
    for y in strong:
        cities.append(y.text)
        a = y.find_all_next("a")
        for z in a:
            z.find_all_next("href")
            templinks.append(z)

for i in range(0, 64):
    links.append(templinks.__getitem__(i))

for i in range(0, 64):
    x = cities.__getitem__(i)
    y = links.__getitem__(i)
    cityDict[x] = y

cities.__delitem__(64)


def weatherInfo(city):
    try:
        tmpLink = cityDict.get(city)
        tmpLink = str(tmpLink)
        x = tmpLink.split('"')
        actualLink = "https://tr.freemeteo.com/" + x[1]

        r2 = requests.get(actualLink)
        source2 = BeautifulSoup(r2.content, "lxml")

        weatherNow = source2.find_all("div", attrs={"class": "today clearfix"})
        for x in weatherNow:
            temp = x.find_all_next("span", attrs={"class": "temp"})
            wind = x.find_all_next("span", attrs={"class": "wind"})
            for y in temp:
                temperatures.append(y.text)
            for z in wind:
                windInfo = z.text
                winds.append(windInfo)

        temperaturesDict["Morning"] = temperatures.__getitem__(0)
        temperaturesDict["Afternoon"] = temperatures.__getitem__(1)
        temperaturesDict["Evening"] = temperatures.__getitem__(2)
        temperaturesDict["Night"] = temperatures.__getitem__(3)

        windsDict["Morning"] = winds.__getitem__(0)
        windsDict["Afternoon"] = winds.__getitem__(1)
        windsDict["Evening"] = winds.__getitem__(2)
        windsDict["Night"] = winds.__getitem__(3)

        temperatures.clear()
        winds.clear()

        print(temperaturesDict)
        print(windsDict)
    except:
        textBox.insert("end", "Unable to get ")


def tempConversion():
    try:
        morningCTemp = temperaturesDict.get("Morning")
        afternoonCTemp = temperaturesDict.get("Afternoon")
        eveningCTemp = temperaturesDict.get("Evening")
        nightCTemp = temperaturesDict.get("Night")

        if (len(morningCTemp) == 4):
            morningCTemp = morningCTemp[0] + morningCTemp[1]
        else:
            morningCTemp = morningCTemp[0]
        if (len(afternoonCTemp) == 4):
            afternoonCTemp = afternoonCTemp[0] + afternoonCTemp[1]
        else:
            afternoonCTemp = afternoonCTemp[0]
        if (len(eveningCTemp) == 4):
            eveningCTemp = eveningCTemp[0] + eveningCTemp[1]
        else:
            eveningCTemp = eveningCTemp[0]
        if (len(nightCTemp) == 4):
            nightCTemp = nightCTemp[0] + nightCTemp[1]
        else:
            nightCTemp = nightCTemp[0]

        morningFTemp = str((int(morningCTemp) * 1.8) + 32) + "°F"
        afternoonFTemp = str((int(afternoonCTemp) * 1.8) + 32) + "°F"
        eveningFTemp = str((int(eveningCTemp) * 1.8) + 32) + "°F"
        nightFTemp = str((int(nightCTemp) * 1.8) + 32) + "°F"

        temperaturesDict["Morning"] = morningFTemp
        temperaturesDict["Afternoon"] = afternoonFTemp
        temperaturesDict["Evening"] = eveningFTemp
        temperaturesDict["Night"] = nightFTemp

        print(temperaturesDict)
    except:
        print("There is no weather information!")


clicked = StringVar()
clicked2 = StringVar()


def readFile(address):
    existFile = os.path.exists(address)
    if existFile:
        file = open(address)
        read = file.read().split()
        clicked.set(read[0])
        if (read[1] == "Fahrenheit"):
            clicked2.set("°F")
        else:
            clicked2.set("℃")
    else:
        clicked.set("Select a city")
        clicked2.set("℃")


readFile("Settings.txt")
def show():
    try:
        textBox.delete("1.0", END)
        weatherInfo(clicked.get())
        if (clicked2.get() == "°F"):
            tempConversion()

        textBox.insert("end", clicked.get() + " Weather Informations")
        textBox.insert("end", "\n\nTEMPERATURES")
        textBox.insert("end", "\nMorning: " + temperaturesDict.get("Morning"))
        textBox.insert("end", "\nAfternoon: " + temperaturesDict.get("Afternoon"))
        textBox.insert("end", "\nEvening: " + temperaturesDict.get("Evening"))
        textBox.insert("end", "\nNight: " + temperaturesDict.get("Night"))
        textBox.insert("end", "\n--------------------------------------------------------------------------------")
        textBox.insert("end", "\nWIND SPEEDS")
        textBox.insert("end", "\nMorning: " + windsDict.get("Morning"))
        textBox.insert("end", "\nAfternoon: " + windsDict.get("Afternoon"))
        textBox.insert("end", "\nEvening: " + windsDict.get("Evening"))
        textBox.insert("end", "\nNight: " + windsDict.get("Night"))

        unit = ""
        if (clicked2.get() == "℃"):
            unit = "Celcius"
        else:
            unit = "Fahrenheit"
        preferences = clicked.get() + " " + unit
        with open("Settings.txt", "w") as f:
            f.write(preferences)
    except:
        textBox.insert("end", "\nThe weather information cannot be displayed!")


textBox = Text()
textBox.pack()

dropDown = OptionMenu(root, clicked, *cities)
dropDown.config(width=20)
dropDown.pack()
dropDown2 = OptionMenu(root, clicked2, "℃", "°F")
dropDown2.config(width=20)
dropDown2.pack()

button = Button(root, text="Show Weather Informations", bg="red", fg="black", font="helvetica 15", command=show).pack()

root.mainloop()
