#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.  See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Fri Mar 31 12:26:09 2023 -0400 $
#
# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECSpylibs.git $
#

"""
Doc String
"""

import sys
import os

from dataclasses import dataclass
from pathlib import Path, PosixPath

import csv
import json
import pandas as pd
import toml
import yaml

from configparser import ConfigParser
from lxml import etree

from json.decoder import JSONDecodeError
from lxml.etree import XMLSyntaxError
from toml.decoder import TomlDecodeError
from xlrd.biffh import XLRDError
from yaml.parser import ParserError
from yaml.scanner import ScannerError

@dataclass
class ConfigFile:
    """Read a configuration file and return its data."""

    file: str = None

    def __post_init__(self):
        """Setup ConfigFile."""

        self.csv_methods = {
            "read": self.csv_read,
        }
        self.ini_methods = {
            "read": self.ini_read,
        }
        self.json_methods = {
            "read": self.json_read,
        }
        self.toml_methods = {
            "read": self.toml_read,
        }
        self.xlsx_methods = {
            "read": self.xlsx_read,
        }
        self.xml_methods = {
            "read": self.xml_read,
        }
        self.yaml_methods = {
            "read": self.yaml_read,
        }

        self.suffix_types = {
            ".conf": self.toml_methods,
            ".csv": self.csv_methods,
            ".ini": self.ini_methods,
            ".json": self.json_methods,
            ".toml": self.toml_methods,
            ".xlsx": self.xlsx_methods,
            ".xml": self.xml_methods,
            ".yaml": self.yaml_methods,
            ".yml": self.yaml_methods,
        }

        if type(self.file) is list:
            for tmp in self.file:
                if type(tmp) is PosixPath and tmp.is_file():
                    self.file = tmp.resolve(strict=False)
                    break
                elif type(tmp) is str:
                    tmp = Path(tmp).resolve(strict=False)
                    if tmp.is_file():
                        self.file = tmp.resolve(strict=False)
                        break
            else:
                raise FileNotFoundError

        if type(self.file) is str and self.file:
            self.file = Path(self.file).resolve(strict=False)

        if type(self.file) is PosixPath and self.file.is_file():
            try:
                self.file = self.file.resolve(strict=True)
            except FileNotFoundError as e:
                print(f"\nMissing or invalid configuration file '{self.file}'.\n", file=sys.stderr)
                raise e
            except Exception as e:
                print(f"\nException error processing file '{self.file}'.\n", file=sys.stderr)
                raise e
        else:
            raise TypeError("Parameter must be an existing file name.")

        if self.file.suffix not in self.suffix_types:
            print(f"\nFile '{self.file}' has an unknown suffix type of '{self.file.suffix}'.\n", file=sys.stderr)
            raise NotImplementedError

        self.suffix = self.file.suffix[1:]

    @property
    def read(self) -> object:

        if self.file.suffix in self.suffix_types:
            if "read" in self.suffix_types[self.file.suffix]:
                try:
                    return self.suffix_types[self.file.suffix]['read']()
                except PermissionError as e:
                    print(f"\nPermission error reading file '{self.file}'.\n", file=sys.stderr)
                    raise e
                except UnicodeDecodeError as e:
                    print(f"\nUnicode decode error while parsing file '{self.file}'.\n", file=sys.stderr)
                    raise e
                except Exception as e:
                    print(f"\nException error processing file '{self.file}'.\n", file=sys.stderr)
                    raise e
            else:
                print(f"\nFile '{self.file}' has no function type 'read'.\n", file=sys.stderr)
                raise NotImplementedError
        else:
            print(f"\nFile '{self.file}' has an unknown suffix type of '{self.file.suffix}'.\n", file=sys.stderr)
            raise NotImplementedError

    def csv_read(self) -> object:
        try:
            with open(self.file, 'r') as f:
                reader = csv.reader(f)
                return [row for row in reader]
        except Exception as e:
            print(f"\nException error processing file '{self.file}'.\n", file=sys.stderr)
            raise e

    def ini_read(self) -> object:
        config = ConfigParser()
        try:
            config.read(self.file)
        except Exception as e:
            print(f"\nException error processing file '{self.file}'.\n", file=sys.stderr)
            raise e
        data = {}
        for section in config.sections():
            data[section] = {}
            for key, value in config.items(section):
                data[section][key] = value
        return data

    def json_read(self) -> object:
        try:
            with open(self.file, 'r') as f:
                return json.load(f)
        except JSONDecodeError as e:
            print(f"\nJSON decode error while parsing file '{self.file}'.\n", file=sys.stderr)
            raise e
        except UnicodeDecodeError as e:
            print(f"\nUnicode decode error while parsing file '{self.file}'.\n", file=sys.stderr)
            raise e
        except Exception as e:
            print(f"\nException error processing file '{self.file}'.\n", file=sys.stderr)
            raise e

    def toml_read(self) -> object:
        try:
            return toml.load(self.file)
        except TomlDecodeError as e:
            print(f"\nTOML decode error while parsing file '{self.file}'.\n", file=sys.stderr)
            raise e
        except UnicodeDecodeError as e:
            print(f"\nUnicode decode error while parsing file '{self.file}'.\n", file=sys.stderr)
            raise e
        except Exception as e:
            print(f"\nException error processing file '{self.file}'.\n", file=sys.stderr)
            raise e

    def xlsx_read(self) -> object:
        try:
            return pd.read_excel(self.file, sheet_name=None)
        except XLRDError as e:
            print(f"\nXLSX XLRD error while parsing file '{self.file}'.\n", file=sys.stderr)
            raise e
        except Exception as e:
            print(f"\nException error processing file '{self.file}'.\n", file=sys.stderr)
            raise e

    def xml_read(self) -> object:
        try:
            return etree.parse(os.fspath(self.file))
        except XMLSyntaxError as e:
            print(f"\nXML Syntax error while parsing file '{self.file}'.\n", file=sys.stderr)
            raise e
        except Exception as e:
            print(f"\nException error processing file '{self.file}'.\n", file=sys.stderr)
            raise e

    def yaml_read(self) -> object:
        try:
            with open(self.file, 'r') as f:
                return yaml.safe_load(f)
        except ParserError as e:
            print(f"\nYAML parse error while parsing file '{self.file}'.\n", file=sys.stderr)
            raise e
        except ScannerError as e:
            print(f"\nYAML Scanner error while parsing file '{self.file}'.\n", file=sys.stderr)
            raise e
        except UnicodeDecodeError as e:
            print(f"\nUnicode decode error while parsing file '{self.file}'.\n", file=sys.stderr)
            raise e
        except Exception as e:
            print(f"\nException error processing file '{self.file}'.\n", file=sys.stderr)
            raise e
