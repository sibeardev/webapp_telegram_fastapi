from datetime import datetime
from typing import Dict, Optional

from beanie import Document


class User(Document):
    user_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool = True
    language_code: Optional[str]
    is_premium: bool = False
    allows_write_to_pm: bool = True
    photo_url: Optional[str]
    date_joined: datetime = datetime.now()
    last_login: Optional[datetime] = None
    updated_at: datetime = datetime.now()
    metadata: Dict = {}

    class Settings:
        name = "users"

    def __repr__(self):
        return f"<User {self.user_id} @{self.username}>"
