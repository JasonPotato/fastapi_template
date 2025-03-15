"""loads up FastAPI webserver"""

from typing import List, Tuple
import logging
import toml
from fastapi import APIRouter, FastAPI

from dep_injection_example import dep_injection_example
from health import health


def configure_logger():
    """basic setup of logging"""
    verbose = None
    logging.basicConfig(
        filename="service.log",
        encoding="utf-8",
        level=logging.ERROR,
    )
    if verbose:
        logging.getLogger().setLevel(logging.WARNING)


def add_route_to_api(api_app: FastAPI, routes: Tuple[APIRouter, List[str]]):
    """add a new route to the api"""
    router, endpoints = routes
    for endpoint in endpoints:
        print(endpoint)
        api_app.include_router(router, prefix=endpoint)


def get_project_info_from_pyproject() -> Tuple[str, str]:
    """scrape out the name and version of this app from pyproject.toml
    so we can feed it into FastAPI"""
    with open("pyproject.toml", "r", encoding="utf-8") as toml_file_handle:
        pyproject = toml.load(toml_file_handle)
    return pyproject["project"]["name"], pyproject["project"]["version"]


def create_app():
    """define the API app for launching the service"""
    proj_title, proj_version = get_project_info_from_pyproject()
    application = FastAPI(title=proj_title, version=proj_version)

    add_route_to_api(application, health.get_routers())
    add_route_to_api(application, dep_injection_example.get_routers())

    return application


# boot the webserver and wait for requests
configure_logger()
app = create_app()
