import requests
from datetime import datetime
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timezone, timedelta
import time
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os
import base64
from bs4 import BeautifulSoup


def write_temp_credentials():
    encoded = os.environ.get("GOOGLE_CREDS_B64")
    if not encoded:
        raise RuntimeError("❌ GOOGLE_CREDS_B64 not set in environment")
    
    with open("dmv-logger-credentials.json", "wb") as f:
        f.write(base64.b64decode(encoded))

write_temp_credentials()

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("dmv-logger-credentials.json", scope)
client = gspread.authorize(creds)
for s in client.openall():
    print("📄 Found sheet:", s.title)

sheet = client.open("DMV Wait Times").sheet1  # Use your sheet name




LOCATIONS = {
    "Greenville - Saluda Dam": "https://scdmvonline.com/Locations/Greenville-63-Saluda-Dam",
    "Greenville - Edgeworth": "https://scdmvonline.com/Locations/Greenville-123-Edgeworth",
    "Pickens": "https://scdmvonline.com/Locations/Pickens",
    "Greer": "https://scdmvonline.com/Locations/Greer",
    "Fountain Inn": "https://scdmvonline.com/Locations/Fountain-Inn"
    
    
    # Add more as needed
}

def scrape_wait_time(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    driver.quit()

    rows = soup.find_all("tr")
    for row in rows:
        tds = row.find_all("td")
        if len(tds) >= 4:
            cell_texts = [td.text.strip() for td in tds]
            if "Max Wait Time" not in cell_texts:
                return cell_texts[3]  # Max Wait Time

    return "No Data"




def scrape_all_locations():
    results = []
    tz_utc = timezone.utc
    tz_eastern = timezone(timedelta(hours=-4))
    # now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    now = datetime.now().astimezone(tz_eastern).strftime('%Y-%m-%d %H:%M:%S')
    # now = now.astimezone(tz_eastern)
    for name, url in LOCATIONS.items():
        try:
            wait_time = scrape_wait_time(url)
            results.append((now, name, wait_time))
        except Exception as e:
            results.append((now, name, f"Error: {e}"))
    return results

results = scrape_all_locations()

for row in results:
    sheet.append_row(list(row))

