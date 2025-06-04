"""Rest API to check on the health of the service"""

from typing import Annotated, Dict, List, Tuple

import uuid
import logging
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from utilities import constants


class Secret(BaseModel):
    """Model describing a secret to share"""

    secret_value: str


class SecretRetrievalUrl(BaseModel):
    """Model describing the path a secret is available at"""

    uuid: str
    url: str


secrets_in_flight: Dict[str, Secret] = {}

api_router = APIRouter(tags=["api_secret"])
frontend_router = APIRouter(tags=["frontend"])


def get_routers() -> List[Tuple[APIRouter, List[str]]]:
    """return a tuple of the routers this api provides and the versions it maps to"""
    routers = constants.LATEST_API_PREFIXES
    return [(api_router, routers), (frontend_router, [""])]


async def add_secret(secret_value: str):
    """create a new secret, returning the uuid at which the secret value can be found"""
    secret_uuid = str(uuid.uuid4())
    secrets_in_flight[secret_uuid] = Secret.model_validate(
        {"secret_value": secret_value}
    )

    logging.info("added secret: %s", secret_uuid)

    return SecretRetrievalUrl.model_validate({"uuid": secret_uuid, "url": secret_uuid})


@api_router.post("/add-secret", response_class=HTMLResponse)
async def add_secret_api(request: Request, secret_value: Annotated[Secret, Form()]):
    """create a new secret, returning the url at which that secret can be found

    if called from the contet of the frontend, return a rendered html template.
    if called from the conted of the rest api, return a json object"""
    secret_retrieval_url = await add_secret(secret_value.secret_value)

    if request.headers.get("hx-request"):
        return constants.templates.TemplateResponse(
            request=request,
            name="add-secret/secret-url.html.j2",
            context={"secret": secret_retrieval_url.uuid},
        )
    return JSONResponse(content=jsonable_encoder(secret_retrieval_url))


async def get_secret(secret_uuid: str):
    """get a secret value and remove it from storage so it cannot be accessed again"""
    if not secret_uuid in secrets_in_flight:
        raise HTTPException(status_code=404, detail="Secret not found!")
    return secrets_in_flight.pop(secret_uuid)


@api_router.get("/get-secret/{secret_uuid}", response_model=Secret)
async def get_secret_api(secret_uuid: str) -> Secret:
    """take a secret uuid, return the corresponding secret value, and prevent
    further reading of that secret"""
    return await get_secret(secret_uuid)


@frontend_router.get("/get-secret/{secret_uuid}", response_class=HTMLResponse)
async def get_secret_frontend(request: Request, secret_uuid: str):
    """take a secret uuid, return html to the user showing them the value, and prevent
    further reading of that secret"""
    secret = await get_secret(secret_uuid)
    return constants.templates.TemplateResponse(
        request=request,
        name="get-secret/index.html.j2",
        context={"secret_value": secret.secret_value},
    )
