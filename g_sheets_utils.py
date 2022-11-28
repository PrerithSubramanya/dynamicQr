import time
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
        return client.open("QlubAuQR")
    except gspread.SpreadsheetNotFound:
        return client.create("QlubAuQR")


def createLinkAndId(worksheet: Worksheet, suffix: str, start: int, qr_range: int):
    base_url = f"http://l.qlub.io/au/{suffix}"

    worksheet.update(
        "A1:E1", [["Ids", "qrLinks", "LandingURL", "Replaced", "DateTime"]]
    )
    retry = True
    initial_time = 2
    while retry:
        while 2 <= start < qr_range + 2:
            try:
                worksheet.update(
                    f"A{start}:B{start}",
                    [[f"{suffix}-{start - 1}", f"{base_url}-{start - 1}"]],
                )
                start += 1
                retry = False
            except gspread.exceptions.APIError:
                time.sleep(initial_time)
                initial_time = initial_time * 2 if initial_time < 60 else 10
