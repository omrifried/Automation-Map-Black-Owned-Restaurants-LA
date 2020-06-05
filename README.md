# Automation-Map-Black-Owned-Restaurants-LA

### <ins>Project Description</ins>:
This python automation script is used to convert a Google spreadsheet into a Google map for Black Owned Restaurants in LA. The script uses Google Maps, Drive, and Sheets APIs to parse the Google spreadsheet and create a Google map from it. 


### <ins>Creating the spreadsheet</ins>:
The Black-Owned Restaurants in LA spreadsheet I use can be found [here](https://docs.google.com/spreadsheets/d/1r27r7aKiiuCtdCYFcReoUE8ZwXcX1VKbOygS_Do5Uec/edit?usp=sharing). The two formulas used can be found in cells A1 and B1. The IMPORTRANGE formula creates a dynamic copy of the original spreadsheet and the formula in column A concatenates the name with the location to create a more precise search criteria.

### <ins>Working with APIs</ins>:
The APIs needed for this project are the Google Maps, Sheets, and Drive APIs. Create a GCP account in order to use these APIs.
#### Google Maps API:
Find the Google Maps API and enable it in your project. Go to "Credentials" and click on "Create Credentials" to create an API Key. Once you have the API Key, make sure to copy it so that it can be used in the script. Configure the key as needed for API restrictions. My key has no application restrictions but is restricted to the Google Maps API.

#### Google Sheets/Drive API:
Find the Google Sheets API and enable it. Next, find the Google Drive API and enable it. For the Google Drive API, a tutorial on how to set it up can be found [here](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html?utm_source=youtube&utm_medium=video&utm_campaign=youtube_python_google_sheets). Only read the section titled "Google Drive API and Service Accounts" as the rest is already integrated into the code.


### <ins>Other Necessary Add-Ons</ins>: 
#### Downloading Libraries
Make sure you have pip installed on your computer. Next, run the following commands: 
pip install gspread oauth2client
pip install googlemaps
pip install selenium
