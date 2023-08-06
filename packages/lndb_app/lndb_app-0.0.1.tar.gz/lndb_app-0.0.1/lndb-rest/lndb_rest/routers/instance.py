from fastapi import APIRouter
from lndb import settings
from lnhub_rest.routers.instance import (
    get_instance_by_name as get_instance_by_name_base,
)

router = APIRouter(prefix="/instance")


@router.get("/")
def get_current_instance():
    instance = get_instance_by_name_base(
        settings.instance._owner, settings.instance._name, f"Bearer {settings.user.access_token}"
    )
    return {
        **instance,
        "storage": {
            "root": "..."
        }
    }


@router.get("/settings")
def get_current_instance_settings():
    return {
        "owner": settings.instance._owner,
        "name": settings.instance._name,
        "storage": settings.instance._storage,
        "db": settings.instance._db,
        "schema_str": settings.instance._schema_str,
    }
