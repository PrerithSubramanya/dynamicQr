import gspread
from gspread import Worksheet
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

credentials = ServiceAccountCredentials.from_json_keyfile_name("dynamicqr.json", scope)


def returnClient():
    return gspread.authorize(credentials=credentials)


def returnGSheet():
    client = returnClient()
    try:
        return client.open("testSheetSample")
    except gspread.SpreadsheetNotFound:
        return client.create("testSheetSample")


def createLinkAndId(worksheet: Worksheet, suffix: str, qr_range: int):
    base_url = f"http://l.qlub.io/au/{suffix}"

    worksheet.update(
        "A1:E1", [["Ids", "qrLinks", "LandingURL", "Replaced", "DateTime"]]
    )

    for i in range(2, qr_range + 2):
        worksheet.update(f"A{i}:B{i}", [[f"{suffix}_{i-1}", f"{base_url}_{i-1}"]])
