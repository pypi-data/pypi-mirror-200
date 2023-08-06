#!/usr/bin/env python
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
import os
import re
import shutil
import tempfile

from autologging import logged, traced
from os.path import abspath, basename, dirname, isabs, isdir, isfile, ismount, join, normpath


@traced
@logged
class CleanupTempDirs:
    """Locate all children processes, if any, and kill them."""

    def __init__(self) -> None:
        """Setup initial variables."""

        self.delete_tmp_dir = None
        self.tmp_dir_pat = re.compile("^scoped_dir[0-9]+_[0-9]+$")
        self.user_temp_directory = tempfile.gettempdir()

    def cleanup_temp_dirs(self) -> None:
        """Locate all old temp files that were not deleted from previous runs and delete them."""

        if self.user_temp_directory:
            if isdir(self.user_temp_directory):
                self.__log.debug('User Temp Directory is located at "%s".', self.user_temp_directory)
                self.__log.debug('Looking for temp directories which match pattern "^scoped_dir[0-9]+_[0-9]+$".')

                for self.tmp_root, self.tmp_dirs, self.tmp_files in os.walk(self.user_temp_directory):
                    for self.tmp_dir in self.tmp_dirs:
                        self.delete_tmp_dir = join(self.tmp_root, self.tmp_dir)

                        if self.tmp_dir_pat.match(self.tmp_dir):
                            self.__log.warning('Found a temp dir that should have been deleted: "%s".',
                                               self.delete_tmp_dir)

                            # Try to remove the directory.  Just continue if the remove fails.
                            try:
                                self.__log.info('Delete directory "%s".', self.delete_tmp_dir)
                                shutil.rmtree(self.delete_tmp_dir)
                                self.__log.info('Directory "%s" was deleted.', self.delete_tmp_dir)
                            except OSError as e:
                                self.__log.error('Error: %s - %s.', e.filename, e.strerror)
                                self.__log.exception('Exception: "%s".', e)
                            except Exception as e:
                                self.__log.critical('Fatal error occurred while removing directory "%s".',
                                                    self.delete_tmp_dir)
                                self.__log.exception('Exception: "%s".', e)
            else:
                self.__log.error('Variable for User Temp Directory was not a directory "%s".', self.user_temp_directory)
        else:
            self.__log.error('Variable for User Temp Directory was not defined.')
