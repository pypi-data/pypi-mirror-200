#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.  See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Fri Feb 17 12:47:46 2023 -0500 $
#
# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECSpylibs.git $
#

# Futuristic implementation of commands.  Must be first from/import
# command.

from __future__ import print_function

# Home grown libraries.

from ecspylibs.password import Password

# Python Standard libraries.

import autologging
import logging
import requests
import sys

from autologging import logged, traced


@traced
@logged
class CheckService:
    """Verify if a given service has status up, maintenance, or is invalid."""

    def __init__(self, cherwell_user: object, passwd_file: object) -> None:
        """Setup the CheckService environment."""

        self.results_count = None
        self.check_service_url = None
        self.service_name = None
        self.cherwell_user = cherwell_user
        self.passwd_file = passwd_file
        self.count = 0

        self.cherwell_pw_data = Password(self.passwd_file)

        self.cherwell_pw = self.cherwell_pw_data.get(self.cherwell_user)
        self.client_Id = self.cherwell_pw_data.get("client_Id")
        self.bus_obj_Id = self.cherwell_pw_data.get("bus_obj_Id")
        self.search_Id = self.cherwell_pw_data.get("search_Id")

        del self.cherwell_pw_data

        self.__log.debug("User            : '%s'", self.cherwell_user)
        self.__log.debug("Pass            : '%s'", self.cherwell_pw)
        self.__log.debug("bus_obj_Id      : '%s'", self.bus_obj_Id)
        self.__log.debug("client_Id       : '%s'", self.client_Id)
        self.__log.debug("search_Id       : '%s'", self.search_Id)

        self.get_token = {
            "grant_type": "password",
            "client_id": self.client_Id,
            "username": self.cherwell_user,
            "password": self.cherwell_pw,
        }

        del self.cherwell_pw

        # There are two types of Cherwell searches: searchid and searchname.
        # Create both and then set self.search_API to the one being used.

        self.cherwell_fields_search_id = {
            "URI": "https://csm.wayne.edu/CherwellAPI",
            "API": "api/V1/getsearchresults/association",
            "busObjId": self.bus_obj_Id,
            "scope": "scope/Global",
            "owner": "scopeowner/(None)",
            "search": "searchid/%s?searchTerm=%%(searchTerm)s" % self.search_Id,
        }

        self.cherwell_fields_search_name = {
            "URI": "https://csm.wayne.edu/CherwellAPI",
            "API": "api/V1/getsearchresults/association",
            "busObjId": self.bus_obj_Id,
            "scope": "scope/Global",
            "owner": "scopeowner/(None)",
            "search": "searchname/HappeningNow%(searchTerm)s"
        }

        self.login_api = "%(URI)s/token?auth_mode=Internal" % self.cherwell_fields_search_id

        self.search_name_api = "%(URI)s/%(API)s/%(busObjId)s/%(scope)s/%(owner)s/%(search)s" % self.cherwell_fields_search_name
        self.search_id_API = "%(URI)s/%(API)s/%(busObjId)s/%(scope)s/%(owner)s/%(search)s" % self.cherwell_fields_search_id

        # Set self.search_API to the one being used from above.

        self.search_api = self.search_name_api

        self.__log.debug("Login API       : '%s'", self.login_api)
        self.__log.debug("Search Name API : '%s'", self.search_name_api)
        self.__log.debug("Search ID API   : '%s'", self.search_id_API)
        self.__log.debug("Search API      : '%s'", self.search_api)

        for self.i in range(1, 9):
            try:
                self.__log.debug("Call %d login_API.", self.i)
                self.auth_r = requests.post(self.login_api, data=self.get_token)
                self.__log.debug("Call %d to login_API successful.", self.i)
                break
            except Exception as e:
                self.__log.critical("Error attempt number %d from call to login_API.", self.i)
                self.__log.exception("Exception: '%s'.", e)
        else:
            self.__log.error("Call to login_API unsuccessful.")
            self.external_errors = True
            self.internal_errors = True
            return

        for self.i in range(1, 9):
            try:
                self.__log.debug("Call %d raise_for_status.", self.i)
                self.auth_r.raise_for_status()
                self.__log.debug("Call %d to raise_for_status successful.", self.i)
                break
            except Exception as e:
                self.__log.critical("Error attempt number %d from self.auth_r.raise_for_status().", self.i)
                self.__log.exception("Exception: '%s'.", e)
        else:
            self.__log.error("Call to raise_for_status unsuccessful.")
            self.external_errors = True
            self.internal_errors = True
            return

        if "access_token" in self.auth_r.json():
            self.token = self.auth_r.json()["access_token"]
        else:
            self.__log.critical('self.auth_r.json()["access_token"] is missing or invalid.')
            self.external_errors = True
            self.internal_errors = True
            return

        if "token_type" in self.auth_r.json():
            self.token_type = self.auth_r.json()["token_type"]
        else:
            self.__log.critical('self.auth_r.json()["token_type"] is missing or invalid.')
            self.external_errors = True
            self.internal_errors = True
            return

        self.auth_header = {
            "Authorization": "%s %s" % (self.token_type, self.token),
            "Accept": "application/json",
        }

    def check_service(self, service_name: object) -> object:
        """Verify if a given service has status up, maintenance, or is invalid.

    Return codes:
        0 : Service should be up.  Continue with check.
        1 : Service is in maintenance.  Skip check.
        2 : Error calling Cherwell.  Check error log for details.
        3 : Error returning service status from Cherwell.  Check error log for details.
        4 : Error processing service status retrieved from Cherwell.  Check error log for details.
    """

        self.service_name = service_name
        self.check_service_url = self.search_api % {"searchTerm": self.service_name}

        self.__log.debug("Service Name = '%s'", self.service_name)
        self.__log.debug("URL = '%s'", self.check_service_url)

        for self.i in range(1, 9):
            try:
                self.__log.debug("Call %d self.check_service_URL.", self.i)
                self.r = requests.get(self.check_service_url, headers=self.auth_header)
                self.__log.debug("Call %d to self.check_service_URL successful.", self.i)
                break
            except Exception as e:
                self.__log.critical(
                    "Error attempt number %d from requests.get(self.check_service_URL, headers=self.auth_header).",
                    self.i)
                self.__log.exception("Exception: '%s'.", e)
        else:
            self.__log.error("Call to self.check_service_URL unsuccessful.")
            self.external_errors = True
            self.internal_errors = True
            return 2

        for self.i in range(1, 9):
            try:
                self.__log.debug("Call %d to self.r.raise_for_status.", self.i)
                self.r.raise_for_status()
                self.__log.debug("Call %d to self.r.raise_for_status successful.", self.i)
                break
            except Exception as e:
                self.__log.critical("Error attempt number %d from self.r.raise_for_status().", self.i)
                self.__log.exception("Exception: '%s'.", e)
        else:
            self.__log.error("Call to self.r.raise_for_status unsuccessful.")
            self.external_errors = True
            self.internal_errors = True
            return 3

        if "totalRows" in self.r.json():
            self.results_count = self.r.json()["totalRows"]
            self.__log.debug("Count = '%s'", self.results_count)
        else:
            self.__log.critical('self.r.json()["totalRows"] is missing or invalid.')
            self.external_errors = True
            self.internal_errors = True
            return 4

        return self.results_count
