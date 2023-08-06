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

from ecspylibs.buildfunctionlist import BuildFunctionList

# Python Standard libraries.

import autologging
import logging
import sys

from autologging import logged, traced
from lxml import etree


@traced
@logged
class ParseXML(BuildFunctionList):
    """Class to parse an XML file into its parts."""

    def __init__(self, xml_file: object, conf_version: object, command_prefix: object = "function") -> None:
        """Setup the ParseXML environment."""

        self.root = None
        self.katalon_commands = None
        self.tree = None
        self.xml_file = xml_file
        self.conf_version = conf_version
        self.xml_file_errors = False
        self.program_errors = False

        super().__init__(command_prefix)

    def parse_katalon_xml_headers(self) -> bool:
        """Parse Katalon XML file headers."""

        try:
            self.tree = etree.parse(self.xml_file)
        except Exception as e:
            self.__log.error("Exception error while parsing file '%s'.", self.xml_file)
            self.__log.exception("Exception: '%s'", e)
            self.xml_file_errors = True
            self.program_errors = True
            return False

        self.root = self.tree.getroot()

        if self.root.tag != "TestCase":
            self.__log.error("Missing or invalid root tag line: '%s'", self.root.tag)
            return False

        self.katalon_commands = self.tree.xpath("./*")
        return True

    def parse_xml_headers(self) -> bool:
        """Parse Monitor XML file headers."""

        try:
            self.tree = etree.parse(self.xml_file)
        except Exception as e:
            self.__log.error("Exception error while parsing file '%s'.", self.xml_file)
            self.__log.exception("Exception: '%s'", e)
            self.xml_file_errors = True
            self.program_errors = True
            return False

        self.root = self.tree.getroot()

    def process_katalon_root(self, command_prefix: object = None) -> bool:
        """Process the root entry in the Katalon XML file."""

        for self.katalon_command in self.katalon_commands:
            if self.program_errors or self.xml_file_errors:
                if self.program_errors:
                    self.__log.error("Internal errors processing Katalon Root.  Aborting!")
                else:
                    self.__log.warning("External errors processing Katalon Root.  Aborting!")
                return False

            if not self.call(self.katalon_command.tag, self.katalon_command, command_prefix):
                return False

        return True

    def process_children(self, args: object, command_prefix: object = None) -> bool:
        """Process all the children entries in the Katalon or Monitor XML files."""

        for self.cmd in args.xpath("./*"):
            if self.program_errors or self.xml_file_errors:
                if self.program_errors:
                    self.__log.error("Internal errors processing Children.  Aborting!")
                else:
                    self.__log.warning("External errors processing Children.  Aborting!")
                return False

            if not self.call(self.cmd.tag, self.cmd, command_prefix):
                return False

        return True
