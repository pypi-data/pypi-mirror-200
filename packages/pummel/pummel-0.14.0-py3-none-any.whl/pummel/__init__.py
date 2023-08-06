import datetime
import json
from pathlib import Path
from typing import Optional, List

import kivalu
import yaml

from .classes import Status, Command, KeyToTarget, ContentToTarget, Task
from .constants import ENCODING, REPORTS_PATH_DEFAULT, KEY_DEFAULT, ATTEMPTS_DEFAULT, PAUSE_DEFAULT, VARIANT_DEFAULT, INCLUDE, COMMAND, VARIANT, KEY, TARGET, CONTENT, STATUS


def run(*,
        reports_path: Path = REPORTS_PATH_DEFAULT,
        key: str = KEY_DEFAULT,
        attempts: int = ATTEMPTS_DEFAULT,
        pause: float = PAUSE_DEFAULT,
        dry: bool = False,
        interactive: bool = False,
        **client_args) -> None:
    client = kivalu.Client(**client_args)
    reports_path.mkdir(parents=True, exist_ok=True)

    print(f"fetching script '{key}' from server {client.url} with levels {client.levels}")
    # the dynamic of the loop and the 'tasks' list below is this:
    # - includes are replaced by the corresponding script items, which are in turn replaced by Task objects (if they're not includes themselves)
    # - the index is only incremented after that final Task transformation
    tasks = [{INCLUDE: key}]
    i = 0
    while i < len(tasks):
        if isinstance(tasks[i], str):  # normalizing a command string into its dictionary counterpart
            tasks[i] = {COMMAND: tasks[i], VARIANT: VARIANT_DEFAULT}

        if not isinstance(tasks[i], dict):
            raise ValueError(f"malformed task, must be a string or a dictionary: {json.dumps(tasks[i])}")

        if (keys := tasks[i].keys()) == {INCLUDE}:
            if not (value := client.get(key := tasks[i].get(INCLUDE))):
                raise LookupError(f"key '{key}' not found")
            if not isinstance(script := yaml.load(value, Loader=yaml.BaseLoader), list):
                raise ValueError(f"key '{key}' is not a proper yaml or json list")

            tasks[i:i + 1] = script  # replaces the include by the script's items (see https://docs.python.org/3/glossary.html#term-slice)
            continue

        # creating an Entry object first
        if keys == {COMMAND, VARIANT}:
            entry = Command(tasks[i].get(COMMAND), tasks[i].get(VARIANT))
        elif keys == {KEY, TARGET}:
            entry = KeyToTarget(tasks[i].get(KEY), tasks[i].get(TARGET))
        elif keys == {CONTENT, TARGET}:
            entry = ContentToTarget(tasks[i].get(CONTENT), tasks[i].get(TARGET))
        else:
            raise ValueError(f"malformed task, unknown keys: {json.dumps(tasks[i])}")

        # computing status
        if any(task.entry == entry for task in tasks[:i]):
            status = Status.IGNORED
        elif (report := reports_path.joinpath(entry.md5)).exists():
            status = json.loads(report.read_text(encoding=ENCODING)).get(STATUS)
        else:
            status = Status.PENDING

        # creating the Task and moving to the next item
        print(f"{status}: {entry.json}")
        tasks[i] = Task(entry, status)
        i += 1

    if dry:  # a dry run stops here
        return

    print()

    # filtering the tasks that are going to be executed
    if not (tasks := [task for task in tasks if task.status in [Status.PENDING, Status.FAILURE]]):
        print("no pending or failed task to run")
        return

    if not interactive:
        for task in tasks:
            print("executing:", task.entry.json)
            task.execute(attempts=attempts, pause=pause, client=client)
            task.write_report(reports_path)

            if task.status == Status.SUCCESS:
                print("success!")
            else:
                print("failed! output:", json.dumps(task.output, indent=2))
                raise ChildProcessError()
    else:
        for task in tasks:
            print("next:", task.entry.json)
            choice = input("(e)xecute or (s)kip? ")
            if choice == "e":
                task.execute(attempts=1, client=client)
                task.write_report(reports_path)

                if task.status == Status.SUCCESS:
                    print("success!")
                else:
                    print("failed! output:", json.dumps(task.output, indent=2))
            else:
                print("skipped")


def log(reports_path: Path = REPORTS_PATH_DEFAULT, md5: str = None, **_) -> None:
    if md5:
        print(reports_path.joinpath(md5).read_text(encoding=ENCODING))
        return

    if not reports_path.exists() or not (files := [path for path in reports_path.iterdir() if path.is_file()]):
        print("no report found")
        return

    for file in sorted(files, key=(get_mtime := lambda path: path.stat().st_mtime)):
        report = json.loads(file.read_text(encoding=ENCODING))
        print(
            file.name,
            datetime.datetime.fromtimestamp(get_mtime(file)).strftime("%c"),
            report.get("status"),
            json.dumps(report.get("entry"))
        )


def main(args: Optional[List[str]] = None) -> None:
    argparser = kivalu.build_argument_parser(description="Minimalist local deployment based on kivalu.")
    argparser.add_argument("-r", "--reports-path", type=Path, default=REPORTS_PATH_DEFAULT, help=f"path to the reports' directory, defaults to {str(REPORTS_PATH_DEFAULT)}", metavar="<path>")
    subparsers = argparser.add_subparsers()

    run_parser = subparsers.add_parser("run", description="", help="")
    run_parser.add_argument("key", nargs="?", default=KEY_DEFAULT, help=f"the script's key, defaults to '{KEY_DEFAULT}'")
    run_parser.add_argument("--attempts", type=int, default=ATTEMPTS_DEFAULT, help=f"maximum number of attempts before reporting a failure, defaults to {ATTEMPTS_DEFAULT}", metavar="<value>")
    run_parser.add_argument("--pause", type=float, default=PAUSE_DEFAULT, help=f"delay in seconds between two attempts, defaults to {PAUSE_DEFAULT}", metavar="<value>")
    run_parser.add_argument("--dry", action="store_true", help="performs a dry run, ie. will stop before executing the tasks")
    run_parser.add_argument("--interactive", action="store_true", help="interactive mode")
    run_parser.set_defaults(command=run)

    log_parser = subparsers.add_parser("log", description="", help="")
    log_parser.add_argument("md5", nargs="?", help="")
    log_parser.set_defaults(command=log)

    args = argparser.parse_args(args)
    args.command(**vars(args))
