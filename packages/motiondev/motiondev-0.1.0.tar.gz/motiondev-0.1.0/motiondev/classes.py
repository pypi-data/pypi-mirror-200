"""
Motiondev

Copyright (c) 2023-present ItsWilliboy

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from .http import Route

if TYPE_CHECKING:
    from .client import Client


__all__ = ("Bot", "User", "Vote")


class Bot:
    """Represents a bot on the Motion Development bot list.

    Attributes
    ----------
    name: `str`
        The bot's name.
    id: `int`
        The bot's ID.
    avatar_url: Optional[`str`]
        The bot's avatar URL (as PNG).
    status: `str`
        The bot's status
    discord: `str`
        Invite URL to the bot's support server.
    invite: `str`
        The bot's OAuth invite URL.
    library: `str`
        The library the bot was built with.
    list_date: `datetime.date`
        The date the bot was listed on the bot list.
    prefix: `str`
        The bot's prefix.
    servers: `int`
        The amount of servers displayed on the bot list.
    site: `str`
        The bot's website
    topics: List[`str`]
        The topics the bot is listed under (max of 3).
    vanity_url: `str`
        The bot's vanity URL.
    owners: `User`
        The bot's owner.
    co_owners: `List[Optional[User]]`

    """

    def __init__(
        self,
        _client: Client,
        _id: str,
        name: str,
        avatar: str,
        status: str,
        co_owners: Optional[List[Dict[str, Any]]],
        discord: str,
        invite: str,
        lib: str,
        list_date,
        owner_id: int,
        owner_name: str,
        prefix: str,
        public_flags: str,
        servers: int,
        site: str,
        tops: List[str],
        vanity_url: str,
        big_desc: str,
        small_desc: str,
    ) -> None:
        self._client = _client
        self._id = _id
        self._name = name
        self._avatar = avatar
        self._status = status
        self._co_owners = co_owners
        self._discord = discord
        self._invite = invite
        self._lib = lib
        self._list_date = list_date
        self._owner_id = owner_id
        self._owner_name = owner_name
        self._prefix = prefix
        self._public_flags = public_flags
        self._servers = servers
        self._site = site
        self._tops = tops
        self._vanity_url = vanity_url
        self._big_desc = big_desc
        self._small_desc = small_desc

    def __str__(self) -> str:
        return self._name

    @property
    def id(self) -> int:
        """`int`: The bot's"""
        return int(self._id)

    @property
    def name(self) -> str:
        """`str`: The bot's name."""
        return self._name

    @property
    def avatar_url(self) -> Optional[str]:
        """Optional[`str`]: The bot's avatar URL (as PNG)."""
        if self._avatar is not None:
            return f"https://cdn.discordapp.com/avatars/{self._id}/{self._avatar}.png"
        return None

    @property
    def status(self) -> str:
        """`str`: The bot's status (not Discord status)."""
        return self._status

    @property
    def discord(self) -> str:
        """`str`: The bot's Discord support server invite URL."""
        return f"https://discord.gg/{self._discord}"

    @property
    def invite(self) -> str:
        """`str`: The bot's invite URL."""
        return self._invite

    @property
    def library(self) -> str:
        """`str`: The library the bot is built with."""
        return self._lib

    @property
    def list_date(self) -> Optional[date]:
        """`datetime.date`: The date the bot was listed on the bot list. `None` if the date wasn't supplied"""
        try:
            return datetime.strptime(self._list_date, "%Y-%m-%d").date()
        except ValueError:
            return None

    @property
    def prefix(self) -> str:
        """`str`: The bot's prefix."""
        return self._prefix

    @property
    def servers(self) -> int:
        """`int`: The bot's amount of servers posted on the bot list."""
        return self._servers

    @property
    def site(self) -> str:
        """`str`: The bot's website."""
        return self._site

    @property
    def public_flags(self) -> int:
        """`str`: The bot's public flags."""
        return int(self._public_flags)

    @property
    def topics(self) -> List[str]:
        """List[`str`]: The topics the bot is listed under (max of 3)."""
        return self._tops

    @property
    def vanity_url(self) -> str:
        """`str`: The bot's vanity URL."""
        return self._vanity_url

    @property
    def big_description(self) -> str:
        """`str`: The bot's big description."""
        return self._big_desc

    @property
    def small_description(self) -> str:
        """`str`: The bot's small description."""
        return self._small_desc

    @property
    def owner(self) -> User:
        """`User`: The bot's owner"""
        return User(id=self._owner_id, username=self._owner_name)

    @property
    def co_owners(self) -> List[Optional[User]]:
        """List[Optional[`User`]]: The bot's co-owners"""
        return self._get_co_owners()

    def _get_co_owners(self) -> List[Optional[User]]:
        users = []
        if self._co_owners is not None:
            for i in self._co_owners:
                user = User(id=i.get("id"), username=i.get("username"))  # type: ignore
                users.append(user)

        return users

    async def update(self, *, servers: int) -> Bot:
        """|coro|

        Updates the bot on the bot list.

        Parameters
        ----------
        servers: `int`

        Returns
        -------
        `Bot`: The bot with the updated parameters.
        """
        route = Route("POST", "/bots/{bot_id}/stats", bot_id=self._id)
        await self._client._http.request(route, json={"guilds": servers}, headers={"Content-Type": "application/json"})
        self._servers = servers
        return self

    async def get_votes(self) -> List[Optional[Vote]]:
        """|coro|

        Gets all of the bots votes on the bot list.

        Returns
        -------
        List[`Vote`]: A list of all the votes.
        """
        route = Route("GET", "/bots/{bot_id}/votes", bot_id=self._id)
        resp = await self._client._http.request(route)

        if resp is None:
            return []

        votes: List[Optional[Vote]] = []
        for i in resp:
            vote = Vote(_id=i.get("id"), vote_time=i.get("vote-time"), user=i.get("user"), user_name=i.get("user_name"))
            votes.append(vote)

        return votes


class User:
    """Represents a user on the bot list

    Attributes
    ----------
    id: `int`
        The user's ID.
    username: `str`
        The user's username.
    """

    def __init__(self, id: int, username: str) -> None:
        self._id = id
        self._username = username

    def __repr__(self) -> str:
        return f"<User id={self._id} username={self._username}>"

    def __str__(self) -> str:
        return self._username

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self) -> str:
        return self._username


class VoteUser(User):
    def __init__(self, id: int, username) -> None:
        super().__init__(id, username)

    def __repr__(self) -> str:
        return f"<User id={self._id}>"

    @property
    def username(self) -> NotImplementedError:
        raise NotImplementedError("It looks like this feature has not been implemented correctly in the API yet.")


class Vote:
    def __init__(self, _id: int, vote_time: str, user: bool, user_name: str) -> None:
        self._id = _id
        self._vote_time = vote_time
        self._user = user
        self._user_name = user_name

    def __repr__(self) -> str:
        return f"<Vote id={self._id}, vote_time={self._vote_time}, user={repr(self.user)}"

    @property
    def user(self) -> Optional[User]:
        """`Optional[User]`: The voter. Is `None` if the vote is a placeholder."""
        if self._user:
            return VoteUser(id=self._id, username=self._user_name)

    @property
    def vote_time(self) -> Optional[datetime]:
        """`datetime.datetime`: The date & time when the vote was added. `None` if parsing failed."""
        try:
            return datetime.strptime(self._vote_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None
