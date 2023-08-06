import importlib
from typing import Dict, List

import lamindb as ln
import numpy as np
from fastapi import APIRouter
from lamindb.schema._table import table_meta
from lndb import settings
from lndb import settings as _settings
from lndb.dev._setup_schema import get_schema_module_name

router = APIRouter(prefix="/introspection")

@router.get("/")
async def get_db_schema() -> Dict[str, List[str]]:
    # the following is based on `lamindb.view()`
    schema_names = ["core"] + list(_settings.instance.schema)
    all_orms = {}
    for schema_name in schema_names:
        schema_module = importlib.import_module(get_schema_module_name(schema_name))
        orms = [
            i
            for i in schema_module.__dict__.values()
            if i.__class__.__name__ == "SQLModelMetaclass" and hasattr(i, "__table__")
        ]
        # make an entry for the schema module
        all_orms[schema_name] = {orm.__name__ for orm in orms}
        # alternatively, use pydantic fields
        # for orm in orms:
        #     # capture information about all fields for every ORM
        #     all_orms[schema_name][orm.__name__] = orm.__fields__
        # alternatively, use sqlalchemy tables
        # ...
    return all_orms


@router.get("/{schema_name}/{table_name}")
async def get_table(schema_name: str, table_name: str):
    table_metaclass = get_table_metaclass(schema_name, table_name)

    # Rows
    table_df = (
        ln
        .select(table_metaclass)
        .df()
        .replace({np.nan: None})
        .reset_index()
    )
    rows = table_df.to_dict(orient="records")

    # Schema
    table_object = ln.schema._core.get_table_object(f"{schema_name}.{table_name}")
    schema = ln.schema._core.get_table_metadata_as_dict(table_object)

    return {"schema": schema, "rows": rows}


def get_table_metaclass(schema_name, table_name):
    if settings.instance.dialect == "sqlite":
        return table_meta.get_model(f"{schema_name}.{table_name}")
    else:
        return table_meta.get_model(table_name)
