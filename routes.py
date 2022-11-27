from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from FTP_util import bulkCreateAndChangeURl
from g_sheets_utils import returnClient, returnGSheet, createLinkAndId

gsClient = returnClient()
gSheet = returnGSheet()


class UserEmail(BaseModel):
    email: EmailStr


class GsheetConfig(BaseModel):
    WorkSheetName: Optional[str] = None


router = APIRouter(tags=["Dynamic Qr"])


@router.get("/")
async def root():
    return {"message": "Welcome to Qlub's own dynamic QR page"}


@router.post("/create_qr/{unique_name}/range/{qr_range}")
async def create_qr(unique_name: str, qr_range: int, sheet: GsheetConfig):
    if not sheet.WorkSheetName or sheet.WorkSheetName == "":
        work_sheet = gSheet.sheet1
    else:
        work_sheet = gSheet.add_worksheet(
            title=sheet.WorkSheetName, rows=qr_range + 1, cols=4
        )

    createLinkAndId(work_sheet, unique_name, qr_range)


@router.post(
    "/share_sheet",
    responses={200: {"description": "Successfully shared sheet to user"}},
)
async def shareSheet(email: UserEmail):
    gSheet.share(f"{email.email}", perm_type="user", role="writer")


@router.post("/bulk_upload/{sheet_name}")
async def bulk_upload(sheet_name: str):
    sheet = gSheet.worksheet(sheet_name)
    values_list = sheet.get_all_records()
    bulkCreateAndChangeURl(values_list, sheet)
