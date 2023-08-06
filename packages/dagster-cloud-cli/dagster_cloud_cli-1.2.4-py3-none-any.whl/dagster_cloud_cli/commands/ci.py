# CI/CD agnostic commands that work with the current CI/CD system

import json
import logging
import os
import sys
from typing import Any, Dict

from typer import Typer

from . import metrics

app = Typer(hidden=True, help="CI/CD agnostic commands")
from dagster_cloud_cli.core.pex_builder import code_location, github_context
from dagster_cloud_cli.types import CliEventTags


@app.command(help="Print json information about current CI/CD environment")
def inspect(project_dir: str):
    project_dir = os.path.abspath(project_dir)
    source = metrics.get_source()
    info = {"source": str(source), "project-dir": project_dir}
    if source == CliEventTags.source.github:
        info.update(load_github_info(project_dir))
    print(json.dumps(info))


def load_github_info(project_dir: str) -> Dict[str, Any]:
    event = github_context.get_github_event(project_dir)
    return {
        "git-url": event.commit_url,
        "commit-hash": event.github_sha,
    }


@app.command(
    help=(
        "Print the branch deployment name (or nothing) for the current context. Creates a new"
        " branch deployment if necessary. Requires DAGSTER_CLOUD_URL and DAGSTER_CLOUD_API_TOKEN"
        " environment variables."
    )
)
def branch_deployment(project_dir: str):
    source = metrics.get_source()
    if source == CliEventTags.source.github:
        event = github_context.get_github_event(project_dir)
        url = os.environ["DAGSTER_CLOUD_URL"]
        api_token = os.environ["DAGSTER_CLOUD_API_TOKEN"]
        deployment_name = code_location.create_or_update_branch_deployment_from_github_context(
            url, api_token, event
        )
        print(deployment_name)
    else:
        logging.error("branch-deployment not supported for %s", source)
        sys.exit(1)
