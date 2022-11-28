import os
import time
from datetime import datetime
from ftplib import FTP

import gspread.exceptions
from gspread import Worksheet


def bulkCreateAndChangeURl(qrIdsList: list, sheet: Worksheet) -> None:
    if not qrIdsList:
        return
    with FTP(
        host="sv14055.xserver.jp", user="qr@l.qlub.io", passwd="Starhip22!"
    ) as ftp:
        ftp.cwd("au")
        for qrIds in qrIdsList:
            if qrIds.get("Replaced") == "" and qrIds.get("LandingURL") != "":
                with open(f'{qrIds.get("Ids")}.html', "w") as f:
                    f.write(
                        f'<meta http-equiv="refresh" content="0; URL={qrIds.get("LandingURL")}" />'
                    )
                with open(f'{qrIds.get("Ids")}.html', "rb") as f:
                    ftp.storbinary(f'STOR {qrIds.get("Ids")}.html', f)
                os.remove(f'{qrIds.get("Ids")}.html')
                retry = True
                initial_time = 2
                while retry:
                    try:
                        cell = sheet.find(f"{qrIds.get('Ids')}")
                        sheet.update_cell(cell.row, 4, "Yes")
                        sheet.update_cell(cell.row, 5, str(datetime.now()))
                        retry = False
                    except gspread.exceptions.APIError:
                        time.sleep(initial_time)
                        initial_time = initial_time * 2 if initial_time < 60 else 10
