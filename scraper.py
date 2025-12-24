from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shutil import which
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os
import sys
from bs4 import BeautifulSoup
from zoneinfo import ZoneInfo
import undetected_chromedriver as uc
import shutil
import re
from google.cloud import bigquery 


LOCATIONS = {'Abbeville': 'https://scdmvonline.com/Locations/Abbeville',
    'Aiken': 'https://scdmvonline.com/Locations/Aiken',
    'Allendale': 'https://scdmvonline.com/Locations/Allendale',
    'Anderson': 'https://scdmvonline.com/Locations/Anderson',
    'Bamberg': 'https://scdmvonline.com/Locations/Bamberg',
    'Barnwell': 'https://scdmvonline.com/Locations/Barnwell',
    'Batesburg': 'https://scdmvonline.com/Locations/Batesburg',
    'Beaufort': 'https://scdmvonline.com/Locations/Beaufort',
    'Belton': 'https://scdmvonline.com/Locations/Belton',
    'Bennettsville': 'https://scdmvonline.com/Locations/Bennettsville',
    'Bishopville': 'https://scdmvonline.com/Locations/Bishopville',
    'Bluffton': 'https://scdmvonline.com/Locations/Bluffton',
    'Camden': 'https://www.scdmvonline.com/Locations/Camden',
    'Charleston - Leeds Avenue': 'https://scdmvonline.com/Locations/Charleston-10-Leeds-Avenue',
    'Charleston - Mount Pleasant': 'https://scdmvonline.com/Locations/Mount-Pleasant',
    'Charleston - Orleans Rd': 'https://scdmvonline.com/Locations/Charleston-Orleans-Rd',
    'Chester': 'https://www.scdmvonline.com/Locations/Chester',
    'Chesterfield': 'https://scdmvonline.com/Locations/Chesterfield',
    "Columbia - O'Neil Court": 'https://www.scdmvonline.com/Locations/Columbia-ONeil-Court',
    'Columbia - Shop Road': 'https://scdmvonline.com/Locations/Columbia-Shop-Road',
    'Conway': 'https://scdmvonline.com/Locations/Conway',
    'Darlington': 'https://scdmvonline.com/Locations/Darlington',
    'Dillon': 'https://scdmvonline.com/Locations/Dillon-DMV',
    'Edgefield': 'https://scdmvonline.com/Locations/Edgefield',
    'Florence': 'https://scdmvonline.com/Locations/Florence',
    'Fort Mill': 'https://www.scdmvonline.com/Locations/Fort-Mill',
    'Fountain Inn': 'https://scdmvonline.com/Locations/Fountain-Inn',
    'Gaffney': 'https://scdmvonline.com/Locations/Gaffney',
    'Georgetown': 'https://scdmvonline.com/Locations/Georgetown',
    'Greenville - Edgeworth': 'https://scdmvonline.com/Locations/Greenville-123-Edgeworth',
    'Greenville - Saluda Dam': 'https://scdmvonline.com/Locations/Greenville-63-Saluda-Dam',
    'Greenwood': 'https://scdmvonline.com/Locations/Greenwood',
    'Greer': 'https://scdmvonline.com/Locations/Greer',
    'Hampton': 'https://scdmvonline.com/Locations/Hampton',
    'Irmo - Ballentine': 'https://www.scdmvonline.com/Locations/Irmo---Ballentine',
    'Kingstree': 'https://scdmvonline.com/Locations/Kingstree',
    'Ladson': 'https://scdmvonline.com/Locations/Ladson',
    'Lake City': 'https://scdmvonline.com/Locations/Lake-City',
    'Lancaster': 'https://www.scdmvonline.com/Locations/Lancaster',
    'Laurens': 'https://scdmvonline.com/Locations/Laurens',
    'Lexington': 'https://www.scdmvonline.com/Locations/Lexington',
    'Manning': 'https://scdmvonline.com/Locations/Manning',
    'Marion': 'https://scdmvonline.com/Locations/Marion',
    'McCormick': 'https://scdmvonline.com/Locations/McCormick',
    'Moncks Corner': 'https://scdmvonline.com/Locations/Moncks-Corner---New-Office',
    'Myrtle Beach': 'https://scdmvonline.com/Locations/Myrtle-Beach',
    'Myrtle Beach Commons': 'https://scdmvonline.com/Locations/Myrtle-Beach-Commons',
    'Newberry': 'https://www.scdmvonline.com/Locations/Newberry',
    'North Augusta': 'https://scdmvonline.com/Locations/North-Augusta',
    'North Myrtle Beach': 'https://scdmvonline.com/Locations/North-Myrtle-Beach',
    'Orangeburg': 'https://scdmvonline.com/Locations/Orangeburg',
    'Pickens': 'https://scdmvonline.com/Locations/Pickens',
    'Ridgeland': 'https://scdmvonline.com/Locations/Ridgeland',
    'Rock Hill': 'https://scdmvonline.com/Locations/Rock-Hill',
    'Saint George': 'https://scdmvonline.com/Locations/Saint-George',
    'Saint Matthews': 'https://scdmvonline.com/Locations/Saint-Matthews',
    'Saluda': 'https://scdmvonline.com/Locations/Saluda',
    'Seneca': 'https://scdmvonline.com/Locations/Seneca',
    'Spartanburg - Fairforest Road': 'https://scdmvonline.com/Locations/Spartanburg-42-Fairforest',
    'Spartanburg - Southport Road': 'https://scdmvonline.com/Locations/Spartanburg-87-Southport-Rd',
    'Sumter': 'https://scdmvonline.com/Locations/Sumter',
    'Union': 'https://scdmvonline.com/Locations/Union',
    'Walterboro': 'https://scdmvonline.com/Locations/Walterboro',
    'Winnsboro': 'https://www.scdmvonline.com/Locations/Winnsboro',
    'Woodruff': 'https://scdmvonline.com/Locations/Woodruff'
    }


