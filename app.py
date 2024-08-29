import os
from dotenv import load_dotenv
from flask import Flask, render_template
from google.oauth2 import service_account
from googleapiclient.discovery import build
from collections import defaultdict

load_dotenv()
SPREADSHEET_ID = os.getenv("SHEET_ID")
app = Flask(__name__)

# Setup Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = '.secrets/token.json'
RANGE_NAME = 'Menu!A2:D999'  # Assumes your data starts from A2

# Create credentials using the service account file
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Google Sheets API service
service = build('sheets', 'v4', credentials=creds)

# Load credentials from the service account file
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Google Sheets API service
service = build('sheets', 'v4', credentials=creds)

def get_menu_from_sheet():
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])
    
    menu = defaultdict(list)
    for row in values:
        if len(row) >= 4:
            category, name, base, flavors = row
            menu[category].append({
                "name": name,
                "base": base,
                "flavors": flavors
            })
    return dict(menu)

@app.route('/favicon.svg')
def favicon():
    return send_file('static/favicon.svg', mimetype='image/svg+xml') # type: ignore

@app.route('/')
def menu():
    soda_menu = get_menu_from_sheet()
    return render_template('menu.html', menu=soda_menu)

def generate_static_site():
    soda_menu = get_menu_from_sheet()
    with app.app_context():
        rendered = render_template('menu.html', menu=soda_menu)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(rendered)

if __name__ == '__main__':
    generate_static_site()
    print("Static site generated as index.html")