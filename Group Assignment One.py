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
    print("4 - Accomodation")
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
            print("Oh! I do not seem to understand!")
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
    # Create a dictionary of all facilities
    area1 = "Restricted zone - Canada"
    area2 = "Restricted zone - International"
    area3 = "Restricted zone - USA"
    facilities = {"PUB JOHN MOLSON": {"area": "Arrivals", "price": "$$$", "type": "Restaurant", "hours": "7.30 am to 8 pm"},
                      "TIM HORTONS": {"area": "Arrivals", "price": "$", "type": "Cafe", "hours": "4 am to 8 pm"},
                      "ILLY": {"area": "Public Area", "price": "$", "type": "Bar", "hours": "6.30 am to 2 pm"},
                      "BURGER KING": {"area": "Public Area", "price": "$", "type": "Restaurant", "hours": "6 am to 9 pm"},
                      "CAMDEN FOOD CO.": {"area": area1, "price": "$$", "type": "Restaurant", "hours": "5 am to 8 pm"},
                      "JAVA U CAFE": {"area": area1, "price": "$", "type": "Cafe", "hours": "4.30 am to 7.30 pm"},
                      "U RESTO BAR": {"area": area2, "price": "$$", "type": "Bar", "hours": "4 am to 11 pm"},
                      "STARBUCKS": {"area": area2, "price": "$$", "type": "Cafe", "hours": "4 am to 8 pm"},
                      "HOUSTON AVENUE GRILL": {"area": area3, "price": "$$$", "type": "Restaurant", "hours": "4 am to 7 pm"},
                      "CAFE MONTREAL BAGELS": {"area": area3, "price": "$", "type": "Cafe", "hours": "4 am to 8 pm"},
                      "FLEURISTE":{"area": "Arrivals", "price": "$$", "type": "Florist", "hours": "12 pm to 10 pm"},
                      "1 MINUTE":{"area": "Arrivals", "price": "$", "type": "Snacks and reading", "hours": "12:15 pm to 8:15pm"},
                      "REALY": {"area": "Public area", "price": "$", "type": "Snacks and reading", "hours": "1 pm to 8:30 pm"},
                      "TRACKER": {"area": "Public area", "price": "$", "type": "Clothing and accessories", "hours": "5 am to 9 pm"},
                      "ISTORE": {"area": area1, "price": "$$$", "type": "Technology", "hours": "11:30 am to 7:15 pm"},
                      "HATLEY": {"area": area1, "price": "$$$", "type": "Clothing and accessories", "hours": "Not available"},
                      "HORS TAXES": {"area": area2, "price": "$$", "type": "Duty Free", "hours": "4 am to 11 pm"},
                      "THE SOURCE": {"area": area2, "price": "$$$", "type": "Technology", "hours": "Not available"},
                      "MAISON DE LA PRESSE":{"area": area3, "price": "$$", "type": "Snacks and reading", "hours": "5:15 am to 7:15 pm"},
                      "MC ELECTRONIQUE":{"area": area3, "price": "$$$", "type": "Technology", "hours": "5 am to 6:30 pm"}
                    }
    services = {"Wi-Fi" : "Aéroports de Montréal is pleased to offer Montréal–Trudeau users free high-speed wireless internet access everywhere in the terminal.To log on to the ADM network, YUL Wi-Fi, simply open your browser and agree to the terms and conditions of use when prompted, for up to 60 minutes of free browsing.For more time, simply start a new session.",
                "Planespotting" :"Jacques-de-Lesseps Park, inaugurated in 2012, provides aviation enthusiasts with one of the best possible vantage points for observing the runways at Montréal–Trudeau. The park is located on ADM-owned land facing runways 24-L and 06-R, at the intersection of Halpern Avenue and Jenkins street.",
                "Prayer Area" : "A multi-faith area for prayer and reflection is available to airport users. It is located in the transborder (U.S.) departures area, near the Java U restaurant.",
                "Smoking Areas": "In accordance with regulations currently in effect, the Montréal–Trudeau terminal is a non-smoking environment. Smoking, including e-cigarettes, is strictly prohibited throughout the terminal building and on the apron. There are areas in front of the terminal where smoking cigarettes and e-cigarettes is permitted. Cannabis consumption is not permitted anywhere on the airport site.",
                "Nursing Rooms" : "Most restrooms in the terminal have adjacent nursing rooms, equipped with a sink, chair, changing table and, in many cases, a microwave oven."
               }

    # Create list of restaurants, cafes and bars and shops
    option_1 = ["Restaurant", "Restaurants","Restaurant area", "Restaurants area"]
    option_2 = ["Cafe","Cafes","Café"]
    option_3 = ["Bars","Bar"]
    option_shop = ["Shopping", "Shopping area", "Shops", "Shoppingarea"]
    option_services = ["Other Services", "Other","Services", "Otherservices"]
    option_map = ["Explore the map","Explore","Map"]
    restaurant_list = []
    cafe_list = []
    bar_list = []
    shops_list = []
    for facility in facilities:
        if facilities[facility]["type"] == "Restaurant":
            restaurant_list.append(facility)
        elif facilities[facility]["type"] == "Cafe":
            cafe_list.append(facility)
        elif facilities[facility]["type"] == "Bar" :
            bar_list.append(facility)
        else:
            shops_list.append(facility)

    # Choosing the area - function
    def chosen_area():
        Finished = False
        while not Finished:
            area = input("\nChoose an area of YUL Airport between 'Arrivals' and 'Departures'(Including all restricted areas):\n")
            area == area.capitalize()
            if area == "Arrivals" or area == "Arrival":
                Finished = True
            elif area == "Departures":
                finished = False
                while not finished:
                    area = input("Choose the correct departure area number:\n1: 'Restricted area - Canada',\n2: 'Restricted area - International',\n3: 'Restricted area - USA'\n")
                    if area == "1":
                        finished = True
                    elif area == "2":
                        finished = True
                    elif area == "3":
                        finished = True
                Finished = True
        return area

    # Cheaper option - function
    def cheap_option():
        cheaper_option = input("\nWould you like to find cheaper option?")
        cheaper_option = cheaper_option.capitalize()
        if "Yes" in cheaper_option:
            cheap_list = []
            print("The following cheaper options have been found:")

            # if chosen restaurant
            if input_2 in option_1:
                for i in restaurant_list:
                    if facilities[i]["price"] == "$":
                        cheap_list.append(i)
                if len(cheap_list) != 0:
                    for i in cheap_list:
                        print("-",i,"in the area:", facilities[i]["area"]+".")
                else:
                    print("Oh! Unfortunately no other cheaper option is available")

            # if chosen a cafe
            if input_2 in option_2:
                for i in cafe_list:
                    if facilities[i]["price"] == "$":
                        cheap_list.append(i)
                if len(cheap_list) != 0:
                    for i in cheap_list:
                        print("-",i,"in the area:", facilities[i]["area"]+".")
                else:
                    print("Oh! Unfortunately no other cheaper option is available")

            # if chosen a bar
            if input_2 in option_3:
                for i in bar_list:
                    if facilities[i]["price"] == "$":
                        cheap_list.append(i)
                if len(cheap_list) != 0:
                    for i in cheap_list:
                        print("-",i,"in the area:", facilities[i]["area"]+".")
                else:
                    print("Oh! Unfortunately no other cheaper option is available")

        elif "No" in cheaper_option:
            print("Perfect!")

    # Other option in the same area - function
    def other_in_area():
        if input_1 in option_1:
            other_option = input("\nWould you like to find another option in this area?")
            other_option = other_option.capitalize()
        else:
            other_option = "Yes"

        if "Yes" in other_option:
            other_list = []
            print("The following options have been found in the same area", area + ":")
            # if chosen arrivals
            if area == "Arrivals" or area == "Arrival":
                for i in facilities:
                    if facilities[i]["area"] == "Arrivals":
                        other_list.append(i)
                for i in other_list:
                    print("-",i+",", facilities[i]["type"])

            # if chosen Public area
            if area == "Public area":
                for i in facilities:
                    if facilities[i]["area"] == "Public Area":
                        other_list.append(i)
                for i in other_list:
                    print("-", i+",", facilities[i]["type"])

            # if chosen area 1
            if area == "1":
                for i in facilities:
                    if facilities[i]["area"] == area1:
                        other_list.append(i)
                for i in other_list:
                    print( "-",i+",", facilities[i]["type"])

            # if chosen area 2
            if area == "2":
                for i in facilities:
                    if facilities[i]["area"] == area2:
                        other_list.append(i)
                for i in other_list:
                    print( "-",i+",", facilities[i]["type"])

            # if chosen area 3
            if area == "3":
                for i in facilities:
                    if facilities[i]["area"] == area3:
                        other_list.append(i)
                for i in other_list:
                    print("-",i+",", facilities[i]["type"])

        elif "No" in other_option:
            print("Perfect!")

    # Providing opening hours - function
    def ask_hours():
        finished = False
        while not finished:
            hours_question = input("\nWould you like to know the opening hours of one of our facilities?\n")
            hours_question = hours_question.capitalize()
            if hours_question == "Yes":
                name = input("Which facility would you like to know the opening hours of?\n")
                name = name.upper()
                print("The facility", name, "has the following opening hours:", facilities[name]["hours"],"\n")
                finished = True
            if hours_question == "No" or hours_question == "no":
                print("Perfect!")
                finished = True

    # Initial choice between restaurant area, shopping area, other services and map
    done = False
    while not done:
        print("Hello, welcome to our YUL Airport facilities section. What are you looking for?")
        print("- Restaurant area, \n- Shopping area, \n- Other services, \n- Explore the map.")
        input_1 = input()
        input_1 = input_1.capitalize()

        # Restaurant area choice
        if input_1 in option_1:
            input_2 = input("\nAre you looking for Restaurants, Cafes or Bars?")
            input_2 = input_2.capitalize()

            # Restaurant choice
            if input_2 in option_1:
                print("\nThe Restaurants available in YUL Airport are:")
                for i in restaurant_list:
                    print(i)

                # Choosing the area for the restaurant
                area = chosen_area()

                # Presenting the restaurants in the area
                rest_area_list = []
                if area == "Arrivals" or area == "Arrival":
                    for restaurant in restaurant_list:
                        if facilities[restaurant]["area"] == "Arrivals":
                            rest_area_list.append(restaurant)
                else:
                    if area == "1":
                        for restaurant in restaurant_list:
                            if facilities[restaurant]["area"] == area1:
                                rest_area_list.append(restaurant)
                    elif area == "2":
                        for restaurant in restaurant_list:
                            if facilities[restaurant]["area"] == area2:
                                rest_area_list.append(restaurant)
                    elif area == "3":
                        for restaurant in restaurant_list:
                            if facilities[restaurant]["area"] == area3:
                                rest_area_list.append(restaurant)
                if rest_area_list == []:
                    print("\nThere are no restaurants available in this are")
                else: 
                    print("\nThe restaurants available in this area are:")
                    for i in rest_area_list:
                        print("-",i)
                    for i in rest_area_list:
                        print("The opening hours are:"+facilities[i]["hours"])
                        print("The price range is:"+facilities[i]["price"])
                    # find a cheaper option
                    cheap_option()

                # find other option in the area
                other_in_area()
                # Ask for opening hours
                ask_hours()

                #Offering to go back to the initial menu
                input_back = input("\nDo you want to go back to YUL Airport facilities menu?")
                if input_back == "No" or input_back == "no":
                    print("Enjoy your visit to YUL Airport!")
                    done = True
                print("\n")

            # Cafe choice
            elif input_2 in option_2:
                print("\nThe Cafes available in YUL Airport are:")
                for i in cafe_list:
                    print(i)

                # Choosing the area for the cafe
                area = chosen_area()

                # Presenting the cafes in the area
                cafe_area_list = []
                if area == "Arrivals" or area == "Arrival":
                    for cafe in cafe_list:
                        if facilities[cafe]["area"] == "Arrivals":
                            cafe_area_list.append(cafe)
                else:
                    if area == "1":
                        for cafe in cafe_list:
                            if facilities[cafe]["area"] == area1:
                                cafe_area_list.append(cafe)
                    elif area == "2":
                        for cafe in cafe_list:
                            if facilities[cafe]["area"] == area2:
                                cafe_area_list.append(cafe)
                    elif area == "3":
                        for cafe in cafe_list:
                            if facilities[cafe]["area"] == area3:
                                cafe_area_list.append(cafe)

                if len(cafe_area_list) == 0:
                    print("\nThere are no Cafes available in this area.\n")
                else:
                    print("\nThe cafes available in this area are:")
                    for i in cafe_area_list:
                        print("-",i)
                    for i in cafe_area_list:
                        print("The opening hours are:"+ facilities[i]["hours"])
                        print("The price range is:"+ facilities[i]["price"])
                    # find a cheaper option
                    cheap_option()

                # Find other option in the area
                other_in_area()

                # Ask for opening hours
                ask_hours()

                #Offering to go back to the initial menu
                input_back = input("\nDo you want to go back to YUL Airport facilities menu?")
                if input_back == "No" or input_back == "no":
                    print("Enjoy your visit to YUL Airport!")
                    done = True
                print("\n")

            # Bar choice
            elif input_2 in option_3:
                print("\nThe Bars available in YUL Airport are:")
                for i in bar_list:
                    print(i)

                # choosing the area for the bar
                area = chosen_area()

                # Presenting the bars in the area
                bar_area_list = []
                if area == "Arrivals" or area == "Arrival":
                    for bar in bar_list:
                        if facilities[bar]["area"] == "Arrivals":
                            bar_area_list.append(bar)
                else:
                    if area == "1":
                        for bar in bar_list:
                            if facilities[bar]["area"] == area1:
                                bar_area_list.append(bar)
                    elif area == "2":
                        for bar in bar_list:
                            if facilities[bar]["area"] == area2:
                                bar_area_list.append(bar)
                    elif area == "3":
                        for bar in bar_list:
                            if facilities[bar]["area"] == area3:
                                bar_area_list.append(bar)
                if bar_area_list == []:
                    print("\nThere are no bars available in this area")
                else: 
                    print("\nThe Bars available in this area are:")
                    for i in bar_area_list:
                        print("-",i)
                    for i in bar_area_list:
                        print("The opening hours are:"+facilities[i]["hours"])
                        print("The price range is:"+facilities[i]["price"])
                    # find a cheaper option
                    cheap_option()

                # find other options in the area
                other_in_area()

                # Ask for opening hours
                ask_hours()

                #Offering to go back to the initial menu
                input_back = input("\nDo you want to go back to YUL Airport facilities menu?")
                if input_back == "No" or input_back == "no":
                    print("Enjoy your visit to YUL Airport!")
                    done = True
                print("\n")


        # Shopping area choice
        elif input_1 in option_shop:
            finished = False
            while not finished:
                input_2 = input("What kind of shop are you looking for?\n1- Florist,\n2- Snacks and Reading,\n3- Technology,\n4- Duty Free,\n5- Clothing and accessories. \nPlease indicate the number of the choice.")
                print("\nThe following shops are available: ")
                if input_2 == "1":
                    for i in shops_list:
                        if facilities[i]["type"] == "Florist":
                            print("-", i,"in the area:",facilities[i]["area"])
                            finished = True
                elif input_2 == "2":
                   for i in shops_list:
                       if facilities[i]["type"] == "Snacks and reading":
                           print("-", i,"in the area:",facilities[i]["area"])
                           finished = True
                elif input_2 == "3":
                   for i in shops_list:
                       if facilities[i]["type"] == "Technology":
                           print("-", i,"in the area:",facilities[i]["area"])
                           finished = True
                elif input_2 == "4":
                   for i in shops_list:
                       if facilities[i]["type"] == "Duty Free":
                           print("-", i,"in the area:",facilities[i]["area"])
                           finished = True
                elif input_2 == "5":
                   for i in shops_list:
                       if facilities[i]["type"] == "Clothing and accessories":
                           print("-", i,"in the area:",facilities[i]["area"])
                           finished = True
                else:
                   print("Oh! Something must have gone wrong, make sure to indicate the number of the choice")

            option = input("\nWould you like to explore other Shops?")   
            option = option.capitalize()
            if option == "Yes":    
                # choosing the area for the shop
                area = chosen_area()
                # find other options in the area
                other_in_area()

            # Ask for opening hours
            ask_hours()

            #Offering to go back to the initial menu
            input_back = input("\nDo you want to go back to YUL Airport facilities menu?")
            if input_back == "No" or input_back == "no":
                print("Enjoy your visit to YUL Airport!")
                done = True
            print("\n")


        # Explore services
        if input_1 in option_services: 
            print("\nHere is a list of additional services offered by YUL Airport:")
            list_services = list(services.keys())
            for i in range(1,len(services)): 
                print(i,"-",list_services[i-1])
            # Providing information about the chosen service
            while True:
                try:
                    input_2 = input("Select the corresponding number for further information about YUL Airport services\n")
                    print("\n"+services[list_services[int(input_2)-1]])
                    break
                except:
                    continue

            #Offering to go back to the initial menu
            input_back = input("\nDo you want to go back to YUL Airport facilities menu?")
            if input_back == "No" or input_back == "no":
                print("Enjoy your visit to YUL Airport!")
                done = True
            print("\n")

        # Explore the map, providing a link to the airport map
        if input_1 in option_map:
            print("Here you can explore the map of YUL Airport, enjoy your stay!")
            print("Click on this link: https://www.admtl.com/sites/default/files/2023/MAP-DEPARTS-ARRIVEES.pdf?panel=filters&dcenter=45.454073,-73.748789&dczoom=16 ")

            #Offering to go back to the initial menu
            input_back = input("\nDo you want to go back to YUL Airport facilities menu?")
            if input_back == "No" or input_back == "no":
                done = True
                print("Enjoy your visit to YUL Airport!")
            print("\n")
