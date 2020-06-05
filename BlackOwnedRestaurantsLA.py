# Owner: Omri Fried
# Last Edit Date: 06/05/2020
# Description: Automation script that uses the Google Maps API and Google Drive/Sheets API to 
#              convert a Google Sheet with Black-Owned Restaurants in LA into a Google Map.
#              In order to use the script, the user must create a (free) GCP account and get
#              an API Key for the Google Maps API. Additionally, the user must enable both
#              the Google Sheets and Google Drive API. More information on how to access the
#              APIs in README.

import googlemaps
import gspread
import csv
## Custom script that contains my API Key, username, and password
import APIKeyCall

from oauth2client.service_account import ServiceAccountCredentials
from time import sleep
from selenium import webdriver


class LoginPage:
    """
    Login class that allows the user to automatically log-in to their
    Google account. If an ELEMENTNOTFOUND error occurs, increase the sleep
    time by one second to make sure that the browser loads before attempting
    to sign.
    """
    def __init__(self, browser):
        self.browser = browser

    def login(self, username, password):
        ## Find the "Sign in" button on Google maps
        loginButton = self.browser.find_element_by_link_text('Sign in')
        loginButton.click()

        sleep(2)

        ## Find the username field and upload the username into the field, then click next
        usernameInput = self.browser.find_element_by_name('identifier')
        usernameInput.send_keys(username)
        usernameButton = self.browser.find_element_by_id("identifierNext")
        usernameButton.click()

        sleep(2)

        ## Find the password field and upload the password into the field, then click next
        passwordInput = self.browser.find_element_by_name('password')
        passwordInput.send_keys(password)
        passwordButton = self.browser.find_element_by_id("passwordNext")
        passwordButton.click()


class AddToList:
    """
    List add class that adds the entry to the Google Map. If an OUTOFBOUNDS error occurs
    on line 74 due to index bounds, increase the sleep time on line 71 to allow the widget
    to fully load before attempting to click it. The index may vary depending on where your
    map list is located in the widget.
    """
    def __init__(self, browser):
        self.browser = browser
    
    def addList(self, index):
        ## Find the "Save" button in Google maps if it exists
        if len(self.browser.find_elements_by_xpath("//button[@data-value='Save']")) != 0:
            listButton = self.browser.find_element_by_xpath("//button[@data-value='Save']")
            listButton.click()

            sleep(1)

            ## Get the possible mini buttons from the widget list
            possibleLists = self.browser.find_elements_by_class_name('action-menu-entry-text-container')

            sleep(3)

            ## Click the desired list to save the location to the lsit
            myList = possibleLists[index]
            browser.execute_script("arguments[0].click();", myList)
            
            sleep(2)


class ParseSheet:
    """
    Parse class that accesses the Google Sheets/Drive API and parses the desired spreadsheet. The parser
    adds the restauarants to a list object that can then be looped through.
    """
    def parseSheet(self, spreadsheet, startPoint):
        ## Open the Google spreadsheet with Black Owned Restaurants in LA using the sheets/drive API
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']   
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open(spreadsheet).sheet1
        sheet2 = client.open(spreadsheet).sheet1

        ## Get all the restaurant names and return the list
        totalDrive = sheet.col_values(1)

        ## Write all current restaurant names to CSV. The doc length will be used as the startPoint
        with open('restaurantdata.csv', 'w') as outfile:
            csvwriter = csv.writer(outfile)  
            csvwriter.writerows(totalDrive)
        driveLen = len(totalDrive)

        ## Put the start point at the newest addition so as not to revisit restaurants already in the list
        startPosition = 'A' + str(startPoint)

        ## Put the end position at the full length of the sheet
        endPosition = 'A' + str(driveLen)

        ## If there are new restaurants pull them, otherwise mark it as QUIT
        # if startPosition != endPosition:
        sheetRange =  startPosition + ':' + endPosition 
        driveTrix = sheet2.get(sheetRange)
        return driveTrix
        # else:
        #     return 'QUIT'


class GoogleMapsId:
    """
    Map class to add the restaurants to Google Maps. The class uses the Google Maps API to 
    find the restaurants in the spreadsheet list and add them to maps. Filters can be adjusted 
    based on type of locations.
    """
    def __init__(self, browser):
        self.browser = browser

    def mapsId(self, key, driveTrix):
        ## Connect to Google Maps API
        gmaps = googlemaps.Client(key = key)
        for name in driveTrix:
            ## Pull the name from the list object. This is the name in the Google spreadshee
            if len(name) > 0:
                nameString = str(name)[2: len(str(name)) - 2: 1].lower()
                ## Avoid pop-ups since they are not found in Google Maps and can lead to erroneuos results
                if "pop-up" not in nameString:
                ## Only search for places tagged as food by the name in the spreadsheet within 100 miles of LA
                    totalList = gmaps.places(query = name, location = '34.052235,-118.243683', radius = 161000, type = 'food')
                    locationDetail = totalList['results']
                    if len(locationDetail) > 0:
                        locationDetail2 = locationDetail[0]
                        ## Find the location's name
                        restaurantName = locationDetail2['name']
                        ## Find the first word in the name provided by Google Maps API
                        firstWord = restaurantName.split()[0].lower()
                        ## Remove apostrophe at the end of the word
                        if firstWord[len(firstWord) - 2: len(firstWord): 1] == "'s":
                            firstWord = firstWord[0: len(firstWord) - 2: 1]
                        ## Only add the location to the map if it soft-matches on name between the API and the spreadsheet
                        if firstWord in nameString:
                            ## Find the location's place ID and search for it in the Google search bar
                            restaurantPlaceId = str(locationDetail2['place_id'])
                            self.browser.get('https://www.google.com/maps/search/?api=1&query=Red%20Hen%20Cafe%2C%202697%20Fair%20Oaks%20Ave%2C%20Altadena%2C%20CA&query_place_id=' + restaurantPlaceId)
                            sleep(4)
                            listAdd = AddToList(self.browser)
                            listAdd.addList(4)


## Initialize the browser object and open a Google maps page
browser = webdriver.Chrome(executable_path=r'/Users/omrifried/Documents/Summer_2020_Projects/BLM_Restaurants/chromedriver')
browser.get('https://www.google.com/maps/')

sleep(2)

## Login in to the Google account
startLogin = LoginPage(browser)
startLogin.login(APIKeyCall.getUserName(), APIKeyCall.getPassword())

startPos = 1

## This can be used to determine the new start point. The original Black-Owned LA Restaurant list has a filter on it, so this won't
## work on it since newly added restaurants won't be at the bottom of the sheet. But it will work on sheets without filters if the loop
## on line 114 is uncommented.
# csvRows = []
# ## Open the CSV to count the number of rows
# with open('restaurantdata.csv', 'r') as csvfile: 
#     csvreader = csv.reader(csvfile)
#     fields = next(csvreader) 
#     for row in csvreader: 
#         csvRows.append(row) 
#     ## Determine the length of the CSV
#     if csvreader.line_num > 0:
#         startPos = csvreader.line_num

## Parse the Google sheet and add restaurants to the map list
driveData = ParseSheet()
sheetData = driveData.parseSheet('LA-Black-Owned-Restaurants-2020', startPos)
if sheetData != 'QUIT':
    placesId = GoogleMapsId(browser)
    placesId.mapsId(APIKeyCall.getKey(), sheetData)

browser.close()