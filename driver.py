#This file contains the main() function and calls most of the functions in the program.
#I have included below some UNIX timecodes that can be used with launch mode 2 in order to further test the program.
#
# New Years Day (01/01/2021): 1609459200
# Christmas Day (12/25/2020): 1608854400
# Election Day [California] (11/03/2020): 1604361600
# First Reported COVID-19 Case (12/31/2019): 1577750400
# Default Ending Date (01/10/2020): 1578657600
# Default Starting Date (12/15/2019): 1576411200
# January 01, 1970 (01/01/1970): 0000000000

import incrementalExport

def main():
    #If you would like to paste the API Token in here instead of on the command line, you can do that as well. Change defaultAPI to true if you are doing so.
    defaultAPI = True
    apiToken = 'JvlM6WHjKR8OzUay1XK2HFGr0OfdZnutWH2uLGc3'

    #Choose which mode to launch in
    print("Please choose launch mode 1 or 2. \nLaunch mode 2 will allow for custom date parameters. \nPlease enter 1 or 2: ", end='')
    while True:
        mode = input()
        if mode.isdigit():
            mode = int(mode)
            if mode == 1 or mode == 2:
                break
        print('Please enter a valid launch mode: ', end='')

    #These are the default date values.
    #Starting = 12/15/2019 12:00PM
    #Ending = 01/10/2020 12:00PM
    starting = '1576411200'  
    ending = '1578657600'

    #Request start time and end time from the user if launch mode 2 was chosen
    if mode == 2:
        starting = input("Please input the first date parameter in UNIX Time: ")

        ending = input("Please input the second date parameter in UNIX Time: ")

    #Makes the ending time exclusive:
    ending = int(ending)
    ending = ending - 1
    ending = str(ending)

    #Request subdomain from the user
    subdomain = input("Please enter the subdomain that you would like to access: ")
    url = 'https://' + subdomain + '.zendesk.com/api/v2/incremental/tickets/cursor.json?start_time=' + starting

    #Request email from the user
    user = input("Please enter your email: ")
    user = user + '/token'

    #Request API Token from the user if defaultAPI is false
    pwd = apiToken
    if defaultAPI == False:
        pwd = input("Please enter your API token: ")

    #Make HTTP GET request and store the JSON object in data
    data = incrementalExport.getResponse(user, pwd, url)

    #Adds the first valid ticket to the sortedData array.
    sortedData = []
    for ticket in data['tickets']:
        ticketDate = ticket['created_at']
        outerBound = incrementalExport.convertTime(ending)
        if incrementalExport.precedes(ticketDate, outerBound):
            sortedData.append(incrementalExport.truncateTicket(data['tickets'][0]))
            break

    #If there were no valid entries, the program exits.
    if len(sortedData) == 0:
        print('No tickets were found inside the date range given. Exiting Program.')
        exit()

    #Adds the rest of the tickets to the array. It will insert the tickets in order of date created.
    for i in range(1, len(data['tickets'])):
        #If the date of the i'th ticket precedes a ticket, insert it before that ticket
        for j in range(len(sortedData)):
            if incrementalExport.precedes(data['tickets'][i]['created_at'], sortedData[j][3]):
                #Check to see if it precedes the end date
                if(incrementalExport.precedes(incrementalExport.truncateTicket(data['tickets'][i])[3], incrementalExport.convertTime(ending))):
                    sortedData.insert(j, incrementalExport.truncateTicket(data['tickets'][i]))
            if j == len(sortedData)-1:
                #Check to see if it precedes the end date
                if(incrementalExport.precedes(incrementalExport.truncateTicket(data['tickets'][i])[3], incrementalExport.convertTime(ending))):
                    sortedData.append(incrementalExport.truncateTicket(data['tickets'][i]))
                continue
                
    #Say we have reached the end of the page of tickets. Now we need to call the next page of tickets and add those to the sortedData array
    #To do so, make another HTTP GET Request using the after_cursor JSON parameter
    curVar = data['after_cursor']
    url = 'https://' + subdomain + '.zendesk.com/api/v2/incremental/tickets/cursor.json?&cursor=' + curVar

    while data['end_of_stream'] == False:
        data = incrementalExport.getResponse(user, pwd, url)
        for i in range(0, len(data['tickets'])):
            #If the date of the i'th ticket precedes a ticket, insert it before that ticket
            for j in range(len(sortedData)):
                if incrementalExport.precedes(data['tickets'][i]['created_at'], sortedData[j][3]):
                    #Check to see if it precedes the end date
                    if(incrementalExport.precedes(incrementalExport.truncateTicket(data['tickets'][i])[3], incrementalExport.convertTime(ending))):
                        sortedData.insert(j, incrementalExport.truncateTicket(data['tickets'][i]))
                if j == len(sortedData)-1:
                    #Check to see if it precedes the end date
                    if(incrementalExport.precedes(incrementalExport.truncateTicket(data['tickets'][i])[3], incrementalExport.convertTime(ending))):
                        sortedData.append(incrementalExport.truncateTicket(data['tickets'][i]))
                    continue
            
    #Open a new file
    outputFile = open('tickets.txt', 'w')
    for ticket in sortedData:
        outputFile.write('----Ticket ID: ' + str(ticket[0]) + '----\n')
        outputFile.write('Subject: ' + str(ticket[1]) + '\n')
        outputFile.write('Description: ' + str(ticket[2]) + '\n')
        outputFile.write('Created At: ' + str(ticket[3]) + '\n')
        outputFile.write('\n')

    #Close the file
    outputFile.close()
    print('Program ran successfully! The selected tickets have been output to a file in this directory titled: tickets.txt')

if __name__ == "__main__":
    main()