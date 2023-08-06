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

import json
from typing import Any, Dict, Union
from urllib.parse import quote

import aiohttp
from aiohttp import ClientResponse

from .errors import Forbidden, HTTPException, NotFound

# (heavily) Inspired by discord.py (by Rapptz) package


async def json_or_text(response: ClientResponse) -> Union[Dict[str, Any], str]:
    text = await response.text()
    try:
        if response.headers["content-type"] == "application/json":
            return json.loads(text)

    except KeyError:
        pass

    return text


class Route:
    BASE: str = "https://motiondevelopment.top/api/v1.2"

    def __init__(self, method: str, path: str, **parameters: Any) -> None:
        self.method: str = method
        self.path: str = path

        url = self.BASE + self.path
        if parameters:
            url = url.format_map({k: quote(v) if isinstance(v, str) else v for k, v in parameters.items()})

        self.url: str = url


class HTTPClient:
    def __init__(self, token: str) -> None:
        self.token: str = token
        self._session: aiohttp.ClientSession = aiohttp.ClientSession()

    async def request(self, route: Route, **kwargs: Any) -> Any:
        if self._session.closed:
            raise Exception("Session is closed")

        url = route.url
        method = route.method

        headers: Dict[str, str] = {
            "User-Agent": "MotionDev Python API Wrapper",
        }

        headers["key"] = self.token

        if kwargs.get("headers"):
            kwargs["headers"] = headers | kwargs["headers"]
        else:
            kwargs["headers"] = headers

        async with self._session.request(method, url, **kwargs) as response:
            data = await json_or_text(response)

            if 300 > response.status >= 200:
                return data

            elif response.status == 403:
                raise Forbidden(data)

            elif response.status == 404:
                raise NotFound(data)

            else:
                raise HTTPException(response, data)
