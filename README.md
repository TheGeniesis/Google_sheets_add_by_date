# Google sheets add by date

![Python 3.8](https://img.shields.io/badge/Python-3.8-green)
![Gdrive 3](https://img.shields.io/badge/GDrive_api-v3-green)

This is a simple repository created to add basic data structure to Google sheets.

## Warnings

It's not recommended using this application. 

This application was created only for learning purposes.

## Basic logic

The code creates new Google sheets by date if it doesn't exist. Saves basic structure there.

if the sheet exists then it will add a new record inside the sheet

The application uses different api keys (token) depending on API.
- Credentials - is required to connect with GCP (GDrive)
- Token - token for API requests (generated)
- Secrets - keys to connect with sheets

## Known problems

The code is not bulletproof. 
 
- Application is interested only in last created sheet with specific name
- Some variables are hardcoded
- sheetname - this variable should have different name for different languages
- email - is hardcoded (should be in .env)
- Code should be split to smaller functions for better readability 