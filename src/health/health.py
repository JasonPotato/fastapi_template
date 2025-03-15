"""Rest API to check on the health of the service"""

from typing import List, Tuple
from fastapi import APIRouter
from pydantic import BaseModel

from utilities import constants


class Health(BaseModel):
    """Model describing the health of the service"""

    status: str


router = APIRouter(tags=["health"])


def get_routers() -> Tuple[APIRouter, List[str]]:
    """return a tuple of the routers this api provides and the versions it maps to"""
    routers = constants.LATEST_API_PREFIXES
    return router, routers


@router.get("/health", response_model=Health)
async def check_health() -> Health:
    """Print Healthy if the service is capable of doing so. Not being able to is
    an indicator that something is really wrong."""

    results_dict = {"status": "Healthy!"}

    return Health.model_validate(results_dict)
