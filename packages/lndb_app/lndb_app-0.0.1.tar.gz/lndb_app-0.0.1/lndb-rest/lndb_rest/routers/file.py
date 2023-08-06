import lamindb as ln
from fastapi import APIRouter
from fastapi import UploadFile

router = APIRouter(prefix="/file")


@router.get("/")
async def get_files(order_by: str = None, desc: bool = True):

    if order_by == "name":
        order_by_exp = ln.File.name
    else:
        order_by_exp = ln.File.created_at

    if desc is True:
        order_by_exp = order_by_exp.desc()

    files = (
        ln.select(ln.File.id, ln.File, ln.Run, ln.User, ln.Transform)
        .join(ln.Run, ln.Run.id == ln.File.source_id)
        .join(ln.User, ln.User.id == ln.Run.created_by)
        .join(ln.Transform, (ln.Transform.id == ln.Run.transform_id), (ln.Transform.v == ln.Run.transform_v))
        .order_by(order_by_exp)
    ).all()

    return files


@router.get("/{file_id}")
async def get_file(file_id: str):

    file = (
        ln.select(ln.File.id, ln.File, ln.Run, ln.User, ln.Transform)
        .join(ln.Run, ln.Run.id == ln.File.source_id)
        .join(ln.User, ln.User.id == ln.Run.created_by)
        .join(ln.Transform, (ln.Transform.id == ln.Run.transform_id), (ln.Transform.v == ln.Run.transform_v))
        .where(ln.File.id == file_id)
    ).one()

    return file


@router.post("/add")
async def add_file(uploadFile: UploadFile):
    transform = ln.add(ln.Transform(name="transform_1", v="1"))
    run = ln.Run(transform=transform)
    contents = await uploadFile.read()
    with open(uploadFile.filename, "wb") as binary_file:
        binary_file.write(contents)
    file = ln.File(uploadFile.filename, source=run)
    ln.add(file)
    return {"filename": uploadFile.filename}
