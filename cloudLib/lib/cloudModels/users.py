from cloudLib._RequestHandlerInstance import RequestHandler
from typing import Optional


class Users:
    """Handler for the users in a sphere"""

    def __init__(self, sphere_id: str) -> None:
        """Init"""
        self.users = {}
        self.sphere_id = sphere_id

    async def sync(self) -> None:
        """Get the users for this sphere from the cloud"""
        user_data = await RequestHandler.get('Spheres', 'users', model_id=self.sphere_id)
        for role, users in user_data.items():
            for user in users:
                self.users[user['id']] = User(user, role)

    def find_by_first_name(self, first_name: str) -> list:
        """Search for a user by first name and return a list with the users found"""
        found_users = []
        for user in self.users.values():
            if first_name == user.first_name:
                found_users.append(user)

        return found_users

    def find_by_last_name(self, last_name: str) -> list:
        """Search for a user by last name and return a list with the users found"""
        found_users = []
        for user in self.users.values():
            if last_name == user.last_name:
                found_users.append(user)

        return found_users

    def find_by_id(self, user_id) -> object or None:
        """Search for a user by id and return crownstone object if found"""
        return self.users[user_id]


class User:
    """Represents a user in a sphere"""

    def __init__(self, data: dict, role: str) -> None:
        self.data = data
        self.role = role

    @property
    def first_name(self) -> str:
        return self.data['firstName']

    @property
    def last_name(self) -> str:
        return self.data['lastName']

    @property
    def email(self) -> str:
        return self.data['email']

    @property
    def cloud_id(self) -> str:
        return self.data['id']

    @property
    def email_verified(self) -> bool:
        return self.data['emailVerified']