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


class MotionDevException(Exception):
    """Base exception for the motiondev package"""

    pass


class HTTPException(MotionDevException):
    """Exception that is raised when an HTTP request operation fails."""

    pass


class Forbidden(HTTPException):
    """Exception that is raised when status code 403 occurs.

    Subclass of :exc:`HTTPException`
    """

    pass


class NotFound(HTTPException):
    """Exception that is raised when status code 404 occurs.

    Subclass of :exc:`HTTPException`
    """

    pass


class ServerError(HTTPException):
    """Exception that is raised when status code in the 500 range occurs.

    Subclass of :exc:`HTTPException`
    """

    pass
