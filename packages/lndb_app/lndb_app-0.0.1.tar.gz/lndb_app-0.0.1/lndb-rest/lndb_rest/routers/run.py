import lamindb as ln
from fastapi import APIRouter
import pandas as pd
from lnschema_core.link import RunIn

router = APIRouter(prefix="/run")


@router.get("/")
async def get_runs(order_by: str = None, desc: bool = True):

    if order_by == "name":
        order_by_exp = ln.Run.name
    else:
        order_by_exp = ln.Run.created_at

    if desc is True:
        order_by_exp = order_by_exp.desc()

    runs = (
        ln.select(ln.Run.id, ln.Run, ln.User, ln.Transform)
        .join(ln.Transform, (ln.Transform.id == ln.Run.transform_id), (ln.Transform.v == ln.Run.transform_v))
        .join(ln.User, ln.User.id == ln.Run.created_by)
        .order_by(order_by_exp)
    ).all()

    if len(runs) == 0:
        return []

    input_files = (
        ln.select(ln.Run.id, ln.File)
        .join(RunIn, ln.Run.id == RunIn.run_id)
        .join(ln.File, RunIn.file_id == ln.File.id)
    ).all()

    output_files = (
        ln.select(ln.Run.id, ln.File)
        .join(ln.File, ln.File.source_id == ln.Run.id)
    ).all()

    runs_df = pd.DataFrame(runs)

    if len(input_files) > 0:
        runs_input_files_df = (
            pd.DataFrame(input_files)
            .rename(columns={"File": "Input"})
            .groupby("id")["Input"]
            .apply(list)
            .reset_index()
        )
    else:
        runs_input_files_df = pd.DataFrame([], columns=["id", "Input"])

    if len(output_files) > 0:
        runs_output_files_df = (
            pd.DataFrame(output_files)
            .rename(columns={"File": "Output"})
            .groupby("id")["Output"]
            .apply(list)
            .reset_index()
        )
    else:
        runs_output_files_df = pd.DataFrame([], columns=["id", "Output"])

    runs_df = join_with_runs_input_files(runs_df, runs_input_files_df)
    runs_df = join_with_runs_output_files(runs_df, runs_output_files_df)

    return runs_df.to_dict("records")


def join_with_runs_input_files(runs_df: pd.DataFrame, runs_input_files_df: pd.DataFrame):
    run_with_files = runs_df.merge(runs_input_files_df, how="left")
    run_with_files["Input"] = run_with_files["Input"].fillna("").apply(list)
    return run_with_files


def join_with_runs_output_files(runs_df: pd.DataFrame, runs_output_files_df: pd.DataFrame):
    run_with_files = runs_df.merge(runs_output_files_df, how="left")
    run_with_files["Output"] = run_with_files["Output"].fillna("").apply(list)
    return run_with_files


@router.get("/{run_id}")
async def get_run(run_id: str, order_by_file: str = None, desc_file: bool = True):

    if order_by_file == "name":
        order_by_file_exp = ln.File.name
    else:
        order_by_file_exp = ln.File.created_at

    if desc_file is True:
        order_by_file_exp = order_by_file_exp.desc()

    run = (
        ln.select(ln.Run, ln.User, ln.Transform)
        .join(ln.Transform, (ln.Transform.id == ln.Run.transform_id), (ln.Transform.v == ln.Run.transform_v))
        .join(ln.User, ln.User.id == ln.Run.created_by)
        .where(ln.Run.id == run_id)
    ).one()

    input_files = (
        ln.select(ln.Run.id, ln.File)
        .join(RunIn, ln.Run.id == RunIn.run_id)
        .join(ln.File, RunIn.file_id == ln.File.id)
        .order_by(order_by_file_exp)
    ).all()

    output_files = (
        ln.select(ln.Run.id, ln.File)
        .join(ln.File, ln.File.source_id == ln.Run.id)
        .order_by(order_by_file_exp)
    ).all()

    return {
        **run,
        "Input": input_files,
        "Output": output_files
    }
