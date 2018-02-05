# !/usr/bin/python3
# coding: utf_8

# Copyright 2017-2018 Stefano Fogarollo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


""" Models and data structure """

import json
import os
import uuid

from validate_email import validate_email

from gamecourse.config import UPLOAD_FOLDER
from gamecourse.utils import can_upload


class XMLHttpRequest:
    """ Parse XMLHttpRequest """

    def __init__(self, req):
        """
        :param req: Request
            Client request
        """

        self.data = req.data
        self.files = req.files
        self.form = req.form
        self.meta_data = None
        self.upload_folder = None

        self._parse()
        self._create_upload_folder()

    def _parse(self):
        """
        :return: void
            Parses and prettify data
        """

        self._parse_files()
        self._parse_form()
        self._parse_data()

    def _parse_files(self):
        """
        :return: void
            Parse and prettify raw data files
        """

        files = {}
        for filename in self.files:
            files[filename] = self.files[filename]
        self.files = files

    def _parse_form(self):
        """
        :return: void
            Parse and prettify raw data form
        """

        form = {}
        for entry in self.form:
            form[entry] = self.form[entry]
        self.form = form

    def _parse_data(self):
        """
        :return: void
            Sets metadata
        """

        self.meta_data = self.form["meta-data"] or None
        self.meta_data = json.loads(self.meta_data)
        self.meta_data["PhysicalProprieties"] = {
            "n": self.meta_data["PhysicalProprieties"][0],
            "nh": self.meta_data["PhysicalProprieties"][1],
            "g": self.meta_data["PhysicalProprieties"][2],
            "u": self.meta_data["PhysicalProprieties"][3],
            "z": self.meta_data["PhysicalProprieties"][4],
            "f": self.meta_data["PhysicalProprieties"][5],
            "a": self.meta_data["PhysicalProprieties"][6],
        }

    def _create_upload_folder(self):
        """
        :return: void
            Create folder where can upload data
        """

        self.upload_folder = self.get_upload_folder()
        os.makedirs(self.upload_folder)

    def is_good_request(self):
        """
        :return: bool
            True iff request is written in valid format
        """

        if len(self.files) != 2:
            return False

        for _, file in self.files.items():
            if not can_upload(file.filename):
                return False

        if len(self.meta_data) != 4:
            return False

        if not validate_email(self.meta_data["Email"]):
            return False

        if len(self.meta_data["PhysicalProprieties"]) != 7:
            return False

        return True

    def write_data_to_file(self):
        """
        :return: void
            Saves meta data to file
        """

        output_file = os.path.join(self.upload_folder, "data.json")
        with open(output_file, "w") as out:
            json.dump(
                self.meta_data,
                out,
                indent=4, sort_keys=True  # pretty print
            )

    @staticmethod
    def get_upload_folder():
        """
        :return: str
            Path to folder than can be used to store data
        """

        return os.path.join(UPLOAD_FOLDER, str(uuid.uuid4()))

    def __str__(self):
        out = "*** files: " + str(self.files) + "\n"
        out += "*** meta data: " + str(self.meta_data) + "\n"
        out += "*** folder: " + str(self.upload_folder) + "\n"
        return out
