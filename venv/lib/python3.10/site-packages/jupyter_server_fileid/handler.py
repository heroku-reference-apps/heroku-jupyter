from jupyter_server.auth.decorator import authorized
from jupyter_server.base.handlers import APIHandler
from tornado import web
from tornado.escape import json_encode

from .manager import BaseFileIdManager


class BaseHandler(APIHandler):
    auth_resource = "contents"

    @property
    def file_id_manager(self) -> BaseFileIdManager:
        return self.settings.get("file_id_manager")


class FileIDHandler(BaseHandler):
    """A handler that fetches a file ID from the file path."""

    @web.authenticated
    @authorized
    def get(self):
        try:
            path = self.get_argument("path")
            id = self.file_id_manager.get_id(path)
            # If the path cannot be found, it returns None. Raise a helpful
            # error to the client.
            if id is None:
                raise web.HTTPError(
                    404,
                    log_message=f"The ID for file, {path}, could not be found.",
                    reason=f"The ID for file, {path}, could not be found.",
                )
            self.write(json_encode({"id": id, "path": path}))
        except web.MissingArgumentError:
            raise web.HTTPError(
                400, log_message="'path' parameter was not provided in the request."
            )


class FilePathHandler(BaseHandler):
    """A handler that fetches a file path from the file ID."""

    @web.authenticated
    @authorized
    def get(self):
        try:
            id = self.get_argument("id")
            path = self.file_id_manager.get_path(id)
            # If the ID cannot be found, it returns None. Raise a helpful
            # error to the client.
            if path is None:
                error_msg = f"The path for file, {id}, could not be found."
                raise web.HTTPError(
                    404,
                    log_message=error_msg,
                    reason=error_msg,
                )
            self.write(json_encode({"id": id, "path": path}))
        except web.MissingArgumentError:
            raise web.HTTPError(400, log_message="'id' parameter was not provided in the request.")
