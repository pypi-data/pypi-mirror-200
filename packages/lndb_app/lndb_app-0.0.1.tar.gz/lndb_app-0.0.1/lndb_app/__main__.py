import argparse
import subprocess

from lndb._settings import settings
from lndb._settings_store import settings_dir

description_cli = "CLI for lndb-app."
parser = argparse.ArgumentParser(
    description=description_cli, formatter_class=argparse.RawTextHelpFormatter
)
subparsers = parser.add_subparsers(dest="command")

# init
i = subparsers.add_parser("init")

# run
r = subparsers.add_parser("run")

# stop
s = subparsers.add_parser("stop")

# run-dev
rd = subparsers.add_parser("run-dev")

# parse args
args = parser.parse_args()


def main():
    if args.command == "init":
        cmd_init_api = "(cd lndb-rest/ && docker build . -t lndb-rest)"
        cmd_init_ui = "(cd lndb-ui/ && docker build . -t lndb-ui)"
        cmd = f"{cmd_init_api} & {cmd_init_ui}"
        subprocess.run(cmd, shell=True)

    if args.command == "run":
        if not settings.instance.storage.is_cloud:
            cmd_run_api = (
                f"docker run -p 8000:8000 -v {settings_dir}:/root/.lndb -v "
                f"{settings.instance.storage.root}:{settings.instance.storage.root} "
                "--name lndb-rest lndb-rest"
            )
        else:
            cmd_run_api = (
                f"docker run -p 8000:8000 -v {settings_dir}:root/.lndb  --name"
                " lndb-rest lndb-rest"
            )
        cmd_run_ui = (
            """docker run -p 3000:3000 """
            """-e NEXT_PUBLIC_LAMIN_REST_DB_URL="http://localhost:8000" """
            """--name lndb-ui lndb-ui"""
        )
        cmd = f"{cmd_run_api} & {cmd_run_ui}"
        subprocess.run(cmd, shell=True)

    if args.command == "stop":
        cmd_stop_api = "docker stop lndb-rest && docker rm lndb-rest"
        cmd_stop_ui = "docker stop lndb-ui && docker rm lndb-ui"
        cmd = f"{cmd_stop_api} && {cmd_stop_ui}"
        subprocess.run(cmd, shell=True)

    if args.command == "run-dev":
        cmd_run_api = "(cd lndb-rest/lndb_rest && python3 main.py)"
        cmd_run_ui = "(cd lndb-ui/ && yarn dev)"
        cmd = f"{cmd_run_api} & {cmd_run_ui}"
        subprocess.run(cmd, shell=True)