#-----------------------------------------------------------------------------------------------------------------------------------

def scenarioFour():
    hotels = {'A': 
                  {'Name': 'OMNI MONT-ROYAL',
                   'Price': 125,
                   'Filter': 'Pet-friendly',
                   'Type':'Bed & breakfast', 
                   'Star': "3", 
                   'PopularLocation':'Montreal and vicinity'},
              'B': 
                  {'Name': 'BIRKS',
                   'Price' : 100, 
                   'Filter' : 'Spa',
                   'Type':'Bed & breakfast', 
                   'Star': "4", 
                   'PopularLocation':'Downtown Montreal'},
              'C': 
                  {'Name': 'WILLIAM GRAY',
                   'Price' : 85, 
                   'Filter' : 'Pool',
                   'Type':'Bed & breakfast', 
                   'Star': "2", 
                   'PopularLocation':'Montreal and vicinity'},
              'D': 
                  {'Name': 'ZERO 1',
                   'Price' : 156, 
                   'Filter' : 'Pool',
                   'Type':'Bed & breakfast', 
                   'Star': "4", 
                   'PopularLocation':'Old Montreal'},
              'E': 
                  {
                   'Name': 'CHROME',
                   'Price' : 210, 
                   'Filter' : 'Pet-friendly',
                   'Type':'Bed & breakfast', 
                   'Star': "5", 
                   'PopularLocation':'Montreal (YUL-Pierre Elliott Trudeau Intl.)'},
              'F': 
                  {'Name': 'LE PETIT HOTEL',
                   'Price' : 225, 
                   'Filter' : 'Pool',
                   'Type':'Bed & breakfast', 
                   'Star': "3", 
                   'PopularLocation':'Montreal and vicinity'},
              'G': 
                  {'Name': 'ROYAL',
                   'Price' : 156, 
                   'Filter' : 'Pool',
                   'Type':'Bed & breakfast', 
                   'Star': "5", 
                   'PopularLocation':'Old Montreal'},
              'H': 
                  {'Name': 'RUBY',
                   'Price' : 125, 
                   'Filter' : 'Spa',
                   'Type':'Bed & breakfast', 
                   'Star': "4", 
                   'PopularLocation':'Downtown Montreal'},
              'I': 
                  {'Name': 'QUEEN',
                   'Price' : 213, 
                   'Filter' : 'Pet-friendly',
                   'Type':'Bed & breakfast', 
                   'Star': "2", 
                   'PopularLocation':'Downtown Montreal'},
              'J': 
                  {'Name': 'FAUBOURG',
                   'Price' : 96, 
                   'Filter' : 'Pool',
                   'Type':'Bed & breakfast', 
                   'Star': "4", 
                   'PopularLocation':'Old Montreal'}}
    
    #Creating a list of possible star ratings
    rangeHotelStar = ["1", "2", "3", "4", "5"]
    #Creating a list of hotels
    hotel_list = []
    for i in hotels:
        hotel_list.append(hotels[i]["Name"])
    
    
    #Selection of hotels in the selected area
    def find_hotels_in_area(area):
        hotels_in_area = []
        for hotel in hotels:
            if hotels[hotel]["PopularLocation"] == area:
                hotels_in_area.append(hotels[hotel]["Name"])
        return hotels_in_area
                   
    def get_price():
        done = False
        while not done: 
            hotel = input("\nWhich hotel would you like to know the price of?")
            hotel = hotel.upper()
            try:
                if hotel in hotel_list:
                    for i in hotels:
                        if hotels[i]["Name"] == hotel:
                            print("\nThe price of the hotel selected is:", hotels[i]["Price"]+"CA$")
                            done = True
                        else:
                            continue
                else:
                    print("\nOh! I do not seem to understand. Please select an hotel among the following:")
                    for i in hotels:
                        print("-",hotels[i]["Name"]+","+hotels[i]["Type"]+", "+hotels[i]["Filter"])
            except:
                print("\nOopsie! I do not seem to understand. Please select an hotel among the following:")
                for i in hotels:
                    print("-",hotels[i]["Name"]+","+hotels[i]["Type"]+", "+hotels[i]["Filter"])
                    
    #Selectin of number of stars 
    def select_star():
        finished=False
        print("What star rating would you prefer?")
        print("1: 1 star")
        print("2: 2 stars")
        print("3: 3 stars")
        print("4: 4 stars")
        print("5: 5 stars")
    
        finished = False
        while not finished:
            userInput = input("\nPlease select 1, 2, 3, 4, or 5:")
            suggestion_hotels2 = []
            if userInput in rangeHotelStar:
                for i in hotels:
                    if hotels[i]["Name"] in suggestion_hotels:
                        if hotels[i]["Star"] == userInput:
                            suggestion_hotels2.append(hotels[i]["Name"])
                if len(suggestion_hotels2) != 0:
                    print("\nBased on your selected area, the following hotels are recommended:")
                    for i in suggestion_hotels2:
                        print("-",i)
                else: 
                    print("Unfortnately there is no option in this area with the desired rating!")
                    print("Here are the hotels available in the area and their corresponding rating:")
                    for i in hotels:
                        if hotels[i]["Name"] in suggestion_hotels:
                            print("-",hotels[i]["Name"] + ", rating:",hotels[i]["Star"])
                finished = True
            else:
                print("\nOh! I do not seem to understand!")
    
    #Main interaction: choice of area and suggestion of hotels
    print("\nWhich area would you like the hotel to be in?")
    print("1: Montreal and vicinity")
    print("2: Montreal (YUL-Pierre Elliott Trudeau Intl.)")
    print("3: Downtown Montreal")
    print("4: Old Montreal")
    finished = False
    while not finished:
        try:
            userInput = int(input("\nPlease select 1, 2, 3, or 4:"))
            if userInput==1: 
                suggestion_hotels = find_hotels_in_area('Montreal and vicinity') 
                finished=True
            elif userInput==2:
                suggestion_hotels = find_hotels_in_area('Montreal (YUL-Pierre Elliott Trudeau Intl.)') 
                finished=True
            elif userInput==3:
                suggestion_hotels = find_hotels_in_area('Downtown Montreal')
                finished=True
            elif userInput==4:
               suggestion_hotels = find_hotels_in_area('Old Montreal')
               finished=True
        except:
            print("Oh! I do not seem to understand. Please try again by inserting the number of your choice.")
    
    print("Based on your selected area, the following hotels are reccommended: ")
    for i in suggestion_hotels:
        print("-",i)

    finished = False
    while not finished:
        star_choice = input("Would you like to filter the reccomendations by star?")
        star_choice = star_choice.capitalize()
        if star_choice == "Yes":
            select_star()
            finished = True
        elif star_choice == "No":
            print("Perfect")
            finished = True
        else: 
            print("Oh! I do not seem to understand. Try answering with Yes or No!")
    
    finished = False
    while not finished:
        request_price = input("Would you like to know the price range of any hotel?")
        request_price = request_price.capitalize()
        if request_price == "Yes":
            get_price()
            finished = True
        elif request_price == "No":
            print("Perfect!")
            finished = True
        else: 
            print("Oh! I do not seem to understand. Try answering with Yes or No!")
    
