#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.  See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Mon Feb 20 16:57:47 2023 -0500 $
#
# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECSpylibs.git $
#

# Futuristic implementation of commands.  Must be first from/import
# command.

from __future__ import print_function

# Python Standard libraries.

import autologging
import logging
import psutil

from autologging import logged, traced


@traced
@logged
class ReapChildren:
    """Locate all children processes, if any, and kill them."""

    def __init__(self) -> None:
        """Nothing to setup."""

    def reap_children(self, timeout: object = 3) -> None:
        """Locate all children processes, if any, and kill them."""

        def on_terminate(proc: object) -> object:
            """Log any process killed by reapChildren."""

            self.__log.warning("Process %s terminated with exit code %s.", proc, proc.returncode)

        processes = psutil.Process().children(recursive=True)

        for process in processes:
            self.__log.warning("Process %s survived drive.quit(); trying SIGTERM!", process)
            process.terminate()

        gone, alive = psutil.wait_procs(processes, timeout=timeout, callback=on_terminate)

        if not alive:
            for process in alive:
                self.__log.error("Process %s survived SIGTERM; trying SIGKILL!", process)
                process.kill()

            gone, alive = psutil.wait_procs(alive, timeout=timeout, callback=on_terminate)

            if not alive:
                for process in alive:
                    self.__log.critical("Process %s survived SIGKILL; giving up!", process)
