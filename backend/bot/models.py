from datetime import datetime
from typing import Optional

from beanie import Document


class User(Document):
    user_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool = True
    language_code: Optional[str]
    is_premium: bool = False
    is_staff: bool = False
    allows_write_to_pm: bool = True
    photo_url: Optional[str]
    date_joined: datetime = datetime.now()
    last_login: Optional[datetime] = None
    updated_at: datetime = datetime.now()
    metadata: dict = {}

    class Settings:
        name = "users"

    def __repr__(self):
        return f"<User {self.user_id} @{self.username}>"

    @classmethod
    async def update_or_create(cls, user_data: dict) -> "User":
        user_id = user_data.get("id")
        if user_id is None:
            raise ValueError("user_data must contain 'id' field")

        user = await cls.find_one(cls.user_id == user_id)

        if user:
            for field, value in user_data.items():
                if field == "id":
                    continue
                if hasattr(user, field):
                    setattr(user, field, value)
            await user.save()

        else:
            user = cls(
                user_id=user_id,
                username=user_data.get("username"),
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                is_active=True,
                language_code=user_data.get("language_code"),
                is_premium=user_data.get("is_premium", False),
                allows_write_to_pm=user_data.get("allows_write_to_pm", True),
                photo_url=user_data.get("photo_url"),
                last_login=datetime.now(),
            )
            await user.insert()

        return user
