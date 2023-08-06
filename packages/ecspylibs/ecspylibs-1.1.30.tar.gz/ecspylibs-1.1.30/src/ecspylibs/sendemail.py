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
import smtplib

from autologging import logged, traced
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from pathlib import Path


@traced
@logged
class SendEmail:
    """ blah """

    def __init__(self) -> None:
        """ blah """

        self.part = None
        self.msg = None
        self.smtp = None
        self.f = None


    def send_email(self,
                   from_id: object,
                   to_list: object,
                   cc_list: object,
                   subject: object,
                   text: object,
                   text_type: object = "plain",
                   files: object = None,
                   server: object = "127.0.0.1"
                   ) -> None:
        """ blah """

        assert isinstance(to_list, list)
        if cc_list:
            assert isinstance(cc_list, list)
            send_list = to_list + cc_list
        else:
            send_list = to_list

        self.__log.debug(f"fromID    : '{from_id}'.")
        self.__log.debug(f"toList    : '{to_list}'.")
        self.__log.debug(f"ccList    : '{cc_list}'.")
        self.__log.debug(f"send_list : '{send_list}'.")
        self.__log.debug(f"subject   : '{subject}'.")
        self.__log.debug(f"text      : '{text}'.")
        self.__log.debug(f"textType  : '{text_type}'.")
        if files:
            self.__log.debug(f"files : '{files}'.")

        self.msg = MIMEMultipart()

        self.msg['From'] = from_id
        self.msg['To'] = COMMASPACE.join(to_list)
        if cc_list:
            self.msg['Cc'] = COMMASPACE.join(cc_list)
        self.msg['Date'] = formatdate(localtime=True)
        self.msg['Subject'] = subject

        self.msg.attach(MIMEText(text, text_type))

        for self.f in files or []:
            try:
                self.f = Path(self.f).resolve(strict=True)
            except FileNotFoundError as e:
                self.__log.exception(f"FileNotFoundError: {e=}")
            except Exception as e:
                self.__log.exception(f"Exception: {e=}")
                sys.exit(5)

            with open(self.f, "rb") as self.file:
                self.part = MIMEApplication(
                    self.file.read(),
                    Name=self.f.name
                )

            # After the file is closed
            self.part['Content-Disposition'] = f'attachment; filename="{self.f.name}"'
            self.msg.attach(self.part)

        self.__log.info(f"Sending email.")

        self.smtp = smtplib.SMTP(server)
        self.smtp.sendmail(from_id, send_list, self.msg.as_string())
        self.smtp.close()

        self.__log.info(f"Email sent.")
