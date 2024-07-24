import os
import shutil
import uuid
from abc import ABC
from typing import BinaryIO


class ObjectStorage(ABC):
    def upload(self, file: BinaryIO, filename: str, base_dir: str):
        pass

    def download(self, file_path: str, base_dir: str):
        pass

    def _get_file_identity(self, filename: str) -> (str, str):
        """ Generate a unique ID and filename for the file """
        id = str(uuid.uuid4())
        filename = f"{id}_{filename}"
        return id, filename


class LocalStorage(ObjectStorage):
    def upload(self, file: BinaryIO, filename: str, base_dir: str) -> str:
        """ Save the file to the local storage"""

        obj_id, obj_filename = self._get_file_identity(filename)
        file_path = f"{base_dir}{obj_filename}"

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file, buffer)

        return obj_filename

    def download(self, file_path: str, base_dir: str):
        """ Download the file from the local storage"""
        with open(f"{base_dir}{file_path}", "rb") as file:
            return file.read()