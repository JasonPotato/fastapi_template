"""Rest API to check on the health of the service"""

from typing import Annotated, List, Tuple
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from utilities import constants


class DependencyInjectionExample(BaseModel):
    """Model showing how to do dependency injection"""

    message: str


router = APIRouter(tags=["dependency-injection-example"])


def get_routers() -> List[Tuple[APIRouter, List[str]]]:
    """return a tuple of the routers this api provides and the versions it maps to"""
    routers = constants.LATEST_API_PREFIXES
    return [(router, routers)]


def get_message_to_send(message_to_return: int) -> str:
    """This is the behavior we want to inject, and will mock out in our tests"""
    possible_responses = ["a message we want to override"]
    return possible_responses[message_to_return]


@router.get("/dependency-injection-example", response_model=DependencyInjectionExample)
async def inject_behavior_here(
    message_to_print: Annotated[str, Depends(get_message_to_send)],
) -> DependencyInjectionExample:
    """Take in a number and print out the message associated with that list
    index from a pre-canned set of messages. Something easy to override and
    make behave differently in a test."""

    results_dict = {"message": message_to_print}

    return DependencyInjectionExample.model_validate(results_dict)
