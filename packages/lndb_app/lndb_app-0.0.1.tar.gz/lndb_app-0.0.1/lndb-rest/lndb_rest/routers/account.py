from fastapi import APIRouter
from lndb import settings

router = APIRouter(prefix="/account")


@router.get("/")
def get_current_account_settings():
    return settings.user
