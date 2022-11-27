import os
from ftplib import FTP
from gspread import Worksheet


def bulkCreateAndChangeURl(qrIdsList: list, sheet: Worksheet) -> None:
    if qrIdsList:
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
                    cell = sheet.find(f"{qrIds.get('Ids')}")
                    sheet.update_cell(cell.row, 4, "Yes")