#-----------------------------------------------------------------------------------------------------------------------------------
def scenarioFive():
    finish = False
    while not finish:
        user_ans1 = input("\nWould you like to know information about parking or transportation?")
        if user_ans1.casefold() == "parking":
            finish = True
            done = False
            while not done:
                user_ans6=input("\nWould you prefer to park indoors or outdoors?")
                if user_ans6.casefold()=="indoors":
                    print("You have chosen idoors.")
                    done = True
                    finished = False
                    while not finished:
                        user_ans8=input("\nWould you like to know the parking rates or parking options?")
                        if user_ans8.casefold()== "parking rates":
                            import pandas as pd
                            data_indoor = {'Options': ['Multilevel', 'Short term'],
                                    '20 min': ['8$', '$8'],
                                    '1 day': ['$45', '$36']}
                            df = pd.DataFrame(data_indoor)
                            print(df)
                            finished = True
                        elif user_ans8.casefold()=="parking options":
                            print("You have chosen parking options"
                                  "The parking options are the following: Multilevel or Short term parking (temporarily closed)")
                            finished = True
                        else:
                            print("\nSorry, that is not a valid choice.")
                elif user_ans6=="outdoors":
                    print("You have chosen outdoors.")
                    done = True
                    while not finished:
                        user_ans7=input("\nWould you like to know the parking rates or parking options?")
                        if user_ans7.casefold()=="parking rates" or user_ans7 == "rates":
                            print("You have chosen parking rates")
                            import pandas as pd
                            data_outdoor = {'Options': ['Valet Parc', 'Hotel Parc', 'Econo Parc', 'AeroParc'],
                                    '20 min': ['-', '$10', '-', '-'],
                                    '1 day': ['$50', '$45', '$30', '$30']}
                            df = pd.DataFrame(data_outdoor)
                            print(df)
                            finished = True
                        elif user_ans7.casefold()=="parking options":
                            print("You have chosen parking options"
                                  "The parking options are the following: valet parking, econoparc or aeroparc")
                            finished = True
                        else:
                            print("\nSorry, unfortunately that is not a valid choice.")
                else:
                    print("\nSorry, unfortunately that is not a valid choice.")
        elif user_ans1 == "transportation":
            print("You have chosen to learn the information about transportation.")
            finish = True
            finished = False
            while not finished:
                    user_ans2 = input("\nWould you like the information about buses, taxis or car rentals? ")
                    if user_ans2.casefold()=="buses" or user_ans2.casefold()=="busses":
                        finished = True
                        print("You have chosen to learn about the information on buses. ")
                        while True:
                            user_ans4=input("\nDo you want to know about the rates or the buses ?")
                            if user_ans4.casefold()=="rates":
                                print("You have chosen rates."
                                      "The rates for the 747 Express bus cost $11."
                                      "The regular service for buses #204, 209, and 460 cost $3.50.")
                                break
                            elif user_ans4.casefold()=="buses" or user_ans4.casefold() == "busses":
                                print("You have chosen buses."
                                      "There are 2 different types of buses."
                                      "First, there is the 747 Express bus which goes downtown and connects the airport to 11 stops in Montreal." 
                                      "It is in continuous service."
                                      "Second, there is the regular service from the Society of Transportation in Montreal #204, 209, and 460 that connects the airport to some places in Montreal.")
                                break
                            else:
                                print("\nSorry, unfortunately that is not a valid choice.")
                    elif user_ans2.casefold() == "taxis":
                        finished = True
                        print("You have chosen to learn about the information on taxis. To learn about the rates, please select where you plan on going.")
                        while True:
                            user_ans3=input("\nAre you go going downtown or another location?")
                            if user_ans3.casefold()=="downtown":
                                print("You have chosen downtown."
                                      "Between 5AM and 11PM, the flat rate is $48.40."
                                      "Outside of these hours, the flat rate is $55.65")
                                break
                            elif user_ans3.casefold()=="other locations":
                                print("You have chosen other locations."
                                      "Between 5AM and 11PM, the rate is $4.10/km and the minimum charge is $20.60."
                                      "Outside of these hours, $4.70/km and the minimum charge is $23.70")
                                break
                            else:
                                print("\nSorry, unfortunately that is not a valid choice.")
                            
                    elif user_ans2 == "car rentals":
                        finished = True
                        print("You have chosen to learn about car rentals.")
                        while True:
                            user_ans5=input("\nDo you want to know the location or companies of car rentals?")
                            if user_ans5.casefold()=="location":
                                print("You have chosen location."
                                      "Please follow signs for 'Ground Transportation Building.'"
                                      "We are located directly inside that facility.  It is approximately a 5-10 minute walk from baggage claim, located in a separate building from the terminal and to the left. ")
                                break
                            elif user_ans5.casefold()=="companies":
                                print("You have chosen companies. Here are the information to contact car rental companies")
                                import pandas as pd
                                car_rentals = {'Company': ['Alamo', 'Avis', 'Budget', 'Dollar', 'Enterprise', 'Hertz', 'National', 'Thrifty'],
                                'Phone': ['514 633-1222', '514 636-1902', '514 636-0052', '514 636-9530', '514 631-4545', '514 636-9530', '514 636-9030', '514 636-9530'],
                                'Toll-Free': ['1 800 462-5266', '1 800 879-2847', '1 800 268-8970', '1 800 800-4000', '1 800 736-8222', '1 800 263-0678', '1 800 227-7368', '1 800 847-4389']}
                                df = pd.DataFrame(car_rentals)
                                print(df)
                                break
                            else:
                                print("\nSorry, unfortunately that is not a valid choice.")
                    else:
                        print("\nSorry, unfortunately that is not a valid choice. Please choose between buses, taxis or car rentals.")
        else:
            print("\nSorry, unfortunately that is not a valid choice. Please choose between parking or transportation.")
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
