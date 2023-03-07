# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 13:40:34 2023

@author: eogha
"""
def welcomeMessage():
    print("Welcome to ______")
    return

def services():
    #prints list of services
    return

def scenarios():
    #has to take user input and then call the certain scenario asked for
    return

def scenarioOne():
    return
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

    