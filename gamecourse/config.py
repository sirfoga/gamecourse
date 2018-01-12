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


""" Server config """

import os

APP_NAME = "gamecourse"
APP_HOST = "0.0.0.0"  # todo in cli
APP_PORT = 1729
THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))
ROOT_FOLDER = os.path.dirname(THIS_FOLDER)
UPLOAD_FOLDER = os.path.join(
    ROOT_FOLDER,
    "uploads"
)
TEMPLATES_FOLDER = os.path.join(
    ROOT_FOLDER,
    "templates"
)
UPLOAD_TEMPLATE = os.path.join(
    TEMPLATES_FOLDER,
    "upload.html"
)
ALLOWED_EXTENSIONS = {"dat"}  # allow only these extensions
