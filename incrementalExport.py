import requests
import json
import time
from datetime import datetime

#Obtains the JSON data from Zendesk using the requests package to make an HTTP GET request
#user: Email address in the form of a String
#pwd: Password for the Zendesk Account in the form of a String
#url: URL to make the request to in the form of a String
def getResponse(user, pwd, url):
    
    #Uses the requests import to make an HTTP GET request to the specified URL with the user and pwd variables.
    response = requests.get(url, auth=(user,pwd))

    #Check for status code. If failure, terminate program.
    if response.status_code != 200:
        print('ERROR Status Code:', response.status_code, '\nThere was a problem with the request. Exiting.')
        exit()

    #Converts the Response object
    data = response.json()

    return data

#Converts the JSON Ticket object into an array representation that holds the ID, subject, description and created_at fields
#ticket: Ticket dictionary
def truncateTicket(ticket):
    arr = []

    arr.append(ticket['id'])
    arr.append(ticket['subject'])
    arr.append(ticket['description'])
    arr.append(ticket['created_at'])

    return arr

#Converts UNIX Time string into a readable format (Also compattible with the precedes() function)
#x: UNIX Timecode represented as a String
def convertTime(x):
    x = int(x)
    strRep = (datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))

    #Further converts the string into the same format used in the precedes() function
    strRep = strRep[:10] + 'T' + strRep[11:]
    strRep = strRep[:19] + 'Z' + strRep[20:]

    return strRep

#Checks to see if date1 precedes date2
#date1: The lower bounded date in String format
#date2: The upper bounded date in String format
def precedes(date1, date2):
    d1 = date1.split('-')
    d2 = date2.split('-')

    #Check the year. If date1 is in an earlier year than date2, return True. If date1 is in a later year than date2, return False. If they are equal, check the month.
    d1[0] = int(d1[0])
    d2[0] = int(d2[0])
    if d1[0] < d2[0]:
        return True
    elif d1[0] > d2[0]:
        return False

    #Check the month. If date1 is in an earlier month then date2, return True. If date1 is in a later month than date2, return False. If they are equal, check the day.
    d1[1] = int(d1[1])
    d2[1] = int(d2[1])
    if d1[1] < d2[1]:
        return True
    elif d1[1] > d2[1]:
        return False

    #Now we have to split the string again to access the day.
    d1 = d1[2].split('T')
    d2 = d2[2].split('T')

    #Compare the days. If equal, check the time
    d1[0] = int(d1[0])
    d2[0] = int(d2[0])
    if d1[0] < d2[0]:
        return True
    elif d1[0] > d2[0]:
        return False

    #Split again for the time
    d1 = d1[1].split(':')
    d2 = d2[1].split(':')

    #Compare the hours
    d1[0] = int(d1[0])
    d2[0] = int(d2[0])
    if d1[0] < d2[0]:
        return True
    elif d1[0] > d2[0]:
        return False

    #Compare the minutes
    d1[1] = int(d1[1])
    d2[1] = int(d2[1])
    if d1[1] < d2[1]:
        return True
    elif d1[1] > d2[1]:
        return False

    #Compare the seconds
    d1 = d1[2]
    d2 = d2[2]
    #Remove the last character of the string
    d1 = d1[:-1]
    d2 = d2[:-1]

    d1 = int(d1)
    d2 = int(d2)
    if d1 < d2:
        return True
    else:
        return False


