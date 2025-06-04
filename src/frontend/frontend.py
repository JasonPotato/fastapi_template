"""Rest API to check on the health of the service"""

from typing import List, Tuple
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from utilities import constants


router = APIRouter(tags=["frontend"])


def get_routers() -> List[Tuple[APIRouter, List[str]]]:
    """return a tuple of the routers this api provides and the versions it maps to"""
    return [(router, [""])]


@router.get("/", response_class=HTMLResponse)
async def get_homepage(request: Request):
    """Return the homepage html to the caller."""
    return constants.templates.TemplateResponse(request=request, name="index.html.j2")
