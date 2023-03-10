# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 13:40:34 2023

@author: Eoghán
"""
import pandas as pd
from datetime import datetime
import requests
import math
from IPython.display import display

def welcomeMessage():
    print("Welcome to ______")
    return

def services():
    #prints list of services
    return

def scenarios():
    #has to take user input and then call the certain scenario asked for
    return

#Eoghán
#-----------------------------------------------------------------------------------------------------------------------------------
#Using the flightlabs API to get a list of all flights out of YUL for the current day
url = 'https://app.goflightlabs.com/advanced-flights-schedules?access_key=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiOTE4Y2JhZDk5ZTQwYmI3OGZhMjU3NzUxYTgyODVlMjdhMzdkMDM2MDA2ODI3N2FjMGI3MjI5MDFkMzdiZGJjMDJmOTBlM2UwZjcxZTExOTIiLCJpYXQiOjE2NzgzOTI3ODIsIm5iZiI6MTY3ODM5Mjc4MiwiZXhwIjoxNzEwMDE1MTgyLCJzdWIiOiIyMDQxMCIsInNjb3BlcyI6W119.oVWxj_THXa_8jGquTX_ymPH60OTGXf55SUFUbI5iTyZ8ZRsBLh5zDgtnEUjrhKY-FcTW2lgq2XL82TzleEuvEA&iataCode=YUL&type=departure'
r = requests.get(url, allow_redirects=True)
search = r.json()
airline=[]
gate=[]
scheduledTime=[]
delay=[]
icaoNumber=[]
iataCode=[]
y = len(search["data"])
for index in range(0,y):
    airline.append(search["data"][index]['airline']['name'])
    gate.append(search['data'][index]['departure']['gate']) 
    time = search["data"][index]['departure']['scheduledTime']
    dkmv = time.split('T')
    justTime = dkmv[1].split(':')
    actualTime = int(str(justTime[0]) + str(justTime[1]))
    scheduledTime.append(actualTime)
    delay.append(search["data"][index]['departure']['delay'])
    icaoNumber.append(search["data"][index]['flight']['icaoNumber'].capitalize())
    iataCode.append(search["data"][index]['arrival']['iataCode'])
    
def printIndexLines(indexes):
    #This function will print the details of the flights at a given index number
    rangeOfAirline = []
    rangeOfGate = []
    rangeOfScheduledTime = []
    rangeOfDelay = []
    rangeOfIcaoNumber = []
    rangeOfIataCode = []
    for i in indexes:
        if search["data"][i]['airline']['name']=='empty':
            #Getting rid of missing flight information
            continue
        rangeOfAirline.append(search["data"][i]['airline']['name'])
        rangeOfGate.append(search['data'][i]['departure']['gate'])
        rangeOfScheduledTime.append(changingTimeFormat(search["data"][i]['departure']['scheduledTime']))
        rangeOfDelay.append(search["data"][i]['departure']['delay'])
        rangeOfIcaoNumber.append(search["data"][i]['flight']['icaoNumber'].capitalize())
        rangeOfIataCode.append(search["data"][i]['arrival']['iataCode'])
    
    range_df = pd.DataFrame({'airline':rangeOfAirline,
                     'gate' : rangeOfGate,
                     'scheduledTime':rangeOfScheduledTime,
                     'delay':rangeOfDelay,
                     'icaoNumber':rangeOfIcaoNumber,
                     'iataCode':rangeOfIataCode,})
    #Showing the flights of the given indexes
    display(range_df)

def changingTimeFormat(time):
    #Formating the time into a standard
    dateAndTimeList = time.split('T')
    justTime = dateAndTimeList[1].split(':')
    actualTime_used = int(str(justTime[0]) + str(justTime[1]))
    return actualTime_used

def gettingRangeOfFlights():
    #Getting the range of flights in the current hour and then printing the table
    print("Getting the Flights for the current hour....")
    minTime = math.trunc(changingTimeFormat(datetime.now().isoformat())/100)
    withinTimePeriod = []
    y = len(search["data"])
    for index in range(0,y):
        temp_time = search["data"][index]['departure']['scheduledTime']
        temp_actualTime = changingTimeFormat(temp_time)
        currentTime = math.trunc(temp_actualTime/100)
        if currentTime==minTime:
            withinTimePeriod.append(index)
    printIndexLines(withinTimePeriod)
    
def indexlist(item, listGiven):
  #Returns the indexes of the given item in a list
  listOfIndexes=[]
  for index in range(0,len(listGiven)):
      if listGiven[index]==item:
          listOfIndexes.append(index)
  return listOfIndexes


def one_1():
    #preforms the first prompt
    finished=False
    while not finished:
        print("Please enter the flight number.")
        flight_number = str(input()).capitalize()
        if flight_number in icaoNumber:
            gatefound = gate[icaoNumber.index(flight_number)]
            print('The gate number for the flight {0} is gate {1}.'.format(flight_number, gatefound))
            finished=True
        else:
            print("Flight not found")
            print("Try again? (yes/no)")
            ifContinue = input()
            if ifContinue == 'yes':
                pass
            else:
                finished=True           
    
def one_3():
    #preforms the third prompt
    finished=False
    while not finished:
        try:
            print("Please enter the scheduled Time with 24hr time (eg. 1pm = 1300).")
            flightTime = int(input())
            if flightTime in scheduledTime:
                print("All flights at that time...")
                listOfFlights = indexlist(flightTime,scheduledTime)
                printIndexLines(listOfFlights)
                finished=True
            else:
                print("Flight not found")
                print("Try again? (yes/no)")
                ifContinue = input()
                if ifContinue == 'yes':
                    pass
                else:
                    finished=True
        except Exception:
            print("Flight not found")
            print("Try again? (yes/no)")
            ifContinue = input()
            if ifContinue == 'yes':
                pass
            else:
                finished=True
                
def scenarioOne():
    #Executes the current question
    finished=False
    print("Which service would you like to ask about.")
    print("1 - Finding the gate number for your flight.")
    print("2 - Getting all the flights for the current hour.")
    print("3 - Finding your flight number.")
    while not finished:
        try:
            userInput = int(input("Please give your answer (1,2,3): "))
            if userInput==1:
                one_1()
                finished=True
            elif userInput==2:
                gettingRangeOfFlights()
                finished=True
            elif userInput==3:
                one_3()
                finished=True
            else:
                raise ValueError('Number not listed')
        except Exception:
            print("Error")
            print("Try again? (yes/no)")
            ifContinue = input().casefold()
            if ifContinue == 'yes':
                pass
            else:
                finished=True
    return
#-----------------------------------------------------------------------------------------------------------------------------------
def scenarioTwo():
    return
def scenarioThree():
    return
def scenarioFour():
    return
def scenarioFive():
    return

def endMessage():
    print("Thank you for visiting the website of _______")
    return

def checkRating():
    #has to take user input and store a rating of the service
    return

welcomeMessage()
finished = not True
while not finished:
    print("Which service would you like to use?")
    services()
    scenarios()
    ifOther = input("Is there any other assistance required?")
    if ifOther.casefold() == "yes":
        print("processing...")
    else:
        finished = True
checkRating()
endMessage()

    
