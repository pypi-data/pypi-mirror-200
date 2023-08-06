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

# Python Standard libraries.

import autologging
import logging
import sys

from autologging import logged, traced
from inspect import isfunction


@traced
@logged
class BuildFunctionList:
    """Validate and call an internal function given the function name as a string."""

    def __init__(self, default_command_prefix: object = "function") -> None:
        """Set default function name prefix."""

        self.default_command_prefix = default_command_prefix
        self.program_errors = False
        self.xml_file_errors = False

    def call(self, function_name: object, function_args: object, command_prefix: object = None) -> object:
        """Validate and call an internal funtion given the function name as a string."""

        if command_prefix == None:
            self.function_name = "%s__%s" % (self.default_command_prefix, function_name,)
        else:
            self.function_name = "%s__%s" % (command_prefix, function_name,)

        self.__log.debug("Validating function : %s", self.function_name)

        if self.__class__.__dict__.get(self.function_name):

            self.__log.debug("%s : %s", self.function_name, self.__class__.__dict__[self.function_name])
            if isfunction(self.__class__.__dict__[self.function_name]):

                self.__log.info("Calling function : %s", self.function_name)
                return self.__class__.__dict__[self.function_name](self, function_args)

            else:

                self.__log.error("Requested function name is invalid : '{self.functionName}'")
                print(f"Requested function name is invalid : '{self.functionNam}'", file=sys.strerr)
                self.xml_file_errors = True

        else:

            self.__log.error("BuildFunctionList.call called with invalid function name %s in class %s.",
                             self.function_name, self.__class__)
            self.__log.warning("Add the following line to %s: def %s(self, args): pass", self.__class__,
                               self.function_name)
            self.__log.warning("Or fix the XML file entry that called '%s'.", self.function_name)
            self.xml_file_errors = True
