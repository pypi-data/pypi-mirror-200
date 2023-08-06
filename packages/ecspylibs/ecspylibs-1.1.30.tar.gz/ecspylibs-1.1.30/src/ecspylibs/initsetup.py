#!/usr/bin/env python
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

"""
Doc String
"""

# Python Standard libraries.

import sys
from pathlib import Path
import logging
import os
import re
import time
from socket import gethostname
from symbol import argument
from dataclasses import dataclass
from ecspylibs.configfile import ConfigFile

import autologging
import yaml
from autologging import logged, traced
from lxml import etree


@traced
@logged
@dataclass
class InitSetup:
    """Initialize the environment using command line parameters and init file."""
    arguments: dict
    default_arguments: dict
    config: object = None
    section: object = None

    def __post_init__(self):
        """Setup InitSetup"""

        if self.config is not None:
            if self.config in self.arguments and self.arguments[self.config] is not None:
                self.config = self.arguments[self.config]
            elif self.config in self.default_arguments and self.default_arguments[self.config] is not None:
                self.config = self.default_arguments[self.config]
            else:
                self.config = False
        else:
            self.config = False

        if self.config:
            # try:
            #     self.config = Path(self.config).resolve(strict=True)
            # except FileNotFoundError as e:
            #     print(f"\n: Can't find configuration file {self.config}\n", file=sys.stderr)
            #     print(f"\nFileNotFoundError: {e=}\n", file=sys.stderr)
            #     sys.exit(1)
            # except Exception as e:
            #     print(f"\nException: {e=}\n", file=sys.stderr)
            #     sys.exit(2)

            # with open(self.config, 'r') as file:
            #     config_data = yaml.safe_load(file)

            config_file = ConfigFile(self.config)
            config_data = config_file.read

            if 'config' not in config_data:
                print(f"\nError: Can't find dictionary 'config' in file '{self.config}'. Aborting!\n", file=sys.stderr)
                sys.exit(3)

            config_len = len(config_data['config'])
            section_number = 1

            if self.section and self.section in self.arguments and self.arguments[self.section]:
                if isinstance(self.arguments[self.section], int) or self.arguments[self.section].isnumeric():
                    section_number = int(self.arguments[self.section])
                else:
                    print(f"\nArgument section number '{section_number}' is missing or invalid", file=sys.stderr)
                    print(f"for file '{self.config}'.", file=sys.stderr)
                    print(f"Aborting!\n", file=sys.stderr)
                    sys.exit(4)

            elif 'section' in config_data:
                if isinstance(config_data['section'], int):
                    section_number = int(config_data['section'])

            if section_number > config_len or section_number <= 0:
                print(f"\nSection number '{section_number}' is out of range for file", file=sys.stderr)
                print(f"'{self.config}'.", file=sys.stderr)
                print(f"Aborting!\n", file=sys.stderr)
                sys.exit(5)

            self.data = config_data['config'][section_number - 1]

            for i in self.arguments:
                if self.arguments[i] is None:
                    if i[2:] in self.data:
                        self.arguments[i] = self.data[i[2:]]
                    elif i in self.default_arguments:
                        self.arguments[i] = self.default_arguments[i]
        else:
            for i in self.arguments:
                if self.arguments[i] is None:
                    if i in self.default_arguments:
                        self.arguments[i] = self.default_arguments[i]
