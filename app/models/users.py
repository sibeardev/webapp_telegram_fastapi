from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserModel(BaseModel):
    """
    UserModel class represents a user model with the following attributes:

    Attributes:
        id (Optional[PyObjectId]): The unique identifier for the user. Defaults to None.
        user_id (int): The user's ID.
        username (str): The user's username.
        photo_url (Optional[str]): The URL of the user's photo. Defaults to None.
        model_config (ConfigDict): Configuration settings for the model.

    """

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: int = Field(...)
    username: str = Field(...)
    photo_url: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "username": "Jane Doe",
                "user_id": 12345678,
                "photo_url": "https://example.com/photo.jpg",
            }
        },
    )


class UpdateUserModel(BaseModel):
    """
    A Pydantic model class for updating user information.

    Attributes:
        username (str): The username of the user. Defaults to None.
        photo_url (Optional[str]): The URL of the user's photo. Defaults to None.
        model_config (ConfigDict): Configuration settings for the model.
    """

    username: str = None
    photo_url: Optional[str] = None

    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "username": "Jane Doe",
                "photo_url": "https://example.com/photo.jpg",
            }
        },
    )


class UserCollection(BaseModel):
    """
    A container holding a list of `UserModel` instances.

    """

    users: List[UserModel]
