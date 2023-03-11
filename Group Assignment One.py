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
from bs4 import BeautifulSoup

def welcomeMessage():
    print("Welcome to YUL Montréal Airport")
    return

def services():
    print("1 - Flight Information")
    print("2 - Special Assistance")
    print("3 - Facilities")
    print("4 - Hotels Nearby")
    print("5 - Transportation")
    return

def scenarios():
    #has to take user input and then call the certain scenario asked for
    finished = False
    while not finished:
        try:
            userInput = int(input("Please give your answer (1, 2, 3, 4, 5): "))
            if userInput==1:
                scenarioOne()
                finished=True
            elif userInput==2:
                scenarioTwo()
                finished=True
            elif userInput==3:
                scenarioThree()
                finished=True
            elif userInput==4:
                scenarioFour()
                finished=True
            elif userInput==5:
                scenarioFive()
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
    #Executes the current question
    finished=False
    print("Which service would you like to ask about?")
    print("1 - Finding the current security times for the airport.")
    print("2 - Information how long in advance to arrive at the airport.")
    print("3 - Information regarding assistance.")
    #A while loop to not exit until found question or quit
    while not finished:
        #A try catch to avoid errors to user and forces repeat
        try:
            #Executes the current question
            userInput = int(input("Please give your answer (1,2,3): "))
            if userInput==1:
                securityTime()
                finished=True
            elif userInput==2:
                checkIn()
                finished=True
            elif userInput==3:
                assitance()
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
 
def securityTime():
    #Using the CATSA to find the current security times for the airport
    url ='https://www.catsa-acsta.gc.ca/en/airport/montreal-trudeau-international-airport'
    # Getting page HTML through request
    page = requests.get(url)
    # Parsing content using beautifulsoup
    soup = BeautifulSoup(page.content, 'html.parser')
    # Looking for the class with the info under td, this gives a list of two
    title = soup.findAll('td', attrs = {'class':'views-field views-field-php'})
    
    finished=False
    print("Where are you heading to?")
    print("1 - United States?")
    print("2 - Domestic?")
    print("3 - International?")
    while not finished:
        try:
            userInput = int(input("Please give your answer (1,2,3): "))
            if userInput==1:
                print('The the security time for travelers to the United States is')
                print(title[0].string)
                finished=True
            elif userInput==2:
                print('The the security time for domestic travelers is')
                print(title[1].string)
                finished=True
            elif userInput==3:
                print('The the security time for International travelers is')
                print(title[1].string)
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
        

def checkIn():
    print('''      CATSA encourages all passengers to arrive at their departing airport
      well in advance of their flight. Many airlines advise passengers to arrive
      two hours in advance for domestic flights and three hours in advance for US
      and international flights.''')
      
def assitance():
    finished=False
    print("Which area do you need assistance in?")
    print("1 - Travelling with childern?")
    print("2 - Travelling with a pet?")
    print("3 - Entering as a foreign student?")
    while not finished:
        try:
            userInput = int(input("Please give your answer (1,2,3): "))
            if userInput==1:
                travellingWithChild()
                finished=True
            elif userInput==2:
                travellingWithPet()
                finished=True
            elif userInput==3:
                travellingForeignStudent()
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

def knowMore(subject):
    #Creating a generic function to ask if more info is required
    print('Do you want to know more about ' + subject + '? (yes/no)')
    ifContinue = input().casefold()
    if ifContinue == 'yes':
        return False
    else:
        return True

def travellingWithChild():
    finished=False
    subject='travelling with children'
    print('Aéroports de Montréal is pleased to offer passengers travelling with young children'\
          'and infants arrangements and services designed to ensure that their airport experience'\
          'is as pleasant as possible. We also invite you to inquire with your airline as to available'\
          'onboard services.')
    while not finished:
        print("Which do you want to know more about?")
        print("1 - Priority queues?")
        print("2 - Play areas?")
        print("3 - Nursing rooms?")
        print("4 - Transportation assistance?")
        try:
            userInput = int(input("Please give your answer (1,2,3,4): "))
            print('\n')
            if userInput==1:
                print("1 - Priority queues")
                print('Passengers travelling with an infant or young child are given priority at security'\
                      'screening checkpoints “A” and “C” \n')
                finished=knowMore(subject)
            elif userInput==2:
                print("2 - Play areas")
                print('Most of the boarding lounges at Montréal–Trudeau are equipped with small play areas'\
                      ' \n')
                finished=knowMore(subject)
            elif userInput==3:
                print("3 - Nursing rooms")
                print('Most restrooms in the terminal have adjacent nursing rooms, equipped with a sink,'\
                      ' chair, changing table and, in many cases, a microwave oven. \n')
                finished=knowMore(subject)
            elif userInput==4:
                print("4 - Transportation assistance")
                print('In the international and transborder jetties, electric cart service is available to'\
                      ' passengers requiring it, from the security checkpoint to the boarding gate'\
                          ' (departures level) and from the arrival gate to the Canada customs hall'\
                              ' (arrivals level). \n')
                finished=knowMore(subject)
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
    