# --- Google auth ---
CRED_PATH = (
    os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    or os.environ.get("GOOGLE_CREDENTIALS")
    or os.path.join(os.path.dirname(__file__), "creds.json")
)
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
if not os.path.exists(CRED_PATH):
    sys.stderr.write(
        f"[ERROR] Google service-account file not found: {CRED_PATH}\n"
        "Place your JSON there or set GOOGLE_APPLICATION_CREDENTIALS.\n"
    )
    sys.exit(1)

creds = ServiceAccountCredentials.from_json_keyfile_name(CRED_PATH, SCOPES)
client = gspread.authorize(creds)

###BigQuery


BQ_PROJECT = "dmv-scraper-465620"
BQ_DATASET = "dmv"
BQ_TABLE   = "wait_times"
bq_client = bigquery.Client.from_service_account_json(CRED_PATH, project=BQ_PROJECT)

def ensure_bq_objects():
    # Ensure dataset exists
    ds_ref = bigquery.DatasetReference(BQ_PROJECT, BQ_DATASET)
    try:
        bq_client.get_dataset(ds_ref)
    except Exception:
        ds = bigquery.Dataset(ds_ref)
        ds.location = "US"
        bq_client.create_dataset(ds, timeout=30)

    # Ensure table exists (partitioned by date(timestamp), clustered by location)
    tbl_ref = ds_ref.table(BQ_TABLE)
    try:
        bq_client.get_table(tbl_ref)
    except Exception:
        schema = [
            bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("location",  "STRING",    mode="REQUIRED"),
            bigquery.SchemaField("wait_raw",  "STRING"),
            bigquery.SchemaField("wait_min",  "INT64"),
            bigquery.SchemaField("status",    "STRING"),
        ]
        tbl = bigquery.Table(tbl_ref, schema=schema)
        tbl.time_partitioning = bigquery.TimePartitioning(field="timestamp")
        tbl.clustering_fields = ["location"]
        bq_client.create_table(tbl, timeout=30)

def _parse_wait_minutes(wait_raw: str):
    if not wait_raw or "no data" in wait_raw.lower():
        return None, "No Data"
    if "error" in wait_raw.lower():
        return None, "Error"
    m = re.search(r"(\d+)", wait_raw)
    if m:
        return int(m.group(1)), "OK"
    return None, "Unknown"

def load_rows_to_bq(rows):
    """
    rows = [(timestamp_str, location, wait_raw), ...]
    """
    ensure_bq_objects()

    payload = []
    for ts, loc, raw in rows:
        wait_min, status = _parse_wait_minutes(raw)
        payload.append({
            "timestamp": ts,   # RFC3339 string okay
            "location":  loc,
            "wait_raw":  raw,
            "wait_min":  wait_min,
            "status":    status,
        })

    table_id = f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}"
    errors = bq_client.insert_rows_json(table_id, payload)
    if errors:
        print("[BQ] insert errors (first):", errors[:1])
    else:
        print(f"[BQ] inserted {len(payload)} rows into {table_id}")


print("Who am I:", bq_client.project)
print("Datasets:", [d.dataset_id for d in bq_client.list_datasets()])


### End BigQuery

