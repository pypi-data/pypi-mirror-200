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

from .classes import Bot
from .http import HTTPClient, Route


class Client:
    """Represents a client that sends requests to the motiondevelopment.top API.

    Parameters
    ----------

    token: `str`: Your Motion Development API token.

    """

    def __init__(self, token: str) -> None:
        self._token: str = token
        self._http = HTTPClient(token)

    async def __aenter__(self) -> Client:
        return self

    async def __aexit__(self, *_) -> None:
        await self._http._session.close()

    async def get_bot(self, bot_id: int) -> Bot:
        route = Route("GET", "/bots/{bot_id}", bot_id=bot_id)
        res = await self._http.request(route)
        return Bot(
            _client=self,
            _id=res.get("bot_id"),
            name=res.get("username"),
            avatar=res.get("avatar"),
            status=res.get("bot_status"),
            co_owners=res.get("co_owners"),
            discord=res.get("discord"),
            invite=res.get("invite"),
            lib=res.get("lib"),
            list_date=res.get("list_date"),
            owner_id=res.get("owner_id"),
            owner_name=res.get("owner_name"),
            prefix=res.get("prefix"),
            public_flags=res.get("public_flags"),
            servers=res.get("servers"),
            site=res.get("site"),
            tops=res.get("tops"),
            vanity_url=res.get("vanity_url"),
            big_desc=res.get("Big_desc"),
            small_desc=res.get("Small_desc"),
        )