def travellingWithPet():
    finished=False
    subject='travelling with pets'
    print('If you are travelling with your pet, please ask your airline before you leave about the'\
          ' available options, the type of cage to use, how to prepare your pet, restrictions and'\
              ' applicable fees, etc. Airlines may also require your animal to be in its cage prior'\
                  ' to your arrival at the check-in counter.')
    while not finished:
        print("Which do you want to know more about?")
        print("1 - Rules in the terminal?")
        print("2 - Relief areas?")
        print("3 - On return?")
        try:
            userInput = int(input("Please give your answer (1,2,3): "))
            print('\n')
            if userInput==1:
                print("1 - Rules in the terminal")
                print('Pets are allowed in the terminal as long as they are in a cage or on a leash. \n')
                finished=knowMore(subject)
            elif userInput==2:
                print("2 - Relief areas")
                print('There are four (4) pet relief areas across the terminal at YUL:\n')
                print('Public area: in the Multi-Level parking lot in front of the terminal building, '\
                      'across gate 25 on the Arrivals level.\n')
                print('Domestic area: in front of boarding gate 47.\n')
                print('International area: in front of the restrooms near boarding gate 62.\n')
                print('Transborder area: in front of the restrooms near boarding gate 73.\n')
                finished=knowMore(subject)
            elif userInput==3:
                print("3 - On return")
                print('On your return, if your pet has travelled as cargo, you must pick it up from your'\
                      ' airline’s cargo services area. \n')
                finished=knowMore(subject)
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

def travellingForeignStudent():
    finished=False
    subject='travelling as a foreign student'
    while not finished:
        print("Which do you want to know more about?")
        print("1 - Tips related to COVID-19?")
        print("2 - Tip related to your studies?")
        print("3 - On Arrival?")
        try:
            userInput = int(input("Please give your answer (1,2,3): "))
            print('\n')
            if userInput==1:
                print("1 - Tips related to COVID-19")
                print("Visit the Public Health Agency of Canada's website to learn about the Government'\
                      'of Canada’s requirements. \n")
                print("Within 72 hours of your arrival to Canada, be sure to submit your travel information"\
                      " through the ArriveCAN mobile application. You will need to provide information about"\
                          " your trip, your quarantine plan and complete a COVID-19 symptom self-assessment test. \n")
                finished=knowMore(subject)
            elif userInput==3:
                print("3 - On your arrival")
                print('Make sure you have your travel and university documents: valid passport, electronic'\
                      ' travel authorization, visa, registration confirmation, etc. These documents should be'\
                          ' easily accessible - it is important not to pack them in your checked baggage! \n')
                print('Simplify your arrival in Canada by filling out your customs and immigration declaration'\
                      ' for the Canada Border Services Agency (CBSA) 72 hours prior to arrival in Canada, using '\
                          'the ArriveCAN application.\n')
                print('When you are speaking with a Canada Border Services Agency officer, remove your hat and '\
                      'sunglasses.\n')
                print('To avoid the possibility of penalties, make sure you have the necessary information before '\
                      'attempting to bring food products into Canada.\n')
                print('For restrictions on alcohol, tobacco and the amounts of money you can bring with you, visit '\
                      'the Government of Canada’s website.\n')
                finished=knowMore(subject)
            elif userInput==2:
                print("2 - Tip related to your studies")
                print('Visit the Government of Canada’s website to obtain all the information you need for your studies. \n')
                finished=knowMore(subject)
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
#-----------------------------------------------------------------------------------------------------------------------------------
def scenarioThree():
    return
#-----------------------------------------------------------------------------------------------------------------------------------
def scenarioFour():
    return
#-----------------------------------------------------------------------------------------------------------------------------------
def scenarioFive():
    return
#-----------------------------------------------------------------------------------------------------------------------------------

def endMessage():
    print("Thank you for visiting the website of YUL Montréal Airport")
    return

def checkRating():
    #Take user input of the rating of the service
    finished = False
    print("Please rate your service experience out of 10.")
    while not finished:
        try:
            userInput = int(input("Please give your answer (1-10): "))
            if 1 <= userInput <= 10:
                print("Thank you for rating our service!")
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

#MAIN
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

    