MONTH_TAB_FORMAT = "%Y-%m"
HEADER_ROW = ["Timestamp", "Location", "Wait Time"]

# def ensure_month_worksheet(spreadsheet, tz="America/New_York"):
#     title = datetime.now(ZoneInfo(tz)).strftime(MONTH_TAB_FORMAT)
#     try:
#         return spreadsheet.worksheet(title)
#     except gspread.exceptions.WorksheetNotFound:
#         ws = spreadsheet.add_worksheet(title=title, rows=1000, cols=max(10, len(HEADER_ROW)))
#         ws.update("A1", [HEADER_ROW])
#         try:
#             ws.freeze(rows=1)
#             ws.format("A1:Z1", {"textFormat": {"bold": True}})
#         except Exception:
#             pass
#         return ws

# sh = client.open("DMV Wait Times")
# sheet = ensure_month_worksheet(sh)

CHROMEDRIVER_PATH = "/usr/bin/chromedriver"   # Debian/RPi location
CHROMIUM_PATHS = ("/usr/bin/chromium", "/usr/bin/chromium-browser")

def make_driver():
    # --- sanity checks ---
    if not shutil.which("chromium") and not shutil.which("chromium-browser"):
        raise RuntimeError(
            "Chromium is not installed or not on PATH. Install with: sudo apt install chromium"
        )
    if not shutil.which("chromedriver") and not shutil.which(CHROMEDRIVER_PATH):
        raise RuntimeError(
            "chromedriver is not installed. Install with: sudo apt install chromium-driver"
        )

    opts = Options()

    for p in CHROMIUM_PATHS:
        if os.path.exists(p):
            opts.binary_location = p
            break

    # Your existing flags/prefs
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,800")
    opts.page_load_strategy = "eager"
    opts.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
        "profile.managed_default_content_settings.fonts": 2,
    })

    # Use the system chromedriver that matches Chromium
    service = Service(CHROMEDRIVER_PATH)
    try:
        driver = webdriver.Chrome(service=service, options=opts)
    except WebDriverException as e:
        raise RuntimeError(
            "Failed to start Chrome via system chromedriver. "
            "Ensure chromium and chromium-driver versions match."
        ) from e

    driver.set_page_load_timeout(12)

    # --- helpful logging + mismatch warning ---
    br = driver.capabilities.get("browserVersion", "")
    dr = driver.capabilities.get("chrome", {}).get("chromedriverVersion", "")
    print("[INFO] Using system chromedriver:", CHROMEDRIVER_PATH)
    print("Browser version:", br)
    print("Driver version:", dr)

    # Warn if major.minor don’t match
    def mm(v):
        m = re.match(r"(\d+)\.(\d+)", str(v))
        return m.groups() if m else ("", "")
    
    if mm(br) != mm(dr):
        print(f"[WARN] Browser/driver mismatch: browser={br}, driver={dr}. "
            "Run: sudo apt update && sudo apt install -y chromium chromium-driver")

    return driver

def scrape_wait_time(driver, url):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
        )                   
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        for row in soup.find_all("tr"):
            tds = row.find_all("td")
            if len(tds) >= 4:
                cells = [td.get_text(strip=True) for td in tds]
                if "Max Wait Time" not in cells:
                    return cells[3] or "No Data"
        return "No Data"
    except Exception as e:
        return f"Error: {e}"

def scrape_all_locations():
    from zoneinfo import ZoneInfo
    from datetime import datetime
    now = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S")
    rows = []

    driver = make_driver()
    try:
        for name, url in LOCATIONS.items():
            wt = scrape_wait_time(driver, url)
            if len(wt) > 120:
                wt = "No Data"
            rows.append((now, name, wt))
    finally:
        driver.quit()
    return rows

if __name__ == "__main__":
    rows = scrape_all_locations()
    print(f"[dmv] rows prepared: {len(rows)}")
    bq_ok = False
    try:
        load_rows_to_bq(rows)
        bq_ok = True
    except Exception as e:
        sys.stderr.write(f"[ERROR][BQ] {e}\n")
    # sheets_ok = False
    # try:
    #     sheet.append_rows(rows, value_input_option="USER_ENTERED")
    #     sheets_ok = True
    # except AttributeError:
    #     for r in rows:
    #         sheet.append_row(list(r), value_input_option="USER_ENTERED")
    #         sheets_ok = True

    # print(f"[done] BigQuery: {'OK' if bq_ok else 'FAIL'} | Sheets: {'OK' if sheets_ok else 'FAIL'}")
    print(f"[done] BigQuery: {'OK' if bq_ok else 'FAIL'})

