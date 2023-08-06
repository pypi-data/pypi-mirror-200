#!/usr/bin/env python3.6
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

# Python Standard libraries.

import autologging
import logging
import mailbox
import sys
import zipfile

from autologging import logged, traced
from os.path import abspath, basename, dirname, isabs, isdir, isfile, ismount, join, normpath


@traced
@logged
class ParseEmail:
    """ blah """

    def __init__(self, mailbox_file: object, data_dir: object) -> None:
        """ blah """

        self.data = None
        self.file_name = None
        self.part_type = None
        self.msg_subject = None
        self.msg = None
        self.init = True

        if not isfile(mailbox_file) or not isdir(data_dir):
            self.init = False
            self.__log.warning(f"One or more parameters are missing or invalid.")

            if not isfile(mailbox_file):
                self.__log.critical(f"File '{mailbox_file}' does not exist.")

            if not isdir(data_dir):
                self.__log.critical(f"Directory '{data_dir}' does not exist.")

            self.__log.warning(f"Aborting call to ParseEmail.__init__({mailbox_file}, {data_dir}).")
        else:
            self.mailbox_file = mailbox_file
            self.data_dir = data_dir
            self.mbox = None

    def open_mbox(self) -> object:
        """ blah """

        self.__log.debug(f"Opening mailbox file '{self.mailbox_file}'.")
        self.mbox = mailbox.mbox(self.mailbox_file)
        return True

    def get_attachments(self, subject: object, attachment_file: object) -> object:
        """ blah """

        self.__log.info(f"Get attachments with subject '{subject}' and file name '{attachment_file}'.")

        for self.key in self.mbox.keys():
            self.__log.info(f"Processing message {self.key}.")

            self.msg = self.mbox[self.key]
            self.msg_subject = self.msg["Subject"]

            self.__log.info(f"Message {self.key} with subject '{self.msg_subject}'.")

            if self.msg_subject == subject:
                self.__log.info(f"Message {self.key} has good subject '{subject}'.")

                for self.part in self.msg.walk():
                    self.__log.info(f"Walking through message {self.key}.")

                    self.part_type = self.part.get_content_disposition()

                    self.__log.info(f"Message {self.key} has content disposition '{self.part_type}'.")

                    if self.part_type == "attachment":
                        self.__log.info(f"Message {self.key} has good content disposition 'attachment'.")

                        self.file_name = self.part.get_filename()

                        self.__log.info(f"Message {self.key} has file name '{self.file_name}'")

                        if self.file_name == attachment_file:
                            self.__log.info(f"Message {self.key} has good file name '{attachment_file}'.")

                            self.__log.info(f"Extract attachment file name '{attachment_file}' from message {self.key}.")

                            self.data = self.part.get_payload(decode=True)

                            self.__log.info(
                                f"Storage attachment file '{attachment_file}' into directory '{self.data_dir}'.")

                            with open(normpath(join(self.data_dir, self.file_name)), "wb") as fp:
                                fp.write(self.data)

                            self.__log.info(
                                f"Unzip attachment file name '{attachment_file}' into directory '{self.data_dir}'")

                            with zipfile.ZipFile(normpath(join(self.data_dir, self.file_name)), "r") as zip_ref:
                                zip_ref.extractall(self.data_dir)

                            self.__log.info(
                                f"Attachment file '{attachment_file}' unzipped into directory '{self.data_dir}'.")

                        else:
                            self.__log.warning(f"Invalid attachment file name '{self.file_name}'.")
                    else:
                        self.__log.info(f"Skipping content disposition type '{self.part_type}'.")
            else:
                self.__log.warning(f"Skipping email with subject '{self.msg_subject}'.")

            self.mbox.lock()
            self.mbox.discard(self.key)
            self.mbox.flush()
            self.mbox.unlock()

        return True

    def close_mbox(self) -> object:
        """ blah """

        self.__log.info(f"Close mailbox file '{self.mailbox_file}'.")

        if self.mbox:
            self.mbox.close()
            self.mbox = None

        return True
