import logging

from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi.responses import Response
from pydantic import BaseModel
from pymongo import ReturnDocument
from starlette.exceptions import HTTPException

from app.db.mongo import get_db_collection
from app.dependencies import get_token_header
from app.models.users import UpdateUserModel, UserCollection, UserModel
from app.settings import STATIC_ROOT, TEMPLATES

logger = logging.getLogger(__file__)

router = APIRouter(
    # dependencies=[Depends(get_token_header)],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.get(
    "/",
    response_description="List all students",
    response_model=UserCollection,
    response_model_by_alias=False,
)
async def get_users():
    try:
        return UserCollection(
            users=await get_db_collection("users").find().to_list(1000)
        )
    except Exception as e:
        logging.error(f"An error occurred: {e}")


@router.post(
    "/",
    response_description="Add new user",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_user(user: UserModel = Body(...)):
    new_user = await get_db_collection("users").insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = await get_db_collection("users").find_one(
        {"_id": new_user.inserted_id}
    )

    return created_user


@router.get(
    "/{user_id}",
    response_description="Get a single user",
    response_model=UserModel,
    response_model_by_alias=False,
)
async def get_user(user_id: int, request: Request):
    if (
        user := await get_db_collection("users").find_one({"user_id": user_id})
    ) is not None:
        template = "user.html"
        context = {"request": request, "user": user}

        return TEMPLATES.TemplateResponse(template, context)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found"
    )


@router.put(
    "/{user_id}",
    response_description="Update a user",
    response_model=UpdateUserModel,
    response_model_by_alias=False,
)
async def update_user(user_id: int, user: UserModel = Body(...)):
    user = {
        key: value
        for key, value in user.model_dump(by_alias=True).items()
        if value is not None
    }
    if len(user) >= 1:
        update_result = await get_db_collection("users").find_one_and_update(
            {"user_id": user_id},
            {"$set": user},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found",
            )

    # The update is empty, but we should still return the matching document:
    if (
        existing_user := await get_db_collection("users").find_one({"user_id": user_id})
    ) is not None:
        return existing_user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found"
    )


@router.delete("/{user_id}", response_description="Delete a user")
async def delete_user(user_id: int):
    delete_result = await get_db_collection("users").delete_one({"user_id": user_id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found"
    )
