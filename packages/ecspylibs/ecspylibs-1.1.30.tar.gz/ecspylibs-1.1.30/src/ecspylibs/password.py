#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.  See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Tue Feb 21 12:10:36 2023 -0500 $
#
# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECSpylibs.git $
#

# Futuristic implementation of commands.  Must be first from/import
# command.

from __future__ import print_function

# Python Standard libraries.
import sys
from dataclasses import dataclass

import autologging
import base64
import logging
import pickle

from Crypto.Cipher import AES
from autologging import logged, traced
from os import urandom


@traced
@logged
@dataclass
class Password:
    """Add, Delete, or return User ID and Password information stored in an application PW file."""
    password_file: str = None

    def __post_init__(self):
        """Set up the Password environment."""

        self.BLOCK_SIZE = 32
        self.PADDING = "{"

        try:
            self.data = pickle.load(open(self.password_file, "rb"))
            self.secret = self.data["secret"]
            self.passwd = self.data["passwd"]
            self.__log.debug("Successfully read the password file '%s'.", self.password_file)
        except Exception as e:
            self.secret = urandom(self.BLOCK_SIZE)
            self.passwd = {}
            self.data = {"secret": self.secret, "passwd": self.passwd}
            self.__log.warning("Password file, '%s', is missing or empty.", self.password_file)
            self.__log.warning("Creating new password file '%s'.", self.password_file)
            self.__log.exception("Exception: '%s'", e)

        self.cipher = AES.new(self.secret)

    def pad(self, passwd: object) -> str:
        """Passwords must be a fixed length, so pad short passwords to the correct len."""

        return passwd + (self.BLOCK_SIZE - len(passwd) % self.BLOCK_SIZE) * self.PADDING

    def update(self) -> bool:
        """Update the PW file."""

        self.data = {"secret": self.secret, "passwd": self.passwd}
        pickle.dump(self.data, open(self.password_file, "wb"))
        return True

    def set(self, user_id: object, passwd: object) -> bool:
        """Add/Modify a User/PW entry in the PW file."""

        self.passwd[user_id] = base64.b64encode(self.cipher.encrypt(self.pad(passwd)))
        self.update()
        return True

    def get(self, user_id: object) -> str:
        """Verify and return, if exists, the PW for the given ID."""

        if user_id in self.passwd:
            user_pw = self.cipher.decrypt(base64.b64decode(self.passwd[user_id])).decode("utf-8").rstrip(self.PADDING)
        else:
            user_pw = ""

        return user_pw

    def delete(self, user_id: object) -> bool:
        """Verify and delete a ID/PW entry in the PW file."""

        if user_id in self.passwd:
            self.__log.warning("Deleting User id '%s'.", user_id)
            del self.passwd[user_id]
            self.update()
        else:
            self.__log.warning("Id '%s' does not exists.", user_id)

        return True

    def list_ids(self) -> bool:
        """Generate a list of User ID in the PW file."""

        print(f"ID", file=sys.stdout)
        user_ids = list(self.passwd)
        user_ids.sort()
        for user_id in user_ids:
            print(f"{user_id:<10}", file=sys.stdout)

        return True

    def list_pws(self) -> bool:
        """Generate a list of User ID and Passwords in the PW file."""

        print(f"{'ID':<15} Password", file=sys.stdout)
        user_ids = list(self.passwd)
        user_ids.sort()
        for user_id in user_ids:
            user_pw = self.get(user_id)
            print(f"{user_id:<15} {user_pw}", file=sys.stdout)

        return True
